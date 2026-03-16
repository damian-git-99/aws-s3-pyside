## 1. Preparación

- [x] 1.1 Leer el archivo `src/main.py` actual para entender la estructura de inicialización
- [x] 1.2 Verificar imports necesarios (`QStyleFactory`, `QPalette` de PySide6)

## 2. Implementación

- [x] 2.1 Importar `QStyleFactory` en `src/main.py` si no está presente
- [x] 2.2 Después de crear `QApplication`, llamar `app.setStyle('Fusion')` para forzar estilo neutral
- [x] 2.3 Configurar paleta clara explícita con `app.setPalette(QPalette())`
- [x] 2.4 Verificar que la aplicación sigue ejecutándose correctamente en Linux

## 3. Verificación

- [x] 3.1 Ejecutar `uv run python -m src.main` y verificar que no hay errores
- [x] 3.2 Confirmar visualmente que la UI carga con tema claro (verificar colores de fondo, texto)
- [x] 3.3 Verificar que los estilos se aplican correctamente a todos los widgets (tabla, botones, formularios)

## 4. Documentación

- [x] 4.1 Agregar comentario breve en `src/main.py` explicando por qué se fuerza el estilo Fusion
