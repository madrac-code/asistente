@echo off
REM ────────────────────────────────────────────────────────────────────
REM EMPAQUETAR JARVIS COMO .EXE
REM ────────────────────────────────────────────────────────────────────
REM Este script convierte Jarvis en un ejecutable standalone para Windows
REM ────────────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion

color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        EMPAQUETAR JARVIS COMO EJECUTABLE (.EXE)                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si estamos en el entorno virtual
if not defined VIRTUAL_ENV (
	echo [!] No estás en el entorno virtual
	echo [*] Activando venv...
	if exist C:\asistente\venv\Scripts\activate.bat (
		call C:\asistente\venv\Scripts\activate.bat
	) else (
		call C:\asistente\venv\Scripts\activate.bat
	)
)

REM Instalar PyInstaller
echo [*] Instalando PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
	echo [!] Error instalando PyInstaller
	pause
	exit /b 1
)

REM Crear directorio de distribución
if exist dist (
	echo [*] Limpiando distribuciones previas...
	rmdir /s /q dist
	rmdir /s /q build
	del /q asistente.spec
)

echo.
echo [*] Empaquetando Jarvis...
echo [*] Esto puede tardar 2-5 minutos...
echo.

REM Ejecutar PyInstaller
pyinstaller --onefile ^
	--windowed ^
	--name "Jarvis" ^
	--add-data "config.json:." ^
	--add-data "perfiles:perfiles" ^
	--add-data "comandos:comandos" ^
	--add-data "logs:logs" ^
	--add-data "data:data" ^
	--hidden-import=faster_whisper ^
	--hidden-import=openwakeword ^
	--hidden-import=sounddevice ^
	--hidden-import=scipy ^
	--hidden-import=numpy ^
	--hidden-import=ollama ^
	--hidden-import=PIL ^
	--hidden-import=pyautogui ^
	--hidden-import=_cffi_backend ^
	--hidden-import=cffi ^
	--hidden-import=_soundfile ^
	--add-binary "venv\Lib\site-packages\_cffi_backend*.pyd;." ^
	--add-data "venv\Lib\site-packages\openwakeword\resources\models;openwakeword\resources\models" ^
	asistente.py

if errorlevel 1 (
	echo [!] Error durante el empaquetamiento
	pause
	exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   EMPAQUETAMIENTO COMPLETADO                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [✓] Ejecutable creado: dist\Jarvis.exe

echo.
echo [*] Instrucciones:
echo    1. El archivo .exe está en: dist\Jarvis.exe
echo    2. Puedes copiarlo a cualquier carpeta
echo    3. Requiere: config.json, perfiles\, comandos\, data\ en la misma carpeta
echo    4. O ejecutarlo desde C:\asistente\ directamente
echo.

echo [*] Para crear un instalador profesional:
echo    1. Descarga NSIS: https://nsis.sourceforge.io
echo    2. Crea un script .nsi personalizado
echo    3. Compila con NSIS
echo.

pause
