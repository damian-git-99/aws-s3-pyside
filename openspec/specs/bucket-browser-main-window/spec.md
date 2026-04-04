# bucket-browser-main-window Specification

## Purpose
TBD - created by archiving change main-window-bucket-browser-mvp. Update Purpose after archive.
## Requirements
### Requirement: Ventana principal muestra lista de objetos del bucket
The system SHALL mostrar una ventana principal que liste todos los folders y objetos del bucket actual en una tabla con las columnas: Name, Size, Last Modified, Storage Class.

#### Scenario: Ventana principal se carga exitosamente
- **WHEN** el usuario abre la aplicación
- **THEN** se muestra la ventana principal del bucket browser
- **AND** la tabla contiene las columnas: Name, Size, Last Modified, Storage Class

#### Scenario: Lista de objetos se muestra correctamente
- **WHEN** el sistema carga los datos del bucket desde S3 (no mocked)
- **THEN** la tabla muestra cada objeto con: nombre, tamaño formateado, fecha de última modificación, clase de almacenamiento
- **AND** los folders se muestran antes que los archivos
- **AND** los datos provienen de la API real de AWS S3

#### Scenario: Loading state is shown during S3 operations
- **WHEN** los datos se están cargando desde S3
- **THEN** se muestra un indicador de carga (spinner o texto "Loading...")
- **AND** la tabla está deshabilitada temporalmente

#### Scenario: Error state is displayed for S3 errors
- **WHEN** ocurre un error de S3 (acceso denegado, bucket no encontrado, etc.)
- **THEN** se muestra un mensaje de error amigable en la ventana
- **AND** se incluye una acción para reintentar

### Requirement: Iconos por tipo de archivo
The system SHALL mostrar un icono apropiado junto al nombre de cada archivo basado en su extensión o tipo MIME.

#### Scenario: Archivos tienen iconos según su tipo
- **WHEN** la lista de archivos se renderiza
- **THEN** cada archivo muestra un icono específico según su tipo:
  - Imágenes (.jpg, .png, .gif) → icono de imagen
  - Documentos (.pdf, .doc, .txt) → icono de documento
  - Código (.py, .js, .html) → icono de código
  - Archivos comprimidos (.zip, .tar) → icono de archivo
  - Otros tipos → icono genérico

#### Scenario: Folders tienen icono de carpeta
- **WHEN** la lista incluye folders
- **THEN** cada folder muestra un icono de carpeta

### Requirement: Toolbar básica
The system SHALL incluir una toolbar con acciones básicas.

#### Scenario: Toolbar es visible
- **WHEN** se muestra la ventana principal
- **THEN** hay una toolbar en la parte superior
- **AND** contiene un botón "Refresh" para actualizar la lista
- **AND** contiene un botón "Upload" (sin funcionalidad por ahora)

### Requirement: Tabla soporta doble-click para navegación
The system SHALL detectar eventos de doble-click en la tabla de objetos y reenviarlos al presenter para manejo de navegación.

#### Scenario: Tabla detecta doble-click y notifica al presenter
- **WHEN** el usuario hace doble-click en una fila de la tabla
- **THEN** la view detecta el evento
- **AND** identifica el objeto correspondiente a esa fila
- **AND** llama al método del presenter `on_item_double_clicked(object_name, is_folder)`

### Requirement: Toolbar incluye controles de navegación
The system SHALL actualizar la toolbar para incluir botones de navegación junto a los botones existentes.

#### Scenario: Toolbar muestra controles de navegación
- **WHEN** se muestra la ventana principal
- **THEN** la toolbar contiene los botones en orden: Home | Up | Refresh | Create Folder | Upload
- **AND** los botones Home y Up están correctamente espaciados

### Requirement: Toolbar tiene botones de acción de archivo
**Reason**: Moved to context menu via context-menu-file-actions capability
**Migration**: Use right-click context menu on file table

The system SHALL include file action buttons in the toolbar (Delete, Download, Preview, Generate Link).

#### Scenario: Toolbar muestra botones de acción de archivo
- **WHEN** se muestra la ventana principal
- **THEN** la toolbar contiene botones: Delete | Download | Preview | Generate Link
- **AND** los botones están posicionados después de Upload

### Requirement: Toolbar incluye acciones de archivo
**Reason**: File actions (Delete, Download, Preview, Generate Link) moved to context menu. See context-menu-file-actions capability.
**Migration**: Use right-click context menu on file table for these actions.

### Requirement: Área de breadcrumb en la toolbar
The system SHALL incluir un área en la toolbar para mostrar el breadcrumb de navegación.

#### Scenario: Breadcrumb visible en toolbar
- **WHEN** se muestra la ventana principal
- **THEN** el breadcrumb se muestra en la toolbar
- **AND** está posicionado después de los botones de navegación
- **AND** tiene espacio suficiente para mostrar la ruta completa

