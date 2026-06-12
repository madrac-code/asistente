import pyautogui
import time

TRIGGERS = ["pausa", "pausar", "play", "pasar", "seguir", "siguiente",
            "anterior", "volver", "music", "música", "pestania", "pestaña",
            "cerrar pestania", "cerrar pestaña", "cerra esa pestaña"]

VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1

def _send_media_key(vk_code):
    import ctypes
    from ctypes import wintypes

    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
        ]

    class INPUT_(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT)]
        _fields_ = [
            ("type", wintypes.DWORD),
            ("u", _INPUT)
        ]

    ki = KEYBDINPUT()
    ki.wVk = vk_code
    ki.dwFlags = 0
    inp = INPUT_()
    inp.type = INPUT_KEYBOARD
    inp.u.ki = ki
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT_))

    ki.dwFlags = KEYEVENTF_KEYUP
    inp.u.ki = ki
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT_))

def play_pause():
    _send_media_key(VK_MEDIA_PLAY_PAUSE)
    return True, "Play/Pause"

def siguiente():
    _send_media_key(VK_MEDIA_NEXT_TRACK)
    return True, "Siguiente canción"

def anterior():
    _send_media_key(VK_MEDIA_PREV_TRACK)
    return True, "Canción anterior"

def cerrar_pestania():
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'w')
    return True, "Pestaña cerrada"

def ejecutar(parametro):
    p = parametro.lower().strip()

    if not p:
        return play_pause()

    if any(w in p for w in ["pausa", "pausar", "stop", "seguir", "play"]):
        return play_pause()
    elif any(w in p for w in ["siguiente", "pasar", "proximo", "próximo"]):
        return siguiente()
    elif any(w in p for w in ["anterior", "volver", "volvé", "atras"]):
        return anterior()
    elif any(w in p for w in ["pestaña", "pestania", "ventana"]):
        return cerrar_pestania()
    else:
        return play_pause()

__all__ = ["play_pause", "siguiente", "anterior", "cerrar_pestania", "ejecutar", "TRIGGERS"]
