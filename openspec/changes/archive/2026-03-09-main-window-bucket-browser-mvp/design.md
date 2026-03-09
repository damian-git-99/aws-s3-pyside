## Context

Este proyecto utiliza PySide6 para desarrollar una aplicación de escritorio para gestionar buckets S3. Actualmente no existe una interfaz principal para visualizar el contenido del bucket. Necesitamos implementar una ventana principal siguiendo el patrón MVP (Model-View-Presenter) para mantener una arquitectura limpia, testeable y mantenible.

El patrón MVP separa la lógica de presentación (Presenter) de la interfaz de usuario (View) y los datos (Model), permitiendo:
- Testing unitario de la lógica de presentación sin necesidad de instanciar widgets
- Reutilización de componentes
- Facilidad de mantenimiento y modificación de la UI sin afectar la lógica

## Goals / Non-Goals

**Goals:**
- Implementar ventana principal con listado de objetos del bucket usando mocked data
- Diseñar sistema de iconos por tipo de archivo para identificación visual
- Establecer estructura MVP consistent y documentada en AGENTS.md
- Crear diseño visual moderno con tabla de archivos mostrando: Name, Size, Last Modified, Storage Class

**Non-Goals:**
- Integración real con AWS S3 (solo mocked data inicialmente)
- Funcionalidades de upload (archivos o carpetas)
- Funcionalidades de drag-and-drop
- Edición inline de metadatos
- Soporte para múltiples buckets simultáneos
- Funcionalidades de búsqueda y filtrado avanzado
- Preview de archivos

## Decisions

### 1. MVP Architecture Pattern
**Decision**: Usar MVP (Model-View-Presenter) con View pasiva

**Rationale**: 
- El Presenter contiene toda la lógica de presentación y actúa como intermediario entre Model y View
- La View es pasiva (solo muestra datos y reenvía eventos al Presenter)
- Facilita testing unitario ya que los Presenters no dependen de PySide6 widgets
- Permite cambiar la implementación de la View (ej: de QWidget a QML) sin modificar lógica

**Alternatives considered**:
- MVC: Acopla demasiado el Model con la View
- MVVM: Overkill para PySide6, requiere binding framework

### 2. Component Structure
**Decision**: Implementar un componente principal:

**BucketBrowserMainWindow**:
- `BucketBrowserModel`: Gestiona datos del bucket (lista de objetos/folders estáticos)
- `BucketBrowserView`: Widget principal con toolbar y área de contenido
- `BucketBrowserPresenter`: Coordina Model y View

**MVP Framework**:
- Clases base abstractas: `BaseModel`, `BaseView`, `BasePresenter`
- Contratos/interfaces definidos en módulo `mvp/contracts.py`
- Documentación de convenciones en `AGENTS.md`

### 3. File Type Icons
**Decision**: Usar sistema de mapeo por extensión con iconos de fallback

**Rationale**:
- Mapeo simple extensión → icono tipo
- Iconos por categoría: images, documents, code, archives, generic
- Usar iconos del sistema donde sea posible (QFileIconProvider) como fallback

### 4. Toolbar Design
**Decision**: Toolbar simple con botón de refresh

**Rationale**:
- Mostrar datos mock estáticos sin navegación de folders
- Evita complejidad inicial y permite iteración posterior cuando se integre S3 real

## Risks / Trade-offs

**[Risk]** Overhead inicial del patrón MVP
**→ Mitigation**: Documentar claramente en AGENTS.md con ejemplos. Empezar con implementaciones simples antes de añadir complejidad.

**[Risk]** Latencia al listar grandes cantidades de objetos (cuando sea real)
**→ Mitigation**: Arquitectura preparada para paginación. Implementar lazy loading en el Model.

**[Trade-off]** Mocked data limita testing de casos edge reales
**→ Aceptance**: Implementar suite de datos mock variados (carpetas vacías, muchos archivos, nombres especiales).

## Migration Plan

No aplica para este cambio inicial. Para futuras migraciones:

1. Implementar nueva versión de componentes en paralelo
2. Feature flags para alternar entre implementaciones
3. Testing exhaustivo de todos los presenters
4. Deprecación gradual de código antiguo

## Open Questions

- ¿Implementar sistema de notificaciones/toasts para feedback de operaciones?
- ¿Soportar vista de lista vs grid (como explorador de archivos)?
- ¿Cómo manejar la navegación de folders cuando se integre S3 real?
