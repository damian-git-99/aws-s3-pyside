## 1. Project Setup

- [x] 1.1 Create pyproject.toml with project metadata and PySide6 dependency
- [x] 1.2 Create src/ directory structure
- [x] 1.3 Initialize Python package with __init__.py

## 2. UV Environment Setup

- [x] 2.1 Install uv if not already installed
- [x] 2.2 Create virtual environment with `uv venv`
- [x] 2.3 Install dependencies with `uv sync`
- [x] 2.4 Verify .venv is created and working

## 3. Main Window Implementation

- [x] 3.1 Create main.py entry point with QApplication
- [x] 3.2 Implement MainWindow class extending QMainWindow
- [x] 3.3 Set window title to "S3 File Manager"
- [x] 3.4 Set minimum window size to 800x600
- [x] 3.5 Implement basic close event handling

## 4. Verification

- [x] 4.1 Test application launches with `uv run python -m src.main`
- [x] 4.2 Verify window displays and can be closed
