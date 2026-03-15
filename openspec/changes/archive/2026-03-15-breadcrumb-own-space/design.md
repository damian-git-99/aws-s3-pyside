## Context

Actualmente el breadcrumb y los botones de acción están en la misma fila/área del header. Con navegación profunda, el breadcrumb ocupa mucho espacio horizontal comprimiendo los botones o requiriendo truncamiento del texto. La arquitectura MVP del proyecto requiere que los cambios se mantengan en la capa View sin afectar la lógica de negocio del Presenter ni el Modelo.

## Goals / Non-Goals

**Goals:**
- Separar visualmente el breadcrumb de los botones de acción
- Proveer espacio ilimitado horizontal para el breadcrumb
- Mantener la posición y funcionalidad actual de los botones
- Mejorar la legibilidad y usabilidad del breadcrumb en navegación profunda
- Mantener compatibilidad con la arquitectura MVP existente

**Non-Goals:**
- Cambiar la lógica de negocio o el modelo de datos
- Modificar el comportamiento de los botones
- Cambiar el estilo visual del breadcrumb (solo su posición)
- Agregar nuevas funcionalidades al breadcrumb

## Decisions

**1. Layout de dos filas en el header**
- **Decision**: Usar un layout vertical con dos filas en lugar de horizontal
- **Rationale**: Es la solución más simple y directa que separa claramente ambos elementos
- **Alternatives consideradas**: 
  - Dropdown para breadcrumb (agrega clicks, menos visible)
  - Botones flotantes (rompe la estructura MVP, más complejo)

**2. Breadcrumb en primera fila, botones en segunda**
- **Decision**: Colocar el breadcrumb arriba y los botones debajo
- **Rationale**: El breadcrumb representa la navegación/ubicación actual (contexto), los botones son acciones sobre ese contexto. Es un patrón común en UIs modernas.

**3. Usar QVBoxLayout para el header**
- **Decision**: Cambiar el layout del header a vertical con QVBoxLayout
- **Rationale**: Qt nativo, compatible con PySide6, permite expansión automática
- **Impacto**: Mínimo, solo cambio de layout manager

**4. Mantener separación de concerns MVP**
- **Decision**: El cambio se limita a la capa View
- **Rationale**: El breadcrumb es puramente presentacional, no requiere cambios en Presenter o Model
- **Validación**: No se importa PySide6 en Model, no hay lógica de negocio en View

## Risks / Trade-offs

**[Riesgo] Consumo vertical de espacio** → Mitigación: El header aumentará de altura pero mejorará la usabilidad. En pantallas pequeñas, el espacio vertical es menos crítico que el horizontal para breadcrumbs.

**[Riesgo] Cambio visual significativo para usuarios existentes** → Mitigación: Es una mejora de UX, no una regresión. Los usuarios se adaptarán rápidamente.

**[Riesgo] Layout podría romperse con widgets personalizados** → Mitigación: Se mantendrá la API de la View, solo cambia el layout interno.

## Decisions on Open Questions

**Separador visual entre filas:** NO - Se mantiene un diseño limpio sin líneas divisorias entre el breadcrumb y los botones.

**Indicador de breadcrumb largo:** NO (por ahora) - No se implementará indicador visual adicional. Si en el futuro el breadcrumb excede el ancho, se evaluará scroll horizontal o truncamiento con elipsis.
