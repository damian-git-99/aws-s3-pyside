## 1. Refactor del Header - Layout Vertical

- [x] 1.1 Identificar el archivo View del header actual
- [x] 1.2 Cambiar el layout del header de QHBoxLayout a QVBoxLayout
- [x] 1.3 Crear contenedor para la fila del breadcrumb (QWidget o QFrame)
- [x] 1.4 Crear contenedor para la fila de botones (QWidget o QFrame)
- [x] 1.5 Agregar ambos contenedores al layout vertical principal

## 2. Reubicar Componentes

- [x] 2.1 Mover el widget del breadcrumb al contenedor superior
- [x] 2.2 Configurar el breadcrumb para usar todo el ancho disponible (expandir)
- [x] 2.3 Mover los botones de acción al contenedor inferior
- [x] 2.4 Configurar alineación de botones (izquierda, derecha o centrada según diseño actual)
- [x] 2.5 Verificar que no queden widgets huérfanos en el layout antiguo

## 3. Ajustes de Estilo y Espaciado

- [x] 3.1 Agregar espaciado entre las dos filas (layout spacing)
- [x] 3.2 Agregar márgenes apropiados al header (layout margins)
- [x] 3.3 ~~Opcional: Agregar línea separadora visual~~ → Decidido: NO se agrega separador
- [x] 3.4 Verificar estilos CSS existentes no se rompan con el nuevo layout

## 4. Testing y Verificación

- [x] 4.1 Ejecutar la aplicación y verificar que se muestra correctamente
- [x] 4.2 Probar navegación profunda (múltiples niveles) para verificar espacio del breadcrumb
- [x] 4.3 Verificar que los botones responden a clicks correctamente
- [x] 4.4 Verificar que el breadcrumb se actualiza al cambiar de vista
- [x] 4.5 Probar en diferentes tamaños de ventana
- [x] 4.6 Ejecutar tests existentes: `uv run python -m unittest discover src/tests/`

## 5. Limpieza y Documentación

- [x] 5.1 Eliminar código comentado o no utilizado del layout anterior
- [x] 5.2 Actualizar docstrings si es necesario
- [x] 5.3 Verificar que se mantienen las convenciones MVP (no lógica en View)
