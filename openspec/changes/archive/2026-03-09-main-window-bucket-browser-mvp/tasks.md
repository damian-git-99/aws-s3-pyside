## 1. MVP Framework Foundation

- [x] 1.1 Crear estructura de directorios MVP (`mvp/`, `models/`, `views/`, `presenters/`)
- [x] 1.2 Implementar `BaseModel` abstract class en `mvp/base_model.py`
- [x] 1.3 Implementar `BaseView` abstract class en `mvp/base_view.py`
- [x] 1.4 Implementar `BasePresenter` abstract class en `mvp/base_presenter.py`
- [x] 1.5 Definir contratos/interfaces en `mvp/contracts.py` con Protocol/ABC
- [x] 1.6 Crear sistema de signals para comunicación Model→Presenter
- [x] 1.7 Implementar helper de mocking para testing de Presenters

## 2. Bucket Browser Main Window

- [x] 2.1 Crear modelo de datos para objetos del bucket (`BucketObject`)
- [x] 2.2 Crear `BucketBrowserModel` con datos mock variados (archivos de distintos tipos)
- [x] 2.3 Implementar sistema de iconos por tipo de archivo en `utils/file_icons.py`
- [x] 2.4 Crear `BucketBrowserView` con QTableWidget y columnas requeridas
- [x] 2.5 Implementar toolbar con botón de refresh y botón de upload (placeholder)
- [x] 2.6 Crear `BucketBrowserPresenter` que coordina Model y View
- [x] 2.7 Implementar ordenamiento de columnas (Name, Size, Last Modified, Storage Class)

## 3. Integration & Polish

- [x] 3.1 Agregar styling CSS/moderno a los widgets
- [x] 3.2 Implementar menu bar básico (File, View, Help)
- [x] 3.3 Agregar status bar con información contextual
- [x] 3.4 Crear entry point principal de la aplicación (`main.py`)

## 4. Testing

- [x] 4.1 Escribir tests unitarios para `BucketBrowserPresenter`
- [x] 4.2 Crear mocks de View para testing sin PySide6
- [x] 4.3 Escribir tests de integración para carga inicial de datos
- [x] 4.4 Escribir tests para sistema de iconos por tipo de archivo

## 5. Documentation

- [x] 5.1 Crear `AGENTS.md` con explicación del patrón MVP
- [x] 5.2 Documentar responsabilidades de Model, View, Presenter
- [x] 5.3 Incluir ejemplo completo de componente MVP en AGENTS.md
- [x] 5.4 Documentar convenciones de nomenclatura
- [x] 5.5 Crear guía de testing para Presenters
- [x] 5.6 Actualizar README con instrucciones de ejecución
