# Architecture

**Analysis Date:** 2026-04-04

## Pattern Overview

**Overall:** Model-View-Presenter (MVP) with Clean Architecture principles

**Key Characteristics:**
- Strict separation: Model knows nothing about UI, View is passive, Presenter orchestrates
- Qt Signals for Model-Presenter communication (async, decoupled)
- Direct method calls for View-Presenter communication (immediate, typed)
- Service layer abstracts external dependencies (S3)
- Configuration persistence via SQLite with Qt signals

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ BucketBrowser│    │   Config     │    │    SetupWizard   │  │
│  │    View      │◄──►│  Presenter   │◄──►│   / Settings     │  │
│  │              │    │              │    │     Panel        │  │
│  └──────┬───────┘    └──────────────┘    └──────────────────┘  │
│         │                                                        │
│         │ set_presenter() / event callbacks                      │
│         ▼                                                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ BucketBrowser│◄──►│ UploadWorker │    │  DownloadWorker  │  │
│  │  Presenter   │    │   (QThread)  │    │    (QThread)     │  │
│  └──────┬───────┘    └──────────────┘    └──────────────────┘  │
│         │                                         ▲              │
│         │ Qt Signals (data_changed, etc.)         │              │
│         ▼                                         │              │
│  ┌──────────────┐    ┌──────────────────────────────┐          │
│  │ BucketBrowser│    │         S3FileService          │          │
│  │    Model     │◄──►│  (boto3 S3 abstraction layer)  │          │
│  └──────────────┘    └──────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/HTTPS
                              ▼
                    ┌─────────────────────┐
                    │    AWS S3 API       │
                    └─────────────────────┘
