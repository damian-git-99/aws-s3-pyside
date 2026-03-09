## Why

El bucket browser actual muestra todos los objetos del bucket en una lista plana en el nivel raíz. Los usuarios necesitan poder navegar dentro de los folders para ver su contenido de manera jerárquica, similar a un explorador de archivos tradicional. Esta funcionalidad es esencial para buckets con estructuras de directorios profundas.

## What Changes

- Agregar detección de doble-click en la tabla de objetos
- Identificar si el objeto clickeado es un folder (termina en `/`)
- Al hacer doble-click en un folder:
  - Navegar dentro del folder y mostrar su contenido
  - Actualizar el título de la ventana para mostrar la ruta actual
  - Mostrar breadcrumb de navegación (ruta actual)
- Agregar botón "Back" o "Up" para volver al directorio padre
- Agregar botón "Home" para volver al directorio raíz
- Mantener el estado de paginación por cada nivel de directorio

## Capabilities

### New Capabilities
- `folder-navigation-double-click`: Navegación hacia adentro de folders mediante doble-click
- `breadcrumb-navigation`: Visualización y navegación por breadcrumb de la ruta actual
- `navigation-back-home`: Botones para volver al directorio padre y al directorio raíz

### Modified Capabilities
- `s3-file-service`: El servicio ya soporta `prefix`, se usará para navegación (no requiere cambios en requirements)
- `bucket-browser-main-window`: Se agregará interacción de doble-click y controles de navegación

## Impact

- **src/views/bucket_browser_view.py**: Agregar eventos de doble-click, breadcrumb, botones de navegación
- **src/presenters/bucket_browser_presenter.py**: Manejar navegación, mantener estado de ruta actual
- **src/services/s3_service.py**: No requiere cambios (ya soporta prefix)
- **src/models/bucket_object.py**: No requiere cambios
- **Interfaz de usuario**: Nueva toolbar con breadcrumb y botones de navegación
