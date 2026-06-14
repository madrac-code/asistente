#!/usr/bin/env python3
# Test script to verify the new core module structure

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing core module imports...")

try:
    from core import (
        cargar_config,
        cargar_perfil,
        guardar_config,
        guardar_perfil,
        configurar_logging,
        logger,
        grabar_audio,
        esperar_wakeword,
        transcribir,
        hablar,
        normalizar,
        _distancia_edicion,
        detectar_intencion_basica,
        consultar_ia,
        _consultar_ollama,
        _consultar_claude,
        _consultar_openai,
        ejecutar_accion
    )
    print("✅ Successfully imported all core functions")
except ImportError as e:
    print(f"❌ Failed to import core functions: {e}")
    sys.exit(1)

print("\nTesting command imports...")

try:
    from comandos import musica, apps, sistema, conversar, escribir, youtube
    print("✅ Successfully imported all command modules")
except ImportError as e:
    print(f"❌ Failed to import command modules: {e}")
    sys.exit(1)

print("\nTesting GUI imports...")

try:
    from ui.main import InterfazJarvis, crear_gui
    print("✅ Successfully imported main GUI components")
except ImportError as e:
    print(f"❌ Failed to import GUI components: {e}")
    sys.exit(1)

print("\nTesting command manager imports...")

try:
    from ui.commands import VentanaGestorComandos, VentanaEditarComando, abrir_gestor_comandos
    print("✅ Successfully imported command manager components")
except ImportError as e:
    print(f"❌ Failed to import command manager components: {e}")
    sys.exit(1)

print("\nTesting copilot imports...")

try:
    from ui.copilot import PanelCopiloto, crear_panel_copilot
    print("✅ Successfully imported copilot components")
except ImportError as e:
    print(f"❌ Failed to import copilot components: {e}")
    sys.exit(1)

print("\n✅ All imports successful! The new structure is working correctly.")
print("\nSummary of new structure:")
print("  - core/: Contains all core functionality (config, audio, transcription, TTS, IA, actions)")
print("  - commands/: Contains all command implementations")
print("  - ui/main/: Contains main GUI components")
print("  - ui/commands/: Contains command management GUI")
print("  - ui/copilot/: Contains copilot panel")
print("  - tests/: Contains all test files")
print("  - artifacts/: Contains build artifacts")
print("  - storage/: Contains user data")
print("  - cache/: Contains Python cache")
print("  - env/: Contains virtual environment")
