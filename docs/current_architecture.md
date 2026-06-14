# Arquitectura Actual - MADRAC Asistente

## Resumen General

MADRAC Asistente es un asistente de escritorio local para Windows que combina reconocimiento de voz, transcripción, IA y automatización de tareas.

## Estructura del Proyecto

```
madrac-asistente/
├── asistente.py                    # Loop principal del asistente
├── nucleo.py                       # Utilidades compartidas (audio, STT, TTS, IA, logging)
├── comandos/                       # Paquete de comandos
│   ├── __init__.py                # Exportaciones
│   ├── apps.py                    # Comando de aplicaciones
│   ├── conversar.py               # Comando conversacional
│   ├── escribir.py                # Comando de escritura
│   ├── media.py                   # Comando de medios
│   ├── musica.py                  # Comando de música
│   ├── sistema.py                 # Comando del sistema
│   └── youtube.py                 # Comando de YouTube
├── gui.py                          # Ventana principal de la interfaz
├── gui_comandos.py                 # Ventana del gestor de comandos
├── gui_copiloto.py                 # Panel del copiloto IA
├── historial.py                    # Gestión del historial de conversación
├── config.json                     # Configuración principal
├── perfiles/                       # Perfiles de usuario
│   └── default.json               # Perfil predeterminado
├── comandos_usuario.py             # Gestor de comandos dinámicos del usuario
├── acciones_copiloto.py             # Acciones permitidas para IA copiloto
├── system_prompt_copiloto.py       # System prompt para IA copiloto
├── indexador_proyecto.py           # Indexador de proyecto para contexto
├── prueba_whisper.py               # Prueba de Whisper
├── pruebas_intenciones.py          # Pruebas de detección de intenciones
├── test_whisper.py                 # Test de Whisper
├── tests_historial.py              # Tests de historial
├── empaquetar.bat                  # Script de empaquetado
├── iniciar.bat                     # Script de inicio
├── build/                          # Build artifacts
├── dist/                           # Distributable
├── logs/                           # Logs
├── data/                           # Datos del usuario
├── venv/                           # Entorno virtual
├── __pycache__/                    # Cache de Python
└── requirements.txt                # Dependencias
```

## Módulos Principales

### 1. asistente.py
**Responsabilidades:**
- Loop principal del asistente
- Inicialización del sistema
- Manejo de la interfaz gráfica
- Coordinación de todos los componentes

**Dependencias:**
- nucleo (para funciones de audio, IA, TTS)
- gui (para interfaz gráfica)
- historial (para gestión de conversación)

### 2. nucleo.py
**Responsabilidades:**
- Funciones utilitarias compartidas
- Grabación de audio
- Transcripción con Whisper
- Síntesis de voz
- Logging
- Carga de configuración y perfiles
- Detección de wakeword
- Consulta a IA
- Ejecución de acciones

**Dependencias:**
- sounddevice, numpy, scipy (para audio)
- faster_whisper (para STT)
- ollama (para IA)
- subprocess (para TTS)

### 3. comandos/
**Responsabilidades:**
- Implementación de todos los comandos disponibles
- Cada comando tiene:
  - TRIGGERS: palabras clave que lo activan
  - ejecutar(parametro): función que ejecuta la acción

**Dependencias:**
- nucleo (para funciones de sistema)
- comandos_usuario (para comandos dinámicos)

### 4. gui.py
**Responsabilidades:**
- Ventana principal de la interfaz
- Panel de monitorización
- Panel del copiloto IA
- Botones de control

**Dependencias:**
- tkinter (para GUI)
- nucleo (para configuración)

### 5. gui_comandos.py
**Responsabilidades:**
- Ventana para crear/editar/eliminar comandos dinámicos
- Tabla de comandos con scrollbar
- Botones de acción (Nuevo, Editar, Ejecutar, Eliminar, Recargar)

**Dependencias:**
- tkinter (para GUI)
- comandos_usuario (para gestión de comandos)

### 6. gui_copiloto.py
**Responsabilidades:**
- Panel de chat para comunicarse con la IA copiloto
- Historial de conversación
- Entrada de texto y botón de envío
- Información sobre capacidades del copiloto

