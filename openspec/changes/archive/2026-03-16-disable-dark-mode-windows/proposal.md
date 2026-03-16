## Why

En Windows, la aplicación hereda automáticamente el tema del sistema operativo. Cuando Windows está en modo dark, PySide6 carga la aplicación con estilos dark que no fueron diseñados ni probados para esta aplicación, causando problemas visuales donde la UI se ve mal (colores incorrectos, contraste deficiente, elementos no visibles). Se necesita deshabilitar explícitamente el soporte de modo dark para asegurar una experiencia visual consistente y funcional en todas las plataformas.

## What Changes

- Deshabilitar el soporte de modo dark en Windows forzando el estilo claro (light) al iniciar la aplicación
- Agregar configuración explícita de estilo en el punto de entrada de la aplicación (`src/main.py`)
- Verificar que el fix también aplique en Linux por si las dudas (prevenir futuros problemas)
- **No breaking changes**: La aplicación simplemente forzará el tema claro en lugar de heredar el del sistema

## Capabilities

### New Capabilities
- `disable-dark-mode`: Forzar tema claro en la aplicación PySide6 ignorando el tema del sistema operativo

### Modified Capabilities
<!-- No hay capacidades existentes que cambien sus requisitos, solo la implementación -->

## Impact

- **Código afectado**: `src/main.py` - punto de entrada de la aplicación
- **APIs**: Ninguna API expuesta cambia
- **Dependencias**: Usa `QApplication.setStyle()` y `QStyleFactory` de PySide6
- **Sistemas**: Windows (principal), Linux (verificación preventiva)
- **UX**: Usuarios verán siempre el tema claro independientemente de la configuración del sistema
