# header-refactor Specification

## Purpose
Define the requirements for refactoring the header component to use a two-row vertical layout, separating the breadcrumb navigation from action buttons.

## Requirements

### Requirement: Layout de dos filas en header
El header DEBE usar un layout vertical de dos filas para separar breadcrumb y botones.

#### Scenario: Estructura de dos filas
- **WHEN** se renderiza el componente header
- **THEN** la primera fila contiene únicamente el breadcrumb
- **AND** la segunda fila contiene únicamente los botones de acción

### Requirement: Breadcrumb en fila superior
El breadcrumb DEBE estar posicionado en la fila superior del header.

#### Scenario: Posición del breadcrumb
- **WHEN** se visualiza el header
- **THEN** el breadcrumb aparece en la parte superior
- **AND** los botones aparecen debajo del breadcrumb

### Requirement: Mantener funcionalidad existente
El header DEBE mantener toda la funcionalidad actual después del refactor.

#### Scenario: Botones funcionales después del cambio
- **WHEN** el usuario hace clic en un botón del header
- **THEN** el botón responde normalmente
- **AND** el evento se propaga correctamente al presenter

#### Scenario: Actualización del breadcrumb
- **WHEN** cambia la navegación
- **THEN** el breadcrumb se actualiza correctamente en su nueva posición
- **AND** no afecta la disposición de los botones
