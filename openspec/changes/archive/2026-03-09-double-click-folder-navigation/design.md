## Context

El bucket browser actual muestra objetos del bucket S3 en una lista plana. El S3FileService ya soporta el parámetro `prefix` para listar objetos bajo rutas específicas, pero actualmente el presenter siempre lo llama sin prefix (nivel raíz).

Para implementar navegación jerárquica, necesitamos:
1. Detectar doble-click en folders y navegar hacia adentro
2. Mantener el estado de la ruta actual
3. Proveer mecanismos para volver (Up) y regresar a raíz (Home)
4. Mostrar el breadcrumb de la ruta actual

## Goals / Non-Goals

**Goals:**
- Navegación fluida hacia adentro de folders mediante doble-click
- Breadcrumb clickeable para navegar rápidamente a cualquier nivel
- Botones Home y Up para navegación alternativa
- Estado de ruta persistente durante la sesión
- Paginación funciona en cada nivel de directorio

**Non-Goals:**
- Historial de navegación tipo "Back button del browser"
- Soporte para múltiples tabs o ventanas
- Persistencia de ruta entre sesiones
- Navegación con teclado (por ahora)

## Decisions

### 1. Estado de ruta en el Presenter
**Decision:** El presenter mantendrá el estado de la ruta actual (`_current_prefix`).

**Rationale:**
- MVP: La view es pasiva, el presenter maneja la lógica
- Facilita testing sin Qt
- El modelo actual no necesita cambios

**Alternative considered:** Mantener estado en el modelo - rechazado porque el modelo actual es simple y esta funcionalidad es de presentación.

### 2. Formato del prefix
**Decision:** Usar formato S3 nativo (`folder/subfolder/`).

**Rationale:**
- S3FileService ya espera este formato
- Consistencia con la API de AWS
- Fácil de construir/descomponer

### 3. Detección de folders
**Decision:** Los folders son identificados por `is_folder=True` en `BucketObject`.

**Rationale:**
- El modelo ya tiene este campo
- El servicio ya establece este flag correctamente
- No necesita parsing de nombres

### 4. Breadcrumb como lista de segmentos
**Decision:** El breadcrumb se construirá como lista de tuplas `(nombre, prefix_completo)`.

**Rationale:**
- Facilita renderizado en la view
- Cada segmento sabe a dónde navegar
- Fácil de mantener sincronizado

Ejemplo:
```
[("my-bucket", ""), ("folder1", "folder1/"), ("subfolder", "folder1/subfolder/")]
```

### 5. Manejo de paginación por nivel
**Decision:** Cada cambio de directorio resetea la paginación.

**Rationale:**
- Más simple de implementar
- Comportamiento esperado del usuario
- S3 API maneja tokens independientemente por prefix

## Riesgos / Trade-offs

**[Riesgo]** El usuario puede perder su posición al navegar hacia adentro y volver (se resetea la paginación)
→ **Mitigación:** Considerar cache de resultados por nivel en iteraciones futuras

**[Riesgo]** Buckets con estructuras muy profundas pueden tener breadcrumbs muy largos
→ **Mitigación:** Implementar truncamiento con "..." en la UI si es necesario

**[Riesgo]** Doble-click accidental en archivos (no hay acción definida todavía)
→ **Mitigación:** Ignorar doble-click en archivos por ahora, documentar para futura implementación (preview/download)

## Open Questions

1. ¿Se debe implementar cache de contenido por directorio para evitar re-fetch al volver?
   - **Decisión:** No por ahora, puede agregarse después sin breaking changes.

2. ¿El breadcrumb debe mostrar el bucket name o solo el path?
   - **Decisión:** Mostrar "Bucket > folder1 > folder2" donde "Bucket" es clickeable y va a raíz.
