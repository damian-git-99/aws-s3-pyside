## Why

La aplicación necesita una forma de gestionar configuraciones persistentes entre sesiones. Actualmente, no hay mecanismo para guardar preferencias del usuario o variables de entorno requeridas, lo que obliga a reconfigurar en cada inicio. Se requiere un sistema de configuración con persistencia en SQLite que funcione tanto en desarrollo como en builds de PyInstaller.

## What Changes

- **Nuevo módulo `src/config/`**: Gestión de configuración usando SQLite como backend
- **Diálogo de primera vez**: Al iniciar sin configuración, mostrar diálogo para ingresar variables de entorno requeridas
- **Botón de configuración en toolbar**: Acceso rápido a las settings desde la UI principal
- **Panel de configuración**: Interfaz para editar y gestionar todas las configuraciones
- **Integración con PyInstaller**: El archivo SQLite debe persistirse correctamente en builds empaquetados
- **Patrón MVP**: ConfigManager (Model), SettingsDialog/Panel (View), ConfigPresenter (Presenter)

## Capabilities

### New Capabilities
- `settings-management`: Gestión completa de configuraciones persistentes con SQLite, incluyendo CRUD de settings, diálogo de primera configuración, y panel de edición

### Modified Capabilities
<!-- Sin capacidades existentes modificadas - es una funcionalidad completamente nueva -->

## Impact

- **Nueva dependencia**: `sqlite3` (módulo estándar de Python)
- **Nuevo directorio**: `src/config/` con modelo, vistas y presenter
- **Modificaciones en `src/main.py`**: Lógica de inicio para detectar primera vez
- **Modificaciones en toolbar**: Agregar botón de configuración
- **PyInstaller**: Configuración adicional para incluir directorio de datos de usuario
