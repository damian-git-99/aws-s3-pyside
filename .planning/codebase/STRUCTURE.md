# Codebase Structure

**Analysis Date:** 2026-04-04

## Directory Layout

```
s3-file-manager/
├── .planning/              # GSD planning artifacts
│   └── codebase/           # Codebase analysis documents
├── .opencode/              # OpenCode framework files
│   ├── agents/             # Agent configurations
│   ├── skills/             # Custom skills
│   └── get-shit-done/      # GSD framework
├── openspec/               # OpenSpec feature specifications
│   └── specs/              # Individual feature specs
├── src/                    # Main source code
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── main_window.py      # Legacy main window (unused)
│   ├── config.py           # Legacy config (deprecated)
│   ├── config/             # Configuration management
│   │   ├── __init__.py
│   │   └── config_manager.py
│   ├── mvp/                # MVP framework base classes
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── base_view.py
│   │   ├── base_presenter.py
│   │   └── contracts.py
│   ├── models/             # Model layer (business logic)
│   │   ├── __init__.py
│   │   ├── bucket_browser_model.py
│   │   └── bucket_object.py
│   ├── views/              # View layer (UI)
│   │   ├── __init__.py
│   │   ├── bucket_browser_view.py
│   │   ├── settings_panel_view.py
│   │   ├── setup_wizard_view.py
│   │   ├── image_preview_dialog.py
│   │   └── folder_first_sort_proxy_model.py
│   ├── presenters/         # Presenter layer (orchestration)
│   │   ├── __init__.py
│   │   ├── bucket_browser_presenter.py
│   │   └── config_presenter.py
│   ├── services/           # Service layer (external APIs)
│   │   ├── __init__.py
│   │   ├── s3_service.py
│   │   └── s3_errors.py
│   ├── utils/              # Utility modules
│   │   ├── __init__.py
│   │   ├── file_icons.py
│   │   └── styles.py
│   └── tests/              # Unit tests
│       ├── __init__.py
│       ├── mock_view.py
│       ├── test_bucket_browser_model.py
│       ├── test_bucket_browser_presenter.py
│       ├── test_config.py
│       ├── test_data_loading.py
│       ├── test_file_icons.py
│       ├── test_s3_errors.py
│       └── test_s3_service.py
├── build.py                # PyInstaller build script
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Python dependencies
├── build/                  # Build artifacts
├── dist/                   # Distribution binaries
├── .env.example            # Environment template
├── .gitignore
├── README.md
└── AGENTS.md               # Project-specific agent instructions
```

## Directory Purposes

### `src/` - Source Root
- **Purpose:** All application code
- **Run command:** `uv run python -m src.main` (note the `-m` flag for proper package resolution)
- **Key files:**
  - `main.py` - Application entry point, QApplication setup, MVP wiring
  - `config.py` - Legacy environment-based config (being phased out)

### `src/mvp/` - MVP Framework
- **Purpose:** Base classes enforcing MVP architecture
- **Contains:** Abstract base classes with Qt signal integration
- **Key files:**
  - `base_model.py` - `BaseModel` with `ModelSignals` (data_changed, error_occurred, etc.)
  - `base_view.py` - `BaseView` extending `QWidget` with presenter reference
  - `base_presenter.py` - `BasePresenter` with automatic signal connection
  - `contracts.py` - Protocol definitions for type checking

### `src/models/` - Model Layer
- **Purpose:** Business logic and data management
- **Contains:** Domain models with Qt signals
- **Key files:**
  - `bucket_browser_model.py` - Manages bucket objects, mock data fallback
  - `bucket_object.py` - Domain entity (dataclass) for S3 objects

### `src/views/` - View Layer
- **Purpose:** UI components, passive presentation
- **Contains:** QWidget subclasses, dialogs
- **Key files:**
  - `bucket_browser_view.py` - Main window (1091 lines), complex UI setup
  - `settings_panel_view.py` - Settings dialog UI
  - `setup_wizard_view.py` - First-time setup wizard
  - `image_preview_dialog.py` - Image preview modal
  - `folder_first_sort_proxy_model.py` - Custom QSortFilterProxyModel

### `src/presenters/` - Presenter Layer
- **Purpose:** Orchestration between Model and View
- **Contains:** Presenter classes, worker threads
- **Key files:**
  - `bucket_browser_presenter.py` - Main presenter (816 lines), includes UploadWorker/DownloadWorker
  - `config_presenter.py` - Settings/configuration presenter

### `src/services/` - Service Layer
- **Purpose:** External API abstraction
- **Contains:** S3 service, custom exceptions
- **Key files:**
  - `s3_service.py` - boto3 wrapper with pagination (385 lines)
  - `s3_errors.py` - Typed S3 exception hierarchy

### `src/config/` - Configuration
- **Purpose:** Persistent settings management
- **Contains:** SQLite-backed configuration manager
- **Key files:**
  - `config_manager.py` - `ConfigManager` with Qt signals, SQLite backend

