## Context

La aplicación PySide6 actualmente no configura explícitamente el estilo de la interfaz, lo que permite que herede el tema del sistema operativo. En Windows 10/11 con tema dark habilitado, esto causa que Qt aplique automáticamente estilos dark que no fueron diseñados para esta aplicación MVP, resultando en problemas visuales.

**Arquitectura actual**: La aplicación sigue el patrón MVP con entry point en `src/main.py` donde se inicializa `QApplication`. El estilo no se configura explícitamente.

**Restricciones**:
- Mínima modificación al código existente
- No introducir dependencias externas
- Mantener compatibilidad multiplataforma (Windows/Linux)

## Goals / Non-Goals

**Goals:**
- Forzar explícitamente el tema claro (light) al iniciar la aplicación
- Prevenir que el SO inyecte estilos dark no deseados
- Mantener consistencia visual en todas las plataformas
- Solución simple y mantenible

**Non-Goals:**
- No agregar soporte para modo dark (solo deshabilitarlo)
- No crear sistema de temas configurable por el usuario
- No modificar el diseño visual actual de la aplicación

## Decisions

### Opción A: Usar `QApplication.setStyle('Fusion')` + paleta clara manual
**Decisión**: ELEGIDA

**Razonamiento**:
- `Fusion` es el estilo nativo de Qt que se ve consistente en todas las plataformas
- Al establecer el estilo explícitamente, evitamos que Windows inyecte sus estilos dark
- Es la solución más simple y robusta

**Código**:
```python
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor

app = QApplication(sys.argv)
# Forzar estilo Fusion (neutral, consistente)
app.setStyle('Fusion')
# Configurar paleta clara explícita
palette = QPalette()
app.setPalette(palette)
```

### Opción B: Usar `QApplication.setStyle('Windows')` 
**Decisión**: RECHAZADA

**Razonamiento**:
- El estilo 'Windows' en Windows 10/11 respeta el tema del sistema
- No solucionaría el problema en Windows con tema dark

### Opción C: Establecer variable de entorno `QT_QPA_PLATFORMTHEME`
**Decisión**: RECHAZADA

**Razonamiento**:
- Requiere configuración externa a la aplicación
- Menos robusto (depende del entorno de ejecución)
- Más difícil de mantener y debuggear

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Estilo Fusion puede verse diferente al nativo de Windows | Aceptable: consistencia cross-platform es más importante que look nativo perfecto |
| Usuarios con preferencia por dark mode no tendrán su preferencia respetada | Aceptable: la aplicación no fue diseñada para modo dark, es un bugfix, no una feature |
| Cambio de comportamiento en Linux | Verificar que sigue funcionando correctamente; Fusion es consistente en Linux |
