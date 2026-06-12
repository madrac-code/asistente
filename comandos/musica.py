# ────────────────────────────────────────────────────────────────────
# Comando: Música
# ────────────────────────────────────────────────────────────────────
# Gestiona reproducción de música: busca archivos, selecciona géneros,
# y controla reproducción mediante VLC.
# ────────────────────────────────────────────────────────────────────

import os
import glob
import random
import subprocess
import json

TRIGGERS = ["poner", "reproducir", "música", "cancion", "canción", "genero", "género", 
            "playlist", "tema", "artista", "album"]

def cargar_config():
    """Carga configuración y perfil del usuario."""
    from nucleo import cargar_config as _cargar_config, cargar_perfil
    return _cargar_config(), cargar_perfil()

def buscar_musica(parametro):
    """
    Busca archivos de música en ~/Music y subcarpetas.
    Acepta:
      - Nombre de canción o artista
      - Género (nombre de carpeta)
      - Palabras clave dentro del nombre del archivo

    Retorna: (ruta_archivo, mensaje_respuesta)
    """
    config, perfil = cargar_config()
    carpeta_musica = os.path.expanduser(config["carpetas"]["musica"])
    extensiones = ["*.mp3", "*.flac", "*.wav", "*.ogg", "*.m4a"]
    parametro = parametro.lower().strip()

    # Buscar en todas las subcarpetas y raíz
    todos = []
    for ext in extensiones:
        todos += glob.glob(os.path.join(carpeta_musica, "**", ext), recursive=True)
        todos += glob.glob(os.path.join(carpeta_musica, ext))

    if not todos:
        return None, "No encontré ningún archivo de música en la carpeta."

    # Si pide un género (nombre de carpeta exacto o alias)
    for genero_alias, genero_real in perfil["generos_musica"].items():
        if parametro.lower() == genero_alias.lower():
            genero_path = os.path.join(carpeta_musica, genero_real)
            if os.path.isdir(genero_path):
                archivos_genero = []
                for ext in extensiones:
                    archivos_genero += glob.glob(os.path.join(genero_path, ext))
                if archivos_genero:
                    elegido = random.choice(archivos_genero)
                    return elegido, f"Poniendo música de {genero_real}."

    # Buscar por nombre de archivo (búsqueda parcial)
    coincidencias = []
    for archivo in todos:
        nombre = os.path.splitext(os.path.basename(archivo))[0].lower()
        if parametro in nombre:
            coincidencias.append(archivo)

    if coincidencias:
        elegido = random.choice(coincidencias)
        return elegido, f"Poniendo {os.path.basename(elegido)}."

    # Si no encontró nada específico, elige aleatoria
    elegido = random.choice(todos)
    return elegido, f"No encontré exactamente eso, poniendo {os.path.basename(elegido)}."

def reproducir_musica(ruta_archivo):
    """Abre el archivo de música con el reproductor predeterminado."""
    try:
        subprocess.Popen(["start", "", ruta_archivo], shell=True)
        return True
    except Exception as e:
        print(f"Error al reproducir música: {e}")
        return False

def ejecutar(parametro):
    """
    Ejecuta el comando de música.

    Args:
        parametro (str): nombre de canción, artista, género o búsqueda

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    if not parametro or parametro.strip() == "":
        return False, "Decí qué música querés escuchar."

    ruta, mensaje = buscar_musica(parametro)
    if ruta:
        exito = reproducir_musica(ruta)
        return exito, mensaje
    else:
        return False, mensaje
