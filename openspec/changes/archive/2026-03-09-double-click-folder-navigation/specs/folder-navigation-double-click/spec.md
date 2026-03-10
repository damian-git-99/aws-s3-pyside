## ADDED Requirements

### Requirement: Double-click en folder navega al contenido del folder
The system SHALL detectar cuando el usuario hace doble-click en una fila que representa un folder y navegar al contenido de ese folder.

#### Scenario: Usuario hace doble-click en un folder
- **WHEN** el usuario hace doble-click en una fila que representa un folder (termina en `/`)
- **THEN** el sistema detecta que es un folder
- **AND** carga el contenido del folder usando el prefijo correspondiente
- **AND** actualiza la vista para mostrar solo los objetos dentro de ese folder
- **AND** actualiza el breadcrumb para mostrar la nueva ruta

#### Scenario: Usuario hace doble-click en un archivo
- **WHEN** el usuario hace doble-click en una fila que representa un archivo (no termina en `/`)
- **THEN** no ocurre ninguna navegación
- **AND** el archivo no reacciona al doble-click (por ahora)

#### Scenario: Doble-click en folder vacío
- **WHEN** el usuario hace doble-click en un folder vacío
- **THEN** se navega al folder
- **AND** se muestra el estado vacío "No files uploaded yet"
