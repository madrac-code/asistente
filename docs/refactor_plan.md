# Plan de Refactorización - MADRAC Asistente

## Resumen Ejecutivo

El proyecto actual es **funcional pero presenta problemas arquitectónicos significativos** que lo hacen difícil de mantener, escalar y extender. Este plan de refactorización clasifica cada archivo según su estado actual y propone acciones específicas para mejorar la arquitectura mientras se preserva toda la funcionalidad.

**Principio Guía:** No modificar lógica, solo reestructurar archivos y dependencias.

## Clasificación de Archivos

### MANTENER TAL CUAL

#### 1. asistente.py
**Motivo:** Punto de entrada principal, flujo de ejecución claro, sin problemas arquitectónicos obvios.
**Riesgo:** Bajo - es el corazón del asistente y funciona correctamente.

#### 2. historial.py
**Motivo:** Módulo independiente, bien diseñado, con tests unitarios inline.
**Riesgo:** Muy bajo - gestión de historial de conversación crítica.

#### 3. config.json
**Motivo:** Configuración centralizada, necesaria para el funcionamiento.
**Riesgo:** Bajo - es la configuración principal.

#### 4. perfiles/default.json
**Motivo:** Perfil de usuario por defecto, necesario para funcionalidad.
**Riesgo:** Bajo - define aplicaciones y preferencias del usuario.

#### 5. requirements.txt
**Motivo:** Lista de dependencias, necesaria para empaquetado.
**Riesgo:** Muy bajo - define dependencias del proyecto.

#### 6. empaquetar.bat
**Motivo:** Script de empaquetado, necesario para distribución.
**Riesgo:** Bajo - script de empaquetado esencial.

#### 7. iniciar.bat
**Motivo:** Script de inicio, necesario para ejecución.
**Riesgo:** Bajo - script de inicio esencial.

#### 8. Jarvis.spec
**Motivo:** Especificación de empaquetado, necesaria para distribución.
**Riesgo:** Bajo - usado por PyInstaller.

### REFACTORIZAR

#### 1. nucleo.py
**Motivo:** Acoplamiento excesivo, crecimiento orgánico (717 líneas), múltiples responsabilidades.
**Acción Propuesta:** Dividir en módulos más pequeños y especializados.
**Riesgo:** Medio - alto acoplamiento con muchos componentes.

#### 2. comandos_usuario.py
**Motivo:** Funcional pero podría ser más modular, alta dependencia de nucleo.
**Acción Propuesta:** Separar concerns (gestión vs ejecución).
**Riesgo:** Medio - usado por GUI y asistente principal.

#### 3. acciones_copiloto.py
**Motivo:** Bien estructurado pero podría ser más extensible.
**Acción Propuesta:** Agregar más acciones permitidas, mejorar organización.
**Riesgo:** Bajo - es la whitelist de seguridad.

#### 4. system_prompt_copiloto.py
**Motivo:** Funcional pero podría ser más dinámico.
**Acción Propuesta:** Mejorar generación de prompts, agregar más contexto.
**Riesgo:** Bajo - usado por panel de copiloto.

#### 5. indexador_proyecto.py
**Motivo:** Funcional pero podría ser más modular.
**Acción Propuesta:** Separar concerns (lectura vs indexación).
**Riesgo:** Bajo - usado por copiloto para contexto.

#### 6. gui.py
**Motivo:** Crecimiento orgánico (80 líneas), múltiples responsabilidades.
**Acción Propuesta:** Dividir en componentes más pequeños.
**Riesgo:** Medio - es la interfaz principal.

#### 7. gui_comandos.py
**Motivo:** Crecimiento orgánico (407 líneas), múltiples responsabilidades.
**Acción Propuesta:** Dividir en componentes más pequeños.
**Riesgo:** Medio - usado por asistente principal.

#### 8. gui_copiloto.py
**Motivo:** Crecimiento orgánico (272 líneas), múltiples responsabilidades.
**Acción Propuesta:** Dividir en componentes más pequeños.
**Riesgo:** Medio - es el panel del copiloto.

### DIVIDIR

#### 1. nucleo.py (Dividir)
**Motivo:** 717 líneas, múltiples responsabilidades (audio, STT, TTS, IA, logging, configuración, wakeword, historial, acciones).
**Archivos Propuestos:**
- `core/audio.py` - Grabación y procesamiento de audio
- `core/transcription.py` - STT con Whisper
- `core/tts.py` - Síntesis de voz
- `core/logging.py` - Sistema de logging
- `core/config.py` - Carga y guardado de configuración
- `core/wakeword.py` - Detección de wakeword
- `core/ia.py` - Consulta a IA y detección de intenciones
- `core/actions.py` - Ejecución de acciones

