# MVP Architecture

Patrón Model-View-Presenter para PySide6.

```
Model ←→ Presenter ←→ View
  ↑                     ↓
 (datos)           (eventos)
```

## Responsabilidades

- **Model**: Datos y lógica de negocio. Emite señales Qt (`data_changed`, `data_loaded`, `error_occurred`).
- **View**: UI pasiva. Solo muestra y reenvía eventos al Presenter.
- **Presenter**: Intermediario. Recibe eventos, pide datos, actualiza view.

## Package Management (uv)

```bash
# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar aplicación
# IMPORTANTE: Usar -m para que Python reconozca src como módulo
uv run python -m src.main

# Tests
uv run python -m unittest discover src/tests/
```

**Nota**: `uv run python -m src.main` es necesario (no `src/main.py`) para que Python reconozca correctamente el paquete `src`.

## Reglas

❌ No lógica de negocio en View  
❌ No imports de PySide6 en Model  
❌ No dependencias View→Model

✅ View solo muestra datos  
✅ Model emite señales Qt  
✅ Presenter testeable sin Qt  
✅ Todo en `src/` con prefijo `src.`

## OpenSpec Workflow

Al usar `/opsx-archive`: recordar sincronizar también con las specs generales (ver formato en algun file de `openspec/specs/`).
