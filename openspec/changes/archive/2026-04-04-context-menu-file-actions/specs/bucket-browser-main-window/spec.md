# bucket-browser-main-window Specification

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Toolbar incluye acciones de archivo
**Reason**: File actions (Delete, Download, Preview, Generate Link) moved to context menu. See context-menu-file-actions capability.
**Migration**: Use right-click context menu on file table for these actions.