#### 2. comandos/musica.py (Dividir)
**Motivo:** 506 líneas, múltiples estrategias de reproducción, estado global complejo.
**Archivos Propuestos:**
- `commands/music/player.py` - Lógica de reproducción
- `commands/music/detector.py` - Detección de reproductores
- `commands/music/state.py` - Gestión de estado
- `commands/music/search.py` - Búsqueda de música

#### 3. comandos/apps.py (Dividir)
**Motivo:** 122 líneas, múltiples responsabilidades (abrir, cerrar, aliases).
**Archivos Propuestos:**
- `commands/apps/opener.py` - Lógica de apertura
- `commands/apps/closer.py` - Lógica de cierre
- `commands/apps/alias.py` - Gestión de aliases

#### 4. comandos/sistema.py (Dividir)
**Motivo:** 9 líneas, podría ser más completo.
**Archivos Propuestos:**
- `commands/system/time.py` - Comandos de hora y fecha
- `commands/system/volume.py` - Control de volumen

#### 5. comandos/media.py (Dividir)
**Motivo:** 9 líneas, podría ser más completo.
**Archivos Propuestos:**
- `commands/media/player.py` - Control de reproducción
- `commands/media/track.py` - Control de canciones

#### 6. comandos/youtube.py (Dividir)
**Motivo:** 9 líneas, podría ser más completo.
**Archivos Propuestos:**
- `commands/youtube/search.py` - Búsqueda
- `commands/youtube/player.py` - Control de reproductor

### MOVER

#### 1. prueba_whisper.py (Mover)
**Motivo:** Archivo de prueba, debería estar en tests/.
**Nuevo Ubicación:** `tests/whisper/`
**Razón:** Separar tests de producción de código.

#### 2. pruebas_intenciones.py (Mover)
**Motivo:** Archivo de prueba, debería estar en tests/.
**Nuevo Ubicación:** `tests/intentions/`
**Razón:** Separar tests de producción de código.

#### 3. test_whisper.py (Mover)
**Motivo:** Archivo de prueba, debería estar en tests/.
**Nuevo Ubicación:** `tests/whisper/`
**Razón:** Separar tests de producción de código.

#### 4. tests_historial.py (Mover)
**Motivo:** Archivo de prueba, debería estar en tests/.
**Nuevo Ubicación:** `tests/history/`
**Razón:** Separar tests de producción de código.

#### 5. build/ (Mover)
**Motivo:** Build artifacts, debería estar en artifacts/ o eliminar.
**Nuevo Ubicación:** `artifacts/build/`
**Razón:** Separar artifacts de código.

#### 6. dist/ (Mover)
**Motivo:** Distribuibles, debería estar en artifacts/ o eliminar.
**Nuevo Ubicación:** `artifacts/dist/`
**Razón:** Separar artifacts de código.

#### 7. logs/ (Mover)
**Motivo:** Logs, debería estar en artifacts/ o eliminar.
**Nuevo Ubicación:** `artifacts/logs/`
**Razón:** Separar artifacts de código.

#### 8. data/ (Mover)
**Motivo:** Datos del usuario, debería estar en storage/.
**Nuevo Ubicación:** `storage/user_data/`
**Razón:** Separar datos de usuario de código.

#### 9. venv/ (Mover)
**Motivo:** Entorno virtual, debería estar en env/.
**Nuevo Ubicación:** `env/`
**Razón:** Convencional para entornos virtuales.

#### 10. __pycache__/ (Mover)
**Motivo:** Cache de Python, debería estar en cache/.
**Nuevo Ubicación:** `cache/`
**Razón:** Convencional para cache de Python.

### ELIMINAR

#### 1. Ninguno
**Nota:** No hay archivos que eliminar en esta fase.
**Razón:** Todos los archivos tienen funcionalidad necesaria.

## Archivos Críticos (No Tocar Inicialmente)

### 1. asistente.py
**Razón:** Punto de entrada principal, flujo de ejecución.
**Protección:** No modificar hasta refactorizar nucleo y comandos.

### 2. historial.py
**Razón:** Gestión de historial de conversación crítica.
**Protección:** No modificar hasta refactorizar GUI y copiloto.

### 3. config.json
**Razón:** Configuración centralizada.
**Protección:** No modificar hasta refactorizar config_service.

### 4. perfiles/default.json
**Razón:** Perfil de usuario por defecto.
**Protección:** No modificar hasta refactorizar perfiles.

## Módulos Más Acoplados

