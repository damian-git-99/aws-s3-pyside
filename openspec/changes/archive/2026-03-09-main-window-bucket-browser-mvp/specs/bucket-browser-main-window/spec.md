## ADDED Requirements

### Requirement: Ventana principal muestra lista de objetos del bucket
The system SHALL mostrar una ventana principal que liste todos los folders y objetos del bucket actual en una tabla con las columnas: Name, Size, Last Modified, Storage Class.

#### Scenario: Ventana principal se carga exitosamente
- **WHEN** el usuario abre la aplicación
- **THEN** se muestra la ventana principal del bucket browser
- **AND** la tabla contiene las columnas: Name, Size, Last Modified, Storage Class

#### Scenario: Lista de objetos se muestra correctamente
- **WHEN** el sistema carga los datos del bucket (mocked)
- **THEN** la tabla muestra cada objeto con: nombre, tamaño formateado, fecha de última modificación, clase de almacenamiento
- **AND** los folders se muestran antes que los archivos

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


