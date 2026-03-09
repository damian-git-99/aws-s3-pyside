# mvp-architecture-framework Specification

## Purpose
TBD - created by archiving change main-window-bucket-browser-mvp. Update Purpose after archive.
## Requirements
### Requirement: Estructura base de MVP
The system SHALL implementar clases base abstractas para el patrón MVP que definan los contratos entre Model, View y Presenter.

#### Scenario: Clases base existen
- **WHEN** se desarrolla un nuevo componente
- **THEN** existen las clases base: `BaseModel`, `BaseView`, `BasePresenter`
- **AND** cada clase base define los métodos y señales comunes requeridos

#### Scenario: Contratos definidos
- **WHEN** se implementa un componente MVP
- **THEN** las interfaces/contratos están definidos en `mvp/contracts.py`
- **AND** cada componente implementa su contrato correspondiente

### Requirement: Model responsabilidades
The system SHALL definir que los Models son responsables de gestionar datos y lógica de negocio, sin conocimiento de la UI.

#### Scenario: Model no depende de View
- **WHEN** se implementa un Model
- **THEN** el Model NO importa ni referencia ninguna clase de View
- **AND** el Model NO contiene código específico de PySide6 widgets

#### Scenario: Model notifica cambios
- **WHEN** los datos del Model cambian
- **THEN** el Model emite señales (usando patron observer) para notificar cambios
- **AND** el Presenter se suscribe a estas señales

#### Scenario: Model contiene lógica de negocio
- **WHEN** se requiere validar o transformar datos
- **THEN** la lógica reside en el Model, no en el Presenter ni View

### Requirement: View responsabilidades
The system SHALL definir que las Views son pasivas, responsables solo de mostrar datos y capturar eventos de usuario.

#### Scenario: View no tiene lógica de negocio
- **WHEN** se implementa una View
- **THEN** la View NO contiene lógica de negocio o validaciones
- **AND** la View delega todas las decisiones al Presenter

#### Scenario: View notifica eventos
- **WHEN** ocurre un evento de usuario (click, selección, etc.)
- **THEN** la View llama al método correspondiente del Presenter
- **AND** la View NO realiza acciones directas

#### Scenario: View expone métodos de display
- **WHEN** el Presenter necesita actualizar la UI
- **THEN** la View expone métodos públicos simples (ej: `set_items()`, `show_error()`)
- **AND** estos métodos solo actualizan widgets, no toman decisiones

### Requirement: Presenter responsabilidades
The system SHALL definir que los Presenters actúan como intermediarios entre Model y View, conteniendo la lógica de presentación.

#### Scenario: Presenter orquesta Model y View
- **WHEN** se implementa un Presenter
- **THEN** el Presenter recibe instancias de Model y View en su constructor
- **AND** el Presenter coordina la comunicación entre ambos

#### Scenario: Presenter maneja eventos de usuario
- **WHEN** la View notifica un evento de usuario
- **THEN** el Presenter decide qué acción tomar
- **AND** el Presenter actualiza el Model y/o la View según corresponda

#### Scenario: Presenter reacciona a cambios del Model
- **WHEN** el Model notifica un cambio de datos
- **THEN** el Presenter recibe la notificación
- **AND** el Presenter actualiza la View con los nuevos datos

### Requirement: Convenciones de nomenclatura
The system SHALL establecer convenciones de nomenclatura consistentes para componentes MVP.

#### Scenario: Nomenclatura de archivos
- **WHEN** se crean archivos de un componente
- **THEN** siguen el patrón:
  - `models/<name>_model.py` para Models
  - `views/<name>_view.py` para Views
  - `presenters/<name>_presenter.py` para Presenters

#### Scenario: Nomenclatura de clases
- **WHEN** se nombran clases
- **THEN** siguen el patrón:
  - `<Name>Model` para Models (ej: `BucketBrowserModel`)
  - `<Name>View` para Views (ej: `BucketBrowserView`)
  - `<Name>Presenter` para Presenters (ej: `BucketBrowserPresenter`)

### Requirement: Testing de Presenters
The system SHALL permitir testing unitario de Presenters sin instanciar widgets de PySide6.

#### Scenario: Presenter testeable sin View real
- **WHEN** se escriben tests para un Presenter
- **THEN** se puede usar un Mock/Stub de la View
- **AND** el Presenter funciona correctamente con el mock

#### Scenario: Tests unitarios independientes
- **WHEN** se ejecutan tests de Presenters
- **THEN** no se requiere QApplication ni event loop de Qt
- **AND** los tests corren rápidamente sin overhead de GUI

### Requirement: Documentación AGENTS.md
The system SHALL incluir documentación en AGENTS.md que explique el patrón MVP y las convenciones para futuros desarrollos.

#### Scenario: AGENTS.md existe
- **WHEN** un desarrollador consulta cómo implementar MVP
- **THEN** existe un archivo `AGENTS.md` en la raíz del proyecto
- **AND** contiene explicación del patrón MVP usado

#### Scenario: AGENTS.md tiene ejemplos
- **WHEN** se lee AGENTS.md
- **THEN** incluye ejemplos de código de un componente completo (Model, View, Presenter)
- **AND** explica las responsabilidades de cada parte
- **AND** documenta las convenciones de nomenclatura