### 1. nucleo.py
**Acoplamiento:**
- **comandos/**: Importa directamente de cada comando
- **asistente.py**: Dependencia fuerte
- **historial.py**: Usa para gestión de conversación

**Impacto:** Alto - es el centro del sistema.

### 2. asistente.py
**Acoplamiento:**
- **nucleo.py**: Dependencia fuerte
- **gui.py**: Dependencia fuerte
- **historial.py**: Dependencia fuerte

**Impacto:** Medio - es el orquestador principal.

### 3. comandos_usuario.py
**Acoplamiento:**
- **nucleo.py**: Necesita para ejecutar acciones
- **gui_comandos.py**: Dependencia fuerte

**Impacto:** Medio - usado por GUI y asistente.

### 4. gui.py
**Acoplamiento:**
- **nucleo.py**: Necesita para configuración
- **asistente.py**: Dependencia fuerte

**Impacto:** Medio - es la interfaz principal.

## Deuda Técnica

### 1. Acoplamiento Excesivo
**Ubicación:** nucleo.py, asistente.py, comandos/
**Impacto:** Alto - difícil de probar, mantener y extender.
**Solución:** Separar concerns, reducir dependencias cruzadas.

### 2. Crecimiento Orgánico
**Ubicación:** nucleo.py (717 líneas), gui_comandos.py (407 líneas)
**Impacto:** Medio-Alto - archivos grandes difíciles de mantener.
**Solución:** Dividir en módulos más pequeños.

### 3. Configuración Fragmentada
**Ubicación:** config.json, perfiles/default.json, comandos_usuario.json
**Impacto:** Medio - múltiples ubicaciones de configuración.
**Solución:** Centralizar en config_service.

### 4. Pruebas Dentro de Módulos
**Ubicación:** historial.py, comandos/musica.py
**Impacto:** Bajo - mezcla de código y tests.
**Solución:** Mover tests a tests/.

### 5. Documentación Incompleta
**Ubicación:** README.md, falta archivos de documentación
**Impacto:** Bajo - afecta onboarding pero no funcionalidad.
**Solución:** Agregar documentación completa.

## Orden de Refactorización (Minimizar Riesgo)

### Fase 1: Foundation (Semanas 1-2)
1. **Mover archivos de tests** a tests/
2. **Mover artifacts** a artifacts/
3. **Mover datos de usuario** a storage/
4. **Mover cache** a cache/
5. **Crear estructura de tests/**

**Razón:** Bajo riesgo, prepara estructura para refactorización.

### Fase 2: Separar Concerns (Semanas 3-4)
1. **Dividir nucleo.py** en módulos especializados
2. **Separar comandos_usuario.py** (gestión vs ejecución)
3. **Dividir gui.py** en componentes
4. **Dividir gui_comandos.py** en componentes
5. **Dividir gui_copiloto.py** en componentes

**Razón:** Aborda los problemas arquitectónicos más críticos.

### Fase 3: Refactorizar (Semanas 5-6)
1. **Refactorizar nucleo.py** dividido
2. **Refactorizar comandos_usuario.py**
3. **Refactorizar acciones_copiloto.py**
4. **Refactorizar system_prompt_copiloto.py**
5. **Refactorizar indexador_proyecto.py**

**Razón:** Mejorar módulos existentes después de dividir.

### Fase 4: Completar (Semanas 7-8)
1. **Dividir comandos/musica.py**
2. **Dividir comandos/apps.py**
3. **Dividir comandos/sistema.py**
4. **Dividir comandos/media.py**
5. **Dividir comandos/youtube.py**

**Razón:** Completar división de comandos.

### Fase 5: Verificar (Semana 9)
1. **Probar toda la funcionalidad**
2. **Verificar que nada se rompió**
3. **Actualizar documentación**
4. **Limpiar artifacts temporales**

**Razón:** Asegurar que todo funciona después de refactorización.

## Riesgo y Consideraciones

### Riesgos Altos:
1. **Cambiar asistente.py**: Punto de entrada principal
2. **Cambiar historial.py**: Gestión de historial crítica
3. **Cambiar config.json**: Configuración centralizada

### Riesgos Medios:
1. **Cambiar nucleo.py**: Alto acoplamiento
2. **Cambiar comandos/**: Múltiples comandos
3. **Cambiar gui.py**: Interfaz principal

### Riesgos Bajos:
1. **Cambiar comandos_usuario.py**: Funcional pero mejorable
2. **Cambiar acciones_copiloto.py**: Whitelist de seguridad
3. **Cambiar system_prompt_copiloto.py**: Prompts del copiloto

## Conclusión

Este plan de refactorización aborda los problemas arquitectónicos del proyecto actual mientras preserva toda la funcionalidad. El enfoque por fases minimiza el riesgo y asegura que cada paso esté bien probado.

**Principio Clave:** No modificar lógica, solo reestructurar archivos y dependencias.

**Resultado Esperado:** Arquitectura más mantenible, escalable y extensible con separación clara de responsabilidades.