**Dependencias:**
- tkinter (para GUI)
- system_prompt_copiloto (para prompts)
- acciones_copiloto (para acciones permitidas)

### 7. historial.py
**Responsabilidades:**
- Gestión del historial de conversación con Ollama
- Separa el historial de conversación (user/assistant) de los comandos JSON ejecutados
- Limpia el historial tras cada comando no conversacional

**Dependencias:**
- Ninguna (módulo independiente)

### 8. comandos_usuario.py
**Responsabilidades:**
- Permite crear, editar, eliminar y ejecutar comandos sin tocar código
- Funciona en runtime: carga/guarda JSON sin reiniciar

**Dependencias:**
- json, os, webbrowser, subprocess
- nucleo (para ejecutar acciones)

### 9. acciones_copiloto.py
**Responsabilidades:**
- Define qué acciones puede ejecutar la IA copiloto de forma segura
- Actúa como "whitelist" de funciones que el copiloto puede llamar

**Dependencias:**
- logging, typing
- comandos_usuario (para acciones de comandos)

### 10. system_prompt_copiloto.py
**Responsabilidades:**
- Define la personalidad y capacidades del IA copiloto
- Genera prompts dinámicos basados en el contexto del proyecto

**Dependencias:**
- indexador_proyecto (para contexto del proyecto)
- acciones_copiloto (para acciones disponibles)

### 11. indexador_proyecto.py
**Responsabilidades:**
- Lee archivos .md, estructura, comandos y config del proyecto
- Expone contexto dinámico para que la IA copiloto entienda la arquitectura

**Dependencias:**
- os, json, logging
- nucleo (para cargar config)

## Puntos de Entrada

### 1. asistente.py
- Punto de entrada principal del asistente
- Llama a `main()` que:
  1. Inicia Ollama
  2. Registra función de salida
  3. Inicializa el sistema
  4. Si `mostrar_gui` es true:
     - Crea GUI
     - Inicia asistente en thread separado
     - Muestra GUI
  5. Si `mostrar_gui` es false:
     - Llama directamente a `loop_principal(gui=None)`

### 2. nucleo.py
- Exporta funciones principales:
  - `cargar_config`, `cargar_perfil`, `guardar_config`, `guardar_perfil`
  - `grabar_audio`, `esperar_wakeword`, `transcribir`, `hablar`
  - `consultar_ia`, `ejecutar_accion`, `logger`, `detectar_intencion_basica`

## Flujo Principal de Ejecución

1. **Inicialización** (asistente.py:167-186):
   - Iniciar Ollama
   - Registrar función de salida
   - Inicializar sistema
   - Si GUI: crear GUI y thread de asistente

2. **Loop Principal** (asistente.py:79-166):
   - Saludar y mostrar estado
   - Esperar wakeword (nucleo.esperar_wakeword)
   - Cuando se detecta wakeword:
     - Saludar
     - Grabar audio (nucleo.grabar_audio)
     - Transcribir (nucleo.transcribir)
     - Si hay comando:
       - Consultar IA (nucleo.consultar_ia)
       - Limpiar historial si es comando
       - Ejecutar acción (nucleo.ejecutar_accion)
       - Hablar respuesta (nucleo.hablar)
     - Si no hay comando:
       - Decir "No entendí nada"
   - Repetir

3. **Flujo de IA** (nucleo.consultar_ia):
   - Intentar detección básica primero (nucleo.detectar_intencion_basica)
   - Si no hay coincidencia básica, continuar con flujo de IA:
     - Agregar comando del usuario al historial
     - Si tipo IA es "ollama":
       - Consultar Ollama (nucleo._consultar_ollama)
     - Si tipo IA es "claude":
       - Consultar Claude (nucleo._consultar_claude) - no implementado
     - Si tipo IA es "openai":
       - Consultar OpenAI (nucleo._consultar_openai) - no implementado
     - Procesar respuesta y manejar historial

4. **Ejecución de Acción** (nucleo.ejecutar_accion):
   - Primero buscar en comandos dinámicos del usuario (comandos_usuario.buscar_comando_por_trigger)
   - Si no existe, fallback a comandos core (Python)
   - Cada comando tiene su propia lógica de ejecución