### `src/utils/` - Utilities
- **Purpose:** Shared utility functions
- **Contains:** Icon management, styling
- **Key files:**
  - `file_icons.py` - `FileIconManager` with custom-drawn icons
  - `styles.py` - Application-wide QSS styles

### `src/tests/` - Tests
- **Purpose:** Unit tests
- **Contains:** Test files with mock implementations
- **Key files:**
  - `mock_view.py` - Mock view for testing presenters
  - `test_*.py` - Individual test modules

### `openspec/` - Feature Specifications
- **Purpose:** OpenSpec workflow artifacts
- **Contains:** YAML specifications for implemented features
- **Examples:** `bucket-browser-main-window/`, `file-upload/`, `search-filter/`, etc.

## Key File Locations

### Entry Points
- **Main:** `src/main.py` - `main()` function, application startup
- **Build:** `build.py` - PyInstaller executable generation

### Configuration
- **Project:** `pyproject.toml` - Dependencies, Python version
- **Legacy:** `src/config.py` - Environment variable config (deprecated)
- **Current:** `src/config/config_manager.py` - SQLite-based config
- **Template:** `.env.example` - AWS credentials template

### Core Logic
- **Main Presenter:** `src/presenters/bucket_browser_presenter.py`
- **Main View:** `src/views/bucket_browser_view.py`
- **Main Model:** `src/models/bucket_browser_model.py`
- **S3 Service:** `src/services/s3_service.py`

### Testing
- **Test Directory:** `src/tests/`
- **Run Tests:** `uv run python -m unittest discover src/tests/`

## Naming Conventions

### Files
- **Pattern:** `snake_case.py`
- **Examples:** `bucket_browser_view.py`, `s3_service.py`

### Classes
- **Pattern:** `PascalCase`
- **Model:** `BucketBrowserModel`, `BucketObject`
- **View:** `BucketBrowserView`, `SettingsPanel`
- **Presenter:** `BucketBrowserPresenter`, `ConfigPresenter`
- **Service:** `S3FileService`
- **Worker:** `UploadWorker`, `DownloadWorker`

### Methods
- **Pattern:** `snake_case`
- **Private:** Leading underscore `_load_bucket_contents`
- **Callbacks:** `on_*` prefix (e.g., `on_refresh_clicked`)
- **Handlers:** `handle_*` prefix (e.g., `handle_delete_file`)

### Qt Objects
- **Pattern:** `snake_case` with `_` prefix for private widgets
- **Examples:** `_table`, `_toolbar`, `_home_btn`

## Where to Add New Code

### New Feature (e.g., new dialog)
- **View:** `src/views/my_feature_view.py` - Extend `BaseView`
- **Model:** `src/models/my_feature_model.py` - Extend `BaseModel` (if needed)
- **Presenter:** `src/presenters/my_feature_presenter.py` - Extend `BasePresenter`
- **Wiring:** `src/main.py` - Add to initialization flow

### New S3 Operation
- **Service:** Add method to `src/services/s3_service.py`
- **Errors:** Add exception class to `src/services/s3_errors.py` (if new error type)
- **Model:** Add method to `src/models/bucket_browser_model.py`
- **Presenter:** Add handler method to `src/presenters/bucket_browser_presenter.py`
- **View:** Add UI controls to `src/views/bucket_browser_view.py`

### New Utility
- **Location:** `src/utils/my_utility.py`
- **Import:** Use absolute imports: `from src.utils.my_utility import ...`

### New Test
- **Location:** `src/tests/test_my_feature.py`
- **Run:** `uv run python -m unittest src.tests.test_my_feature`

## Special Directories

### `.venv/`
- **Purpose:** Python virtual environment (uv-managed)
- **Generated:** Yes (by `uv`)
- **Committed:** No (in `.gitignore`)

### `build/` and `dist/`
- **Purpose:** PyInstaller build artifacts
- **Generated:** Yes (by `build.py`)
- **Committed:** No (in `.gitignore`)

### `.opencode/`
- **Purpose:** OpenCode framework metadata
- **Contains:** Skills, GSD workflow files
- **Committed:** Yes (contains custom skills)

### `openspec/specs/`
- **Purpose:** Feature specifications
- **Format:** YAML with implementation artifacts
- **Committed:** Yes (project documentation)

## Import Patterns

### Internal Imports
```python
# Absolute imports required (package is 'src')
from src.mvp.base_model import BaseModel
from src.models.bucket_object import BucketObject
from src.services.s3_service import S3FileService
```

### Qt Imports
```python
from PySide6.QtWidgets import QWidget, QTableWidget
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QAction, QIcon
```

### Third-Party Imports
```python
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
```

## Package Management

**Tool:** `uv` (modern Python package manager)

**Key Commands:**
```bash
# Install dependencies
uv pip install -r requirements.txt

# Run application (CRITICAL: use -m for proper package resolution)
uv run python -m src.main

# Run tests
uv run python -m unittest discover src/tests/

# Build executable
uv run python build.py
```

**Important:** Always use `uv run python -m src.main` (not `src/main.py`) so Python recognizes `src` as a package and absolute imports work correctly.

---

*Structure analysis: 2026-04-04*
