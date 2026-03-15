## Why

El breadcrumb actual comparte espacio con los botones de acción, lo que causa problemas de espacio cuando el usuario navega profundamente en la jerarquía. El texto del breadcrumb se trunca o los botones se comprimen, afectando la usabilidad. Es necesario darle a cada elemento su propio espacio dedicado para mejorar la experiencia de usuario y la legibilidad.

## What Changes

- Mover el breadcrumb a una línea/barra dedicada separada de los botones de acción
- El área de botones mantendrá su posición actual pero con espacio exclusivo
- El breadcrumb ocupará todo el ancho disponible en su propia fila
- Ajustar el layout del header para separar claramente estas dos áreas funcionales

## Capabilities

### New Capabilities
- `breadcrumb-layout`: Nueva estructura de layout que separa el breadcrumb en su propio espacio visual
- `header-refactor`: Reorganización del componente header para soportar múltiples filas de controles

### Modified Capabilities
<!-- No hay capabilities existentes con cambios en requisitos, solo implementación -->

## Impact

- UI/View: Cambio en la estructura del layout del header
- Presenter: Posible ajuste en la lógica de actualización del breadcrumb
- Estilos CSS: Nuevos estilos para el layout de dos filas