5. **Flujo de GUI**:
   - GUI principal muestra estado, último comando, última respuesta
   - Panel de monitorización muestra logs de actividad
   - Panel de copiloto permite conversación con IA para configuración
   - Ventana de gestor de comandos permite crear/editar/eliminar comandos dinámicos

## Dependencias entre Módulos

### Acoplamiento Alto:
1. **nucleo → comandos/**: nucleo importa directamente de cada comando
2. **asistente → nucleo**: asistente depende fuertemente de funciones de nucleo
3. **nucleo → historial**: nucleo usa historial para gestión de conversación
4. **comandos_usuario → nucleo**: comandos_usuario necesita nucleo para ejecutar acciones

### Acoplamiento Medio:
1. **gui → nucleo**: gui necesita nucleo para configuración
2. **gui_comandos → comandos_usuario**: gui_comandos necesita comandos_usuario para gestión
3. **gui_copiloto → system_prompt_copiloto**: gui_copiloto necesita prompts
4. **gui_copiloto → acciones_copiloto**: gui_copiloto necesita acciones permitidas

### Acoplamiento Bajo:
1. **historial**: módulo independiente, no depende de otros módulos
2. **acciones_copiloto**: depende de comandos_usuario, pero es limitado
3. **indexador_proyecto**: depende de nucleo, pero es para documentación

## Arquitectura Actual: Problemas

### 1. Acoplamiento Excesivo
- **nucleo.py:627-710**: Importa directamente de cada comando
- **asistente.py:15**: Importa nucleo directamente
- **nucleo.consultar_ia:499**: Importa historial directamente

### 2. Crecimiento Orgánico
- **nucleo.py:717-717**: 717 líneas en un solo archivo
- **comandos/musica.py:506**: 506 líneas en un solo archivo
- **gui_comandos.py:407**: 407 líneas en un solo archivo

### 3. Configuración Fragmentada
- **config.json**: Configuración principal
- **perfiles/default.json**: Perfil de usuario
- **comandos_usuario.py**: Almacena comandos en data/comandos_usuario.json

### 4. Sin Separación Clara de Responsabilidades
- **nucleo.py**: Audio, STT, TTS, IA, logging, configuración, wakeword, historial
- **asistente.py**: Loop principal, inicialización, GUI, coordinación
- **comandos/**: Aplicaciones, sistemas, medios, música, YouTube, escritura, conversación

### 5. Pruebas Dentro de los Módulos
- **historial.py:159-247**: Tests unitarios inline
- **comandos/musica.py:421-500**: Tests inline
- **nucleo.py**: No tiene tests (pero hay prueba_whisper.py)

### 6. Documentación Incompleta
- **README.md**: Solo nombre del proyecto
- **ARQUITECTURA.md**: No existe
- **CAMBIOS.md**: No existe
- **EJEMPLOS.md**: No existe

## Arquitectura Deseada (Para Referencia)

### Núcleo
- Responsable únicamente de:
  - ciclo principal
  - eventos
  - despacho de acciones

### Proveedores
- AI Provider (Ollama, OpenAI, Claude)
- Music Provider (Local, YouTube, Spotify Web)
- Browser Provider (detectado, configurado)
- Vision Provider (ninguno, OCR local, OCR nube)

### Servicios
- SpeechService
- AIService
- MusicService
- AppService
- ConfigService
- AutomationService

### Sistema de Acciones
- Mantener la idea actual:
  - acción + parámetro

### Experiencia de Usuario
- Setup Wizard extremadamente corto (máximo 2-3 pantallas)
- Navegador preferido
- Música local o web
- Modo local o híbrido
- Voz activada
- Confirmaciones de seguridad

## Resumen

La arquitectura actual es **funcional pero difícil de escalar** debido a:

1. **Acoplamiento excesivo** entre módulos
2. **Crecimiento orgánico** resultando en archivos grandes
3. **Configuración fragmentada** en múltiples ubicaciones
4. **Sin separación clara de responsabilidades**
5. **Pruebas dentro de módulos**
6. **Documentación incompleta**

La refactorización debe abordar estos problemas mientras preserva toda la funcionalidad existente.