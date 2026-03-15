## ADDED Requirements

### Requirement: Breadcrumb en espacio dedicado
El breadcrumb DEBE ocupar su propia fila/barra separada de los botones de acción.

#### Scenario: Visualización con navegación profunda
- **WHEN** el usuario navega a una ruta con múltiples niveles
- **THEN** el breadcrumb se muestra en una fila completa sin compartir espacio con botones

#### Scenario: El breadcrumb utiliza ancho completo
- **WHEN** se renderiza el breadcrumb
- **THEN** tiene acceso al 100% del ancho disponible del header

### Requirement: Sin truncamiento del breadcrumb
El breadcrumb NO DEBE truncarse o comprimirse por falta de espacio horizontal.

#### Scenario: Ruta larga visible completa
- **WHEN** el breadcrumb contiene texto que excede el ancho disponible
- **THEN** el texto se muestra completo o con scroll horizontal si es necesario
- **AND** los botones mantienen su tamaño y posición
