# ────────────────────────────────────────────────────────────────────
# Comando: Aplicaciones
# ────────────────────────────────────────────────────────────────────
# Abre y cierra aplicaciones según el perfil del usuario.
# Soporta aliases personalizados y búsqueda de ejecutables.
# ────────────────────────────────────────────────────────────────────

import subprocess
import json
import os

TRIGGERS = ["abrir", "abre", "abro", "ejecutar", "ejecuta", "cerrar", "cierra", "cierro", 
            "terminar", "mata", "matar"]

def cargar_config():
    """Carga configuración y perfil del usuario."""
    from nucleo import cargar_config as _cargar_config, cargar_perfil
    return _cargar_config(), cargar_perfil()

def abrir_app(nombre_app):
    """
    Abre una aplicación usando el nombre del alias del perfil.

    Args:
        nombre_app (str): nombre o alias de la aplicación

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    config, perfil = cargar_config()
    nombre_app = nombre_app.lower().strip()

    # Buscar en el mapa de aplicaciones del perfil
    ejecutable = perfil["aplicaciones"].get(nombre_app, nombre_app)

    try:
        # Intentar abrir con shell
        subprocess.Popen(ejecutable, shell=True)
        return True, f"Abriendo {nombre_app}."
    except Exception as e:
        return False, f"No pude abrir {nombre_app}: {str(e)}"

def cerrar_app(nombre_app):
    """
    Cierra una aplicación por nombre de proceso.

    Args:
        nombre_app (str): nombre o alias de la aplicación

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    config, perfil = cargar_config()
    nombre_app = nombre_app.lower().strip()

    # Buscar en el mapa de aplicaciones
    proceso = perfil["aplicaciones"].get(nombre_app, nombre_app)

    # Extraer solo el nombre del ejecutable sin .exe si está presente
    if proceso.endswith(".exe"):
        proceso = proceso[:-4]

    try:
        # Usar taskkill para cerrar el proceso
        resultado = subprocess.run(
            ["taskkill", "/F", "/IM", f"{proceso}.exe"],
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            return True, f"Cerré {nombre_app}."
        else:
            return False, f"{nombre_app} no estaba abierto o no pude cerrarlo."
    except Exception as e:
        return False, f"Error al cerrar {nombre_app}: {str(e)}"

def ejecutar(parametro):
    """
    Ejecuta el comando de aplicación.
    Detecta automáticamente si es "abrir" o "cerrar" por contexto.

    Args:
        parametro (str): nombre de la aplicación y acción

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    parametro = parametro.lower().strip()

    if not parametro:
        return False, "Especificá qué aplicación querés abrir o cerrar."

    # Por defecto, abre la aplicación
    # En una versión más avanzada, se podría usar NLP para detectar "cerrar"
    return abrir_app(parametro)

# Funciones auxiliares expuestas para uso directo
__all__ = ["abrir_app", "cerrar_app", "ejecutar", "TRIGGERS"]
