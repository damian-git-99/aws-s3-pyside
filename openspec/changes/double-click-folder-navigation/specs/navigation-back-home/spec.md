## ADDED Requirements

### Requirement: Botón para volver al directorio padre
The system SHALL incluir un botón "Up" o "Back" que permita al usuario volver al directorio padre.

#### Scenario: Botón Up navega al directorio padre
- **WHEN** el usuario está en un subdirectorio (no raíz)
- **AND** hace click en el botón "Up"
- **THEN** el sistema navega al directorio padre
- **AND** actualiza la vista con el contenido del directorio padre
- **AND** actualiza el breadcrumb

#### Scenario: Botón Up deshabilitado en directorio raíz
- **WHEN** el usuario está en el directorio raíz del bucket
- **THEN** el botón "Up" está deshabilitado (grisado)
- **AND** no responde a clicks

### Requirement: Botón para volver al directorio raíz
The system SHALL incluir un botón "Home" que permita al usuario volver directamente al directorio raíz desde cualquier nivel.

#### Scenario: Botón Home navega a directorio raíz
- **WHEN** el usuario está en cualquier subdirectorio
- **AND** hace click en el botón "Home"
- **THEN** el sistema navega al directorio raíz del bucket
- **AND** actualiza la vista con el contenido raíz
- **AND** actualiza el breadcrumb para mostrar solo el bucket

#### Scenario: Botón Home deshabilitado en directorio raíz
- **WHEN** el usuario está en el directorio raíz del bucket
- **THEN** el botón "Home" está deshabilitado
- **AND** se vuelve a habilitar cuando se navega a un subdirectorio
