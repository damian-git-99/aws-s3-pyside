## ADDED Requirements

### Requirement: Visualización de breadcrumb de navegación
The system SHALL mostrar un breadcrumb en la parte superior de la tabla que indique la ruta actual dentro del bucket.

#### Scenario: Breadcrumb muestra ruta actual
- **WHEN** el usuario navega a un folder específico
- **THEN** el breadcrumb muestra la ruta completa: Bucket > folder1 > folder2 > ...
- **AND** cada segmento del breadcrumb es clickeable para navegar a ese nivel

#### Scenario: Breadcrumb en directorio raíz
- **WHEN** la aplicación muestra el contenido del directorio raíz
- **THEN** el breadcrumb muestra solo el nombre del bucket
- **AND** no hay segmentos adicionales

#### Scenario: Breadcrumb se actualiza al navegar
- **WHEN** el usuario navega hacia adentro de un folder mediante doble-click
- **THEN** el breadcrumb se actualiza para incluir el nuevo folder
- **AND** el nuevo segmento se agrega al final

#### Scenario: Navegación mediante breadcrumb
- **WHEN** el usuario hace click en un segmento intermedio del breadcrumb
- **THEN** el sistema navega a ese nivel del directorio
- **AND** se eliminan los segmentos posteriores del breadcrumb
