# ────────────────────────────────────────────────────────────────────
# JARVIS - Asistente de Escritorio Local en Windows
# ────────────────────────────────────────────────────────────────────
# Loop principal del asistente. Orquesta el flujo completo.
# ────────────────────────────────────────────────────────────────────

import sys
import os
import time
import atexit
import subprocess
import urllib.request
import urllib.error
import threading
import nucleo
from gui import crear_gui

historial = []
_proceso_ollama = None


def _ollama_responde() -> bool:
    try:
        urllib.request.urlopen("http://127.0.0.1:11434", timeout=2)
        return True
    except Exception:
        return False


def _iniciar_ollama():
    global _proceso_ollama
    if _ollama_responde():
        nucleo.logger.info("Ollama ya está corriendo")
        return

    nucleo.logger.info("Iniciando Ollama...")
    try:
        _proceso_ollama = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        for _ in range(30):
            if _ollama_responde():
                nucleo.logger.info("Ollama iniciado correctamente")
                return
            time.sleep(0.5)
        nucleo.logger.warning("Ollama no respondió después de 15 segundos")
    except FileNotFoundError:
        nucleo.logger.error("Ollama no encontrado. Instalalo en https://ollama.com")


def _detener_ollama():
    global _proceso_ollama
    if _proceso_ollama:
        nucleo.logger.info("Deteniendo Ollama...")
        _proceso_ollama.terminate()
        try:
            _proceso_ollama.wait(timeout=5)
        except Exception:
            _proceso_ollama.kill()
        _proceso_ollama = None

def inicializar_sistema():
    """Inicializa todos los componentes del asistente."""
    nucleo.logger.info("=" * 70)
    nucleo.logger.info("INICIANDO JARVIS")
    nucleo.logger.info("=" * 70)
    try:
        config = nucleo.cargar_config()
        perfil = nucleo.cargar_perfil()
        nucleo.logger.info(f"Configuración cargada: {config['modelo_ia']['tipo']}")
        return True
    except Exception as e:
        nucleo.logger.error(f"Error inicializando sistema: {e}")
        return False

def loop_principal(gui=None):
    """Loop principal del asistente."""
    global historial

    nucleo.hablar("Asistente iniciado. Decí hey Jarvis para activarme.")
    if gui:
        gui.actualizar_estado("Escuchando...")
        gui.agregar_log("Sistema listo. Esperando palabra clave...")

    nucleo.logger.info("Sistema listo. Esperando wakeword...")

    while True:
        try:
            if gui and not gui.activo:
                continue

            if gui:
                gui.actualizar_estado("Esperando wakeword...")

            nucleo.esperar_wakeword()

            nucleo.logger.info("Palabra clave detectada!")
            if gui:
                gui.actualizar_estado("Palabra clave detectada")
                gui.agregar_log("✓ Palabra clave detectada")

            nucleo.hablar("Sí?")

            if gui:
                gui.actualizar_estado("Grabando comando...")

            config = nucleo.cargar_config()
            audio_cmd = nucleo.grabar_audio(segundos=config["audio"]["duracion_grabacion"])

            if gui:
                gui.actualizar_estado("Transcribiendo...")

            comando = nucleo.transcribir(audio_cmd)

            if gui:
                gui.actualizar_comando(comando)
                gui.agregar_log(f"Transcripción: '{comando}'")

            if comando:
                if gui:
                    gui.actualizar_estado("Procesando...")

                accion, parametro = nucleo.consultar_ia(comando, historial)
                nucleo.logger.info(f"Acción: {accion} | Parámetro: {parametro}")

                if gui:
                    gui.actualizar_estado("Ejecutando...")

                exito, mensaje = nucleo.ejecutar_accion(accion, parametro)

                if gui:
                    gui.actualizar_respuesta(mensaje)
                    gui.agregar_log(f"Respuesta: {mensaje}")

                if gui:
                    gui.actualizar_estado("Hablando...")

                nucleo.hablar(mensaje)
            else:
                nucleo.hablar("No entendí nada, intentá de nuevo.")

            if gui:
                gui.actualizar_estado("Escuchando...")

        except KeyboardInterrupt:
            nucleo.logger.info("Asistente interrumpido por usuario")
            if gui:
                gui.agregar_log("Asistente detenido")
            nucleo.hablar("Adiós!")
            _detener_ollama()
            break

        except Exception as e:
            nucleo.logger.error(f"Error en loop principal: {e}", exc_info=True)
            if gui:
                gui.agregar_log(f"Error: {e}")
            nucleo.hablar("Ocurrió un error. Intentá de nuevo.")

def main():
    """Función principal."""
    _iniciar_ollama()
    atexit.register(_detener_ollama)

    if not inicializar_sistema():
        nucleo.logger.error("No se pudo inicializar el sistema")
        sys.exit(1)

    config = nucleo.cargar_config()
    if config["interfaz"]["mostrar_gui"]:
        gui, root = crear_gui()
        thread_asistente = threading.Thread(target=loop_principal, args=(gui,), daemon=True)
        thread_asistente.start()
        gui.mostrar()
    else:
        loop_principal(gui=None)

if __name__ == "__main__":
    main()
