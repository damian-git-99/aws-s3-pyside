## Why

Necesitamos una ventana principal para navegar y gestionar el contenido del bucket S3. Actualmente no existe una interfaz visual para visualizar folders y objetos. Esta interfaz proporcionará una vista de explorador de archivos moderna y familiar para navegar el contenido del bucket.

## What Changes

- **Nueva ventana principal** con lista de folders y objetos del bucket
- **Sistema de listado** con columnas: Name, Size, Last Modified, Storage Class
- **Iconos por tipo de archivo** para identificación visual rápida
- **Toolbar básica** con acción de refresh
- **Patrón MVP (Model-View-Presenter)** para toda la arquitectura de la UI
- **Datos mock** para desarrollo y testing inicial
- **Documentación AGENTS.md** estableciendo convenciones MVP para futuras implementaciones

## Capabilities

### New Capabilities

- `bucket-browser-main-window`: Ventana principal del explorador de bucket con listado de objetos y folders, incluyendo toolbar básica y área de contenido con tabla de archivos
- `mvp-architecture-framework`: Framework de arquitectura MVP definiendo estructura de Modelos, Vistas y Presenters, y convenciones para su implementación consistente

### Modified Capabilities

<!-- No hay capabilities existentes que modificar -->

## Impact

- **Nuevos módulos**: Models, Views, Presenters para el bucket browser
- **UI Framework**: PySide6 para widgets y manejo de eventos
- **Patrón arquitectónico**: MVP pattern en toda la capa de presentación
- **Assets**: Iconos para diferentes tipos de archivo (images, documents, code, etc.)
- **Tests**: Unit tests para Presenters y Models
