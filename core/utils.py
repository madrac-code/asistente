# ────────────────────────────────────────────────────────────────────
# Utilidades
# ────────────────────────────────────────────────────────────────────
# Funciones utilitarias compartidas.
# ────────────────────────────────────────────────────────────────────

import os
import sys
from typing import Tuple


def _raiz_proyecto() -> str:
    """Retorna la raíz del proyecto (parent del directorio core/)."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _raiz_ejecutable() -> str:
    """Retorna el directorio del ejecutable o raíz del proyecto."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return _raiz_proyecto()


def obtener_ruta_recurso(ruta_relativa: str) -> str:
    """Ruta absoluta para lectura de archivos empaquetados o raíz del proyecto."""
    return os.path.join(_raiz_proyecto(), ruta_relativa)


def obtener_ruta_escritura(ruta_relativa: str) -> str:
    """Ruta absoluta para escritura (junto al .exe o raíz del proyecto)."""
    return os.path.join(_raiz_ejecutable(), ruta_relativa)

__all__ = [
    "obtener_ruta_recurso",
    "obtener_ruta_escritura"
]
