## 1. Presenter - Estado de Navegación

- [ ] 1.1 Agregar `_current_prefix: Optional[str]` al presenter para rastrear la ruta actual
- [ ] 1.2 Agregar método `navigate_to_folder(folder_name: str)` para navegar hacia adentro
- [ ] 1.3 Agregar método `navigate_to_prefix(prefix: Optional[str])` para navegación directa
- [ ] 1.4 Agregar método `navigate_up()` para volver al directorio padre
- [ ] 1.5 Agregar método `navigate_to_root()` para volver a la raíz
- [ ] 1.6 Modificar `_load_bucket_contents()` para usar `_current_prefix` en lugar de hardcodear `None`
- [ ] 1.7 Agregar método `get_breadcrumb()` que retorne lista de tuplas `(nombre, prefix)`
- [ ] 1.8 Agregar método `on_item_double_clicked(object_name: str, is_folder: bool)` manejador de eventos

## 2. View - Doble-click y Breadcrumb

- [ ] 2.1 Agregar event handler `cellDoubleClicked` a la tabla con conexión al presenter
- [ ] 2.2 Crear método `setup_breadcrumb()` para inicializar el área de breadcrumb en la toolbar
- [ ] 2.3 Crear método `update_breadcrumb(path_segments: List[Tuple[str, Optional[str]]])` para actualizar el breadcrumb
- [ ] 2.4 Crear método `_on_breadcrumb_clicked(prefix: Optional[str])` handler para clicks en breadcrumb
- [ ] 2.5 Agregar botón "Home" a la toolbar (ícono de casa)
- [ ] 2.6 Agregar botón "Up" a la toolbar (ícono de flecha arriba)
- [ ] 2.7 Conectar botón Home a `_on_home_clicked()` que llame a presenter
- [ ] 2.8 Conectar botón Up a `_on_up_clicked()` que llame a presenter
- [ ] 2.9 Crear método `enable_navigation_buttons(can_go_up: bool)` para habilitar/deshabilitar botones
- [ ] 2.10 Actualizar título de ventana para incluir ruta actual

## 3. Tests

- [ ] 3.1 Crear tests para `navigate_to_folder()` - verificar que actualiza prefix y recarga datos
- [ ] 3.2 Crear tests para `navigate_up()` - verificar que sube un nivel y maneja raíz
- [ ] 3.3 Crear tests para `navigate_to_root()` - verificar que va a raíz y limpia prefix
- [ ] 3.4 Crear tests para `get_breadcrumb()` - verificar estructura correcta de tuplas
- [ ] 3.5 Crear tests para `on_item_double_clicked()` - verificar que solo navega en folders
- [ ] 3.6 Actualizar tests existentes para incluir el nuevo estado de navegación

## 4. Integración y Verificación

- [ ] 4.1 Verificar que doble-click en folder navega correctamente
- [ ] 4.2 Verificar que doble-click en archivo no hace nada
- [ ] 4.3 Verificar que breadcrumb se actualiza al navegar
- [ ] 4.4 Verificar que clicks en breadcrumb navegan al nivel correcto
- [ ] 4.5 Verificar que botón Home va a raíz desde cualquier nivel
- [ ] 4.6 Verificar que botón Up sube un nivel correctamente
- [ ] 4.7 Verificar que botones están deshabilitados en raíz
- [ ] 4.8 Verificar que paginación funciona en cada nivel de directorio
- [ ] 4.9 Verificar que refresh mantiene el directorio actual
- [ ] 4.10 Ejecutar todos los tests y confirmar que pasan
