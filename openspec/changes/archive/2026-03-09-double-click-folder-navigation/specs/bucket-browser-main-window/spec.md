## ADDED Requirements

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
- **THEN** la toolbar contiene los botones en orden: Home | Up | Refresh | Upload
- **AND** los botones Home y Up están correctamente espaciados

### Requirement: Área de breadcrumb en la toolbar
The system SHALL incluir un área en la toolbar para mostrar el breadcrumb de navegación.

#### Scenario: Breadcrumb visible en toolbar
- **WHEN** se muestra la ventana principal
- **THEN** el breadcrumb se muestra en la toolbar
- **AND** está posicionado después de los botones de navegación
- **AND** tiene espacio suficiente para mostrar la ruta completa