```

## Layers

### Model Layer
- **Purpose:** Business logic, data management, domain objects
- **Location:** `src/models/`
- **Contains:** Data classes, model implementations with Qt signals
- **Depends on:** Services (for external data), MVP base classes
- **Used by:** Presenters

**Key Components:**
- `BucketBrowserModel` - Manages bucket objects list, handles CRUD operations
- `BucketObject` - Domain entity representing S3 objects (files/folders)

### View Layer
- **Purpose:** UI presentation, event forwarding, passive display
- **Location:** `src/views/`
- **Contains:** QWidget subclasses, dialogs, custom widgets
- **Depends on:** PySide6, MVP base classes, models (for data typing)
- **Used by:** Presenters

**Key Components:**
- `BucketBrowserView` - Main window with table, toolbar, breadcrumbs
- `SetupWizardDialog` - First-time configuration wizard
- `SettingsPanel` - Configuration management dialog
- `ImagePreviewDialog` - Image preview modal
- `FolderFirstSortProxyModel` - Custom sorting (folders first)

### Presenter Layer
- **Purpose:** Orchestration, business logic coordination, View-Model mediation
- **Location:** `src/presenters/`
- **Contains:** Presenter classes that wire Models to Views
- **Depends on:** Models, Views, Services
- **Used by:** Main application, Views (via callbacks)

**Key Components:**
- `BucketBrowserPresenter` - Main presenter handling navigation, uploads, downloads
- `ConfigPresenter` - Settings/configuration management
- `UploadWorker` / `DownloadWorker` - Background thread workers for I/O

### Service Layer
- **Purpose:** External API abstraction, I/O operations, error translation
- **Location:** `src/services/`
- **Contains:** Service classes, custom exceptions, API clients
- **Depends on:** boto3, external APIs
- **Used by:** Models, Presenters

**Key Components:**
- `S3FileService` - AWS S3 operations (list, upload, download, delete)
- `S3Error` hierarchy - Typed exceptions for S3 operations

### Configuration Layer
- **Purpose:** Persistent settings management
- **Location:** `src/config/`
- **Contains:** Config manager with SQLite backend
- **Depends on:** PySide6 (signals), sqlite3
- **Used by:** Presenters, Main application

**Key Components:**
- `ConfigManager` - SQLite-backed persistent settings with Qt signals
- Legacy `config.py` - Environment variable loading (deprecated)

### MVP Framework
- **Purpose:** Base classes enforcing MVP contract
- **Location:** `src/mvp/`
- **Contains:** Abstract base classes, protocols, signal definitions
- **Depends on:** PySide6 (signals)
- **Used by:** All Models, Views, Presenters

**Key Components:**
- `BaseModel` - Abstract model with Qt signals
- `BaseView` - Abstract view with presenter reference
- `BasePresenter` - Abstract presenter with Model signal connections
- `contracts.py` - Protocol definitions for type checking

## Data Flow

### Initial Load Flow:

1. **Main** creates `ConfigManager`, checks for first-time setup
2. **Main** creates `S3FileService` with loaded configuration
3. **Main** creates `BucketBrowserModel` → `BucketBrowserView`
4. **Main** creates `BucketBrowserPresenter(model, view, s3_service)`
5. **Presenter.initialize()** connects to Model signals, loads bucket contents
6. **Presenter** calls `S3FileService.list_objects()` → converts to `BucketObject` list
7. **Presenter** calls `view.display_data(objects)` → View updates table
8. **View** enables UI elements based on data presence

### Navigation Flow:

1. **User** double-clicks folder in View
2. **View** forwards to `presenter.on_item_double_clicked(name, is_folder=True)`
3. **Presenter** updates `_current_prefix`, resets pagination
4. **Presenter** calls `_load_bucket_contents()` → fetches from S3
5. **Model** (indirectly) receives data via Presenter
6. **Presenter** calls `view.display_data()` with new objects
7. **Presenter** calls `view.update_breadcrumb()` with path segments

### Upload Flow:

1. **User** clicks Upload button or drops file
2. **View** shows file picker dialog, returns path to Presenter
3. **Presenter** creates `UploadWorker(QThread)` with file path
4. **Worker** runs in background, reads file with `ProgressFileReader`
5. **Worker** calls `S3FileService.upload_fileobj_to_prefix()`
6. **Worker** emits `progress` signal → updates progress dialog
7. **Worker** emits `finished` signal → Presenter refreshes view
8. **Presenter** calls `on_refresh_clicked()` to reload bucket contents

### Delete Flow:

1. **User** selects file, clicks Delete button
2. **View** confirms deletion with QMessageBox
3. **View** calls `presenter.handle_delete_file(filename)`
4. **Presenter** constructs full S3 key (prefix + filename)
5. **Presenter** calls `model.delete_file(key)`
6. **Model** calls `s3_service.delete_object(key)`
7. **Model** emits `file_deleted` signal
8. **Presenter** receives signal, calls `on_refresh_clicked()`

## Key Abstractions

### Qt Signal Communication
- **Purpose:** Decouple Model from Presenter (async notifications)
- **Defined in:** `ModelSignals` class in `src/mvp/base_model.py`
- **Signals:** `data_changed`, `data_loaded`, `error_occurred`, `file_deleted`, `folder_created`, etc.
- **Pattern:** Model emits → Presenter slot receives → View updates

### Worker Threads
- **Purpose:** Keep UI responsive during I/O operations
- **Defined in:** `src/presenters/bucket_browser_presenter.py`
- **Classes:** `UploadWorker`, `DownloadWorker` (both extend `QThread`)
- **Pattern:** Create worker → Connect signals → Start thread → Auto-cleanup on finish

### Error Hierarchy
- **Purpose:** Typed errors for specific S3 failure modes
- **Defined in:** `src/services/s3_errors.py`
- **Base:** `S3Error` → Specific errors (`S3AccessDeniedError`, `S3BucketNotFoundError`, etc.)
- **Pattern:** Service raises → Presenter catches → View shows user-friendly message

### Protocol Interfaces
- **Purpose:** Type safety without concrete dependencies
- **Defined in:** `src/mvp/contracts.py`
- **Protocols:** `IBucketObject`, `IBucketBrowserModel`, `IBucketBrowserView`, `IBucketBrowserPresenter`
- **Pattern:** Used for typing, enables mocking in tests

## Entry Points

### Main Application Entry
- **Location:** `src/main.py`
- **Function:** `main()`
- **Responsibilities:**
  - Configure logging (silence boto3 noise)
  - Create QApplication with forced light theme
  - Initialize ConfigManager, check first-time setup
  - Show setup wizard if needed
  - Create Model-View-Presenter triad
  - Start Qt event loop

### Build Entry
- **Location:** `build.py`
- **Purpose:** PyInstaller build script for executable creation

## Error Handling

**Strategy:** Exception-based with signal propagation for async operations

**Patterns:**
- Synchronous operations: Try/except at Presenter level, show error dialog
- Async operations (workers): Error signal → Presenter slot → View error display
- Model operations: Exceptions caught, converted to error signals

**Error Display:**
- `show_error(message)` - Simple status bar error
- `show_error_with_retry(message, on_retry)` - Error dialog with retry button

## State Management

**Configuration State:**
- Stored in SQLite database (`~/.config/BucketBrowser/config.db`)
- Managed by `ConfigManager` with Qt signals (`config_changed`, `config_saved`)
- Required keys: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `AWS_S3_BUCKET_NAME`

**Navigation State:**
- Stored in `BucketBrowserPresenter`: `_current_prefix`, `_continuation_token`, `_all_objects`
- Pagination: `_is_truncated`, `_continuation_token` for S3 pagination
- Search: `_search_query` with debounced filter application

## Cross-Cutting Concerns

**Logging:**
- Standard Python logging, console output
- boto3/botocore logs suppressed (WARNING level)
- Module-level loggers: `logging.getLogger(__name__)`

**Styling:**
- `src/utils/styles.py` - Centralized QSS styles
- `apply_style(app)` called in main before showing window
- Explicit light palette to prevent OS dark mode issues

**Icons:**
- `src/utils/file_icons.py` - `FileIconManager` class
- Custom-drawn icons using QPainter (no external assets)
- Caching: Icons cached in `_icon_cache` dict

**Drag & Drop:**
- Enabled on `BucketBrowserView` (`setAcceptDrops(True)`)
- Validation in Presenter: single file only, local files only
- Visual feedback: border highlight on drag enter

---

*Architecture analysis: 2026-04-04*
