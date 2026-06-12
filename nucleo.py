# ────────────────────────────────────────────────────────────────────
# Núcleo: Utilidades compartidas
# ────────────────────────────────────────────────────────────────────
# Funciones comunes para audio, transcripción, TTS, IA y logging.
# ────────────────────────────────────────────────────────────────────

import json
import os
import sys
import tempfile
import subprocess
import logging
from datetime import datetime
from typing import Tuple, Dict, List

def obtener_ruta_recurso(ruta_relativa: str) -> str:
    """Ruta absoluta para lectura de archivos empaquetados (sys._MEIPASS o junto al script)."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_relativa)

def obtener_ruta_escritura(ruta_relativa: str) -> str:
    """Ruta absoluta para escritura (junto al .exe o junto al script)."""
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_relativa)

# Configurar logging
def configurar_logging():
    """Configura el sistema de logging del asistente."""
    ruta_logs = obtener_ruta_escritura("logs")
    os.makedirs(ruta_logs, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(ruta_logs, f"jarvis_{timestamp}.log")),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = configurar_logging()

def cargar_config() -> Dict:
    """Carga config.json: primero junto al .exe (modificaciones), sino bundle."""
    ruta = obtener_ruta_escritura("config.json")
    if not os.path.exists(ruta):
        ruta = obtener_ruta_recurso("config.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def cargar_perfil() -> Dict:
    """Carga perfil: primero junto al .exe (modificaciones), sino bundle."""
    ruta = obtener_ruta_escritura("perfiles/default.json")
    if not os.path.exists(ruta):
        ruta = obtener_ruta_recurso("perfiles/default.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_config(config: Dict):
    """Guarda config.json junto al ejecutable."""
    ruta = obtener_ruta_escritura("config.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def guardar_perfil(perfil: Dict):
    """Guarda el perfil del usuario junto al ejecutable."""
    ruta = obtener_ruta_escritura("perfiles/default.json")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(perfil, f, indent=2, ensure_ascii=False)

# ────────────────────────────────────────────────────────────────────
# Funciones de Audio
# ────────────────────────────────────────────────────────────────────

def grabar_audio(segundos: int = 5) -> 'np.ndarray':
    """
    Graba audio del micrófono seleccionado.

    Args:
        segundos (int): duración de la grabación

    Returns:
        np.ndarray: audio grabado
    """
    import sounddevice as sd
    import numpy as np

    config = cargar_config()
    sample_rate = config["audio"]["sample_rate"]
    device = config["audio"]["dispositivo_mic"]

    logger.info(f"Grabando {segundos} segundos desde dispositivo {device}...")

    audio = sd.rec(
        int(segundos * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        device=device
    )
    sd.wait()

    return audio

def esperar_wakeword() -> bool:
    """
    Espera a que el usuario diga la palabra clave.

    Returns:
        bool: True si se detectó la palabra clave
    """
    import sounddevice as sd
    import numpy as np
    from openwakeword.model import Model as WakeModel

    config = cargar_config()
    sample_rate = config["audio"]["sample_rate"]
    chunk_size = config["audio"]["chunk_size"]
    device = config["audio"]["dispositivo_mic"]
    modelo_path = config["wakeword"]["modelo"]
    umbral = config["wakeword"]["umbral"]

    logger.info("Esperando palabra clave...")

    wake_model = WakeModel(
        wakeword_models=[modelo_path],
        inference_framework=config["wakeword"]["framework"]
    )
    wake_model.reset()

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        device=device,
        blocksize=chunk_size
    ) as stream:
        while True:
            chunk, _ = stream.read(chunk_size)
            chunk_np = np.squeeze(chunk)
            prediccion = wake_model.predict(chunk_np)
            score = list(prediccion.values())[0]

            if score >= umbral:
                logger.info(f"Palabra clave detectada (score: {score:.2f})")
                return True

# ────────────────────────────────────────────────────────────────────
# Funciones de Transcripción
# ────────────────────────────────────────────────────────────────────

def transcribir(audio: 'np.ndarray') -> str:
    """
    Transcribe audio usando Whisper.

    Args:
        audio (np.ndarray): datos de audio

    Returns:
        str: texto transcrito
    """
    import scipy.io.wavfile as wav
    from faster_whisper import WhisperModel

    config = cargar_config()
    modelo_whisper = config["whisper"]["modelo"]
    sample_rate = config["audio"]["sample_rate"]
    idioma = config["audio"]["idioma"]

    # Crear archivo temporal
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp.name
    tmp.close()

    try:
        # Guardar audio en archivo temporal
        wav.write(tmp_path, sample_rate, audio)

        # Transcribir con Whisper
        logger.info(f"Transcribiendo con modelo {modelo_whisper}...")
        whisper_model = WhisperModel(
            modelo_whisper,
            device=config["whisper"]["device"],
            compute_type=config["whisper"]["compute_type"]
        )

        segmentos, _ = whisper_model.transcribe(tmp_path, language=idioma)
        texto = " ".join(s.text for s in segmentos)

        logger.info(f"Transcripción: {texto}")
        return texto.strip().lower()

    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

# ────────────────────────────────────────────────────────────────────
# Funciones de TTS (Text-to-Speech)
# ────────────────────────────────────────────────────────────────────

def hablar(texto: str) -> bool:
    """
    Convierte texto a voz usando el motor TTS configurado.

    Args:
        texto (str): texto a reproducir

    Returns:
        bool: True si fue exitoso
    """
    config = cargar_config()
    motor = config["tts"]["motor"]

    logger.info(f"Asistente: {texto}")

    if motor == "powershell":
        return _hablar_powershell(texto)
    elif motor == "pyttsx3":
        return _hablar_pyttsx3(texto)
    else:
        logger.error(f"Motor TTS desconocido: {motor}")
        return False

def _hablar_powershell(texto: str) -> bool:
    """Usa PowerShell y TTS de Windows para hablar."""
    config = cargar_config()
    voz = config["tts"]["voz"]

    # Limpiar caracteres problemáticos
    texto_safe = texto.replace("'", "").replace('"', "")

    try:
        subprocess.run([
            "powershell", "-Command",
            f"Add-Type -AssemblyName System.Speech; "
            f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$s.SelectVoice('{voz}'); "
            f"$s.Speak('{texto_safe}')"
        ], capture_output=True, timeout=30)
        return True
    except Exception as e:
        logger.error(f"Error en TTS PowerShell: {e}")
        return False

def _hablar_pyttsx3(texto: str) -> bool:
    """Usa pyttsx3 para hablar."""
    try:
        import pyttsx3
        config = cargar_config()
        voz = config["tts"]["voz"]

        engine = pyttsx3.init()
        # Configurar voz (si está disponible)
        # engine.setProperty('voice', voz)
        engine.say(texto)
        engine.runAndWait()
        return True
    except Exception as e:
        logger.error(f"Error en TTS pyttsx3: {e}")
        return False

# ────────────────────────────────────────────────────────────────────
# Funciones de IA
# ────────────────────────────────────────────────────────────────────

def consultar_ia(comando: str, historial: List[Dict]) -> Tuple[str, str]:
    """
    Consulta al modelo de IA configurado.

    Args:
        comando (str): comando o pregunta del usuario
        historial (List[Dict]): historial de conversación

    Returns:
        tuple: (accion, parametro)
    """
    config = cargar_config()
    tipo_ia = config["modelo_ia"]["tipo"]

    if tipo_ia == "ollama":
        return _consultar_ollama(comando, historial)
    elif tipo_ia == "claude":
        return _consultar_claude(comando, historial)
    elif tipo_ia == "openai":
        return _consultar_openai(comando, historial)
    else:
        logger.error(f"Tipo de IA desconocido: {tipo_ia}")
        return "conversar", "No tengo conexión con el modelo de IA."

def _consultar_ollama(comando: str, historial: List[Dict]) -> Tuple[str, str]:
    """Consulta a Ollama."""
    import ollama

    config = cargar_config()
    modelo = config["modelo_ia"]["opciones"]["ollama"]["modelo"]

    historial.append({"role": "user", "content": comando})

    system_prompt = (
        "Sos un asistente de escritorio en español rioplatense.\n"
        "Respondé SIEMPRE con un JSON válido y nada más, sin explicaciones, sin markdown.\n"
        "Formato exacto: {\"accion\": \"ACCION\", \"parametro\": \"VALOR\"}\n"
        "Acciones disponibles:\n"
        "- conversar: para charla o preguntas generales. parametro = tu respuesta corta.\n"
        "- reproducir_musica: cuando pidan poner música. parametro = nombre canción, artista o género.\n"
        "- cerrar_ventana: cuando pidan cerrar un programa. parametro = nombre del programa.\n"
        "- abrir_app: cuando pidan abrir algo. parametro = nombre del programa.\n"
        "- obtener_hora: cuando pidan la hora. parametro = vacio.\n"
        "- obtener_fecha: cuando pidan la fecha. parametro = vacio.\n"
        "- escribir: cuando pidan escribir algo (búsqueda, formulario, etc). parametro = texto a escribir.\n"
        "- youtube: cuando pidan youtube o buscar video. parametro = término de búsqueda (opcional).\n"
        "- play_pause: cuando pidan pausar, reanudar o seguir la música. parametro = vacio.\n"
        "- siguiente_cancion: cuando pidan pasar a la siguiente canción. parametro = vacio.\n"
        "- anterior_cancion: cuando pidan volver a la canción anterior. parametro = vacio.\n"
        "- cerrar_pestania: cuando pidan cerrar una pestaña del navegador. parametro = vacio.\n"
        "- subir_volumen: cuando pidan subir el volumen. parametro = vacio.\n"
        "- bajar_volumen: cuando pidan bajar el volumen. parametro = vacio.\n"
        "- silenciar: cuando pidan silenciar o mutear. parametro = vacio.\n"
        "- establecer_volumen: cuando pidan un volumen específico. parametro = número del 0 al 100.\n"
        "Nunca respondas fuera del JSON. Nunca inventes información."
    )

    try:
        respuesta = ollama.chat(
            model=modelo,
            messages=[{"role": "system", "content": system_prompt}] + historial
        )

        texto = respuesta["message"]["content"].strip()
        historial.append({"role": "assistant", "content": texto})

        # Limpiar markdown si existe
        texto = texto.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(texto)
            accion = data.get("accion", "conversar")
            parametro = data.get("parametro", "")
            logger.info(f"Acción: {accion} | Parámetro: {parametro}")
            return accion, parametro
        except json.JSONDecodeError:
            logger.error(f"JSON inválido de Ollama: {texto}")
            return "conversar", "No entendí bien, podés repetir?"

    except Exception as e:
        logger.error(f"Error consultando Ollama: {e}")
        return "conversar", "Hubo un error consultando el modelo de IA."

def _consultar_claude(comando: str, historial: List[Dict]) -> Tuple[str, str]:
    """Consulta a Claude API (por implementar)."""
    logger.warning("Claude API no implementado aún")
    return "conversar", "Claude API no está configurada."

def _consultar_openai(comando: str, historial: List[Dict]) -> Tuple[str, str]:
    """Consulta a OpenAI API (por implementar)."""
    logger.warning("OpenAI API no implementado aún")
    return "conversar", "OpenAI API no está configurada."

# ────────────────────────────────────────────────────────────────────
# Funciones de Acciones
# ────────────────────────────────────────────────────────────────────

def ejecutar_accion(accion: str, parametro: str) -> Tuple[bool, str]:
    """
    Ejecuta la acción decidida por el IA.

    Primero busca en comandos del usuario (dinámicos).
    Si no existe, fallback a comandos core (Python).

    Args:
        accion (str): nombre de la acción
        parametro (str): parámetro para la acción

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    logger.info(f"Ejecutando acción: {accion} con parámetro: {parametro}")

    try:
        # ─── FASE 1: Buscar en comandos dinámicos del usuario ───
        import comandos_usuario
        cmd = comandos_usuario.buscar_comando_por_trigger(accion)
        if cmd:
            logger.info(f"Comando dinámico encontrado: {cmd['nombre']}")
            return comandos_usuario.ejecutar_comando(cmd)

        # ─── FASE 2: Fallback a comandos core ───
        if accion == "reproducir_musica":
            from comandos import musica
            return musica.ejecutar(parametro)

        elif accion == "abrir_app":
            from comandos import apps
            return apps.abrir_app(parametro)

        elif accion == "cerrar_ventana":
            from comandos import apps
            return apps.cerrar_app(parametro)

        elif accion == "obtener_hora":
            from comandos import sistema
            return sistema.obtener_hora()

        elif accion == "obtener_fecha":
            from comandos import sistema
            return sistema.obtener_fecha()

        elif accion == "escribir":
            from comandos import escribir
            return escribir.ejecutar(parametro)

        elif accion == "youtube":
            from comandos import youtube
            return youtube.ejecutar(parametro)

        elif accion == "play_pause":
            from comandos import media
            return media.play_pause()

        elif accion == "siguiente_cancion":
            from comandos import media
            return media.siguiente()

        elif accion == "anterior_cancion":
            from comandos import media
            return media.anterior()

        elif accion == "cerrar_pestania":
            from comandos import media
            return media.cerrar_pestania()

        elif accion == "subir_volumen":
            from comandos import sistema
            return sistema.controlar_volumen("subir")

        elif accion == "bajar_volumen":
            from comandos import sistema
            return sistema.controlar_volumen("bajar")

        elif accion == "silenciar":
            from comandos import sistema
            return sistema.controlar_volumen("silencio")

        elif accion == "establecer_volumen":
            from comandos import sistema
            return sistema.controlar_volumen("establecer", parametro)

        elif accion == "conversar":
            from comandos import conversar
            return conversar.ejecutar(parametro)

        else:
            logger.warning(f"Acción desconocida: {accion}")
            return False, f"No sé cómo ejecutar la acción '{accion}'."

    except Exception as e:
        logger.error(f"Error ejecutando acción {accion}: {e}")
        return False, f"Error al ejecutar {accion}: {str(e)}"

# Exportar funciones principales
__all__ = [
    "cargar_config", "cargar_perfil", "guardar_config", "guardar_perfil",
    "grabar_audio", "esperar_wakeword", "transcribir", "hablar",
    "consultar_ia", "ejecutar_accion", "logger"
]
