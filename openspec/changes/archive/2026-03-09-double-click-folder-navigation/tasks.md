## 1. Presenter - Estado de Navegación

- [x] 1.1 Agregar `_current_prefix: Optional[str]` al presenter para rastrear la ruta actual
- [x] 1.2 Agregar método `navigate_to_folder(folder_name: str)` para navegar hacia adentro
- [x] 1.3 Agregar método `navigate_to_prefix(prefix: Optional[str])` para navegación directa
- [x] 1.4 Agregar método `navigate_up()` para volver al directorio padre
- [x] 1.5 Agregar método `navigate_to_root()` para volver a la raíz
- [x] 1.6 Modificar `_load_bucket_contents()` para usar `_current_prefix` en lugar de hardcodear `None`
- [x] 1.7 Agregar método `get_breadcrumb()` que retorne lista de tuplas `(nombre, prefix)`
- [x] 1.8 Agregar método `on_item_double_clicked(object_name: str, is_folder: bool)` manejador de eventos

## 2. View - Doble-click y Breadcrumb

- [x] 2.1 Agregar event handler `cellDoubleClicked` a la tabla con conexión al presenter
- [x] 2.2 Crear método `setup_breadcrumb()` para inicializar el área de breadcrumb en la toolbar
- [x] 2.3 Crear método `update_breadcrumb(path_segments: List[Tuple[str, Optional[str]]])` para actualizar el breadcrumb
- [x] 2.4 Crear método `_on_breadcrumb_clicked(prefix: Optional[str])` handler para clicks en breadcrumb
- [x] 2.5 Agregar botón "Home" a la toolbar (ícono de casa)
- [x] 2.6 Agregar botón "Up" a la toolbar (ícono de flecha arriba)
- [x] 2.7 Conectar botón Home a `_on_home_clicked()` que llame a presenter
- [x] 2.8 Conectar botón Up a `_on_up_clicked()` que llame a presenter
- [x] 2.9 Crear método `enable_navigation_buttons(can_go_up: bool)` para habilitar/deshabilitar botones
- [x] 2.10 Actualizar título de ventana para incluir ruta actual

## 3. Tests

- [x] 3.1 Crear tests para `navigate_to_folder()` - verificar que actualiza prefix y recarga datos
- [x] 3.2 Crear tests para `navigate_up()` - verificar que sube un nivel y maneja raíz
- [x] 3.3 Crear tests para `navigate_to_root()` - verificar que va a raíz y limpia prefix
- [x] 3.4 Crear tests para `get_breadcrumb()` - verificar estructura correcta de tuplas
- [x] 3.5 Crear tests para `on_item_double_clicked()` - verificar que solo navega en folders
- [x] 3.6 Actualizar tests existentes para incluir el nuevo estado de navegación

## 4. Integración y Verificación

- [x] 4.1 Verificar que doble-click en folder navega correctamente
- [x] 4.2 Verificar que doble-click en archivo no hace nada
- [x] 4.3 Verificar que breadcrumb se actualiza al navegar
- [x] 4.4 Verificar que clicks en breadcrumb navegan al nivel correcto
- [x] 4.5 Verificar que botón Home va a raíz desde cualquier nivel
- [x] 4.6 Verificar que botón Up sube un nivel correctamente
- [x] 4.7 Verificar que botones están deshabilitados en raíz
- [x] 4.8 Verificar que paginación funciona en cada nivel de directorio
- [x] 4.9 Verificar que refresh mantiene el directorio actual
- [x] 4.10 Ejecutar todos los tests y confirmar que pasan
