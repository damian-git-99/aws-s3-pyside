## Context

La aplicación utiliza el patrón MVP con PySide6. Actualmente no existe ningún mecanismo de persistencia de configuraciones. El usuario necesita gestionar variables de entorno y preferencias que deben sobrevivir entre sesiones. Para builds de PyInstaller, la configuración debe almacenarse en una ubicación accesible (directorio de datos de usuario) en lugar de empaquetarse en el ejecutable.

## Goals / Non-Goals

**Goals:**
- Implementar sistema de configuración persistente usando SQLite
- Crear diálogo de primera configuración que se muestre automáticamente al iniciar sin config
- Agregar botón de configuración en el toolbar principal
- Implementar panel de edición de configuraciones con validación
- Asegurar compatibilidad con PyInstaller (datos fuera del bundle)
- Seguir el patrón MVP: ConfigManager (Model), SettingsDialog/Panel (View), ConfigPresenter (Presenter)

**Non-Goals:**
- Soporte para múltiples perfiles de usuario
- Sincronización en red o cloud
- Encriptación de configuraciones (por ahora)
- Soporte para archivos de configuración externos (YAML/JSON)

## Decisions

### 1. SQLite como backend de persistencia
- **Rationale**: SQLite está incluido en Python estándar, no requiere instalación adicional, es portable, y funciona perfectamente con PyInstaller (archivo único .db)
- **Alternativas consideradas**: 
  - JSON files: Más simple pero sin tipos estrictos ni queries
  - QSettings: Específico de Qt, menos flexible para estructuras complejas

### 2. Ubicación del archivo de configuración
- **Rationale**: Usar directorio de datos de usuario según el OS (`~/.appname/` en Linux/Mac, `%APPDATA%/appname/` en Windows)
- **PyInstaller**: En builds, detectar si estamos en un bundle y usar directorio de datos del usuario en lugar de directorio temporal

### 3. Estructura de tablas
- **Rationale**: Tabla simple key-value con timestamps para auditoría
- **Esquema**:
  ```sql
  CREATE TABLE settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

### 4. Arquitectura MVP
- **Model (ConfigManager)**: Acceso a SQLite, CRUD de settings, emite señales Qt
- **View (SettingsDialog/SettingsPanel)**: UI de configuración, inputs validados
- **Presenter (ConfigPresenter)**: Coordina entre model y view, lógica de negocio

### 5. Detección de primera vez
- **Rationale**: Verificar existencia de archivo SQLite al inicio
- **Implementación**: En main.py, antes de mostrar ventana principal, verificar si existe config. Si no, mostrar SetupWizard antes de lanzar app principal

## Risks / Trade-offs

- **[Risk]** SQLite en PyInstaller puede tener problemas de paths → **Mitigation**: Usar `sys._MEIPASS` check y crear directorio de datos en ubicación persistente
- **[Risk]** Cambios en estructura de settings en futuras versiones → **Mitigation**: Implementar versionado de schema en tabla `__meta__`
- **[Risk]** Concurrency si múltiples instancias de la app → **Mitigation**: SQLite maneja locking automáticamente, pero considerar singleton pattern si es necesario
- **[Trade-off]** Simplicidad vs Features: SQLite es simple pero no escala a configuraciones complejas jerárquicas

## Migration Plan

1. Implementar módulo `src/config/` con ConfigManager
2. Crear vistas SettingsDialog y SettingsPanel  
3. Crear ConfigPresenter
4. Modificar main.py para detectar primera vez y mostrar SetupWizard
5. Agregar botón de configuración al toolbar
6. Testear en modo desarrollo
7. Testear build de PyInstaller para verificar persistencia

## Open Questions

- ¿Qué variables de entorno específicas son requeridas para esta app? (Necesito contexto del proyecto)
- ¿Hay preferencias adicionales que deban persistirse además de env vars?
