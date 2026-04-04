# Codebase Concerns

**Analysis Date:** 2026-04-04

## Tech Debt

### S3Service Error Handling Duplication
- **Issue:** Every method in `S3FileService` (list_objects, upload_fileobj_to_prefix, delete_object, create_folder, download_fileobj) duplicates the same error handling pattern for ClientError, NoCredentialsError, EndpointConnectionError, and generic Exception.
- **Files:** `src/services/s3_service.py` (lines 128-141, 217-233, 252-270, 309-325, 367-385)
- **Impact:** ~80 lines of duplicated code; inconsistent error wrapping if modifications needed
- **Fix approach:** Create a decorator or context manager to handle S3 exceptions uniformly

### View Class Complexity (God Object)
- **Issue:** `BucketBrowserView` has grown to 1091 lines with mixed responsibilities (UI setup, dialog management, event handling, styling)
- **Files:** `src/views/bucket_browser_view.py`
- **Impact:** Difficult to maintain and test; violates Single Responsibility Principle
- **Fix approach:** Extract dialog classes into separate files (CreateFolderDialog already exists, move it out); create separate classes for toolbar, breadcrumb, and content area management

### Presenter Complexity
- **Issue:** `BucketBrowserPresenter` is 816 lines with multiple nested worker classes (UploadWorker, DownloadWorker, ProgressFileReader)
- **Files:** `src/presenters/bucket_browser_presenter.py`
- **Impact:** Hard to test individual worker behaviors; presenter knows too much about threading
- **Fix approach:** Extract worker classes to separate files in `src/workers/` directory; consider a worker factory pattern

### Configuration Manager Singleton
- **Issue:** Global singleton `_config_manager` in `config_manager.py` makes testing difficult and hides dependencies
- **Files:** `src/config/config_manager.py` (lines 238-251)
- **Impact:** Tests must manage global state; cannot easily swap configurations for testing
- **Fix approach:** Use dependency injection; pass ConfigManager instance through constructor chain from main.py

## Known Bugs

### None
- **Search audit found no TODO/FIXME/XXX comments in source code**

## Security Considerations

### AWS Credentials in Environment Variables
- **Risk:** `main.py` sets AWS credentials as environment variables (lines 143-145), which could leak to child processes or be visible in process listings
- **Files:** `src/main.py`
- **Current mitigation:** Credentials are loaded from encrypted SQLite database via ConfigManager
- **Recommendations:** Pass credentials directly to boto3 client instead of using environment variables; add credential rotation/expiration warnings

### Config Database Location
- **Risk:** SQLite database stored in user's home directory (`~/.config/BucketBrowser/config.db`) may be accessible by other users on shared systems
- **Files:** `src/config/config_manager.py` (lines 62-72)
- **Current mitigation:** Database permissions rely on OS defaults
- **Recommendations:** Set restrictive file permissions (0o600) on the database file; consider OS keychain integration for secrets

### File Upload Validation Missing
- **Risk:** No validation on file types, sizes, or content before upload to S3
- **Files:** `src/presenters/bucket_browser_presenter.py` (on_upload_clicked, on_files_dropped)
- **Current mitigation:** None
- **Recommendations:** Add optional file size limits; scan for malicious file extensions; validate MIME types

## Performance Bottlenecks

### S3 ListObjects Pagination
- **Problem:** `list_objects` method in S3FileService concatenates pages into memory before returning
- **Files:** `src/services/s3_service.py` (lines 84-142)
- **Cause:** Uses while loop to fetch all pages, collecting all results
- **Improvement path:** Implement true streaming/lazy loading; return generator or use callbacks for incremental updates

### Image Preview Loading
- **Problem:** Image preview downloads entire file to memory before displaying
- **Files:** `src/views/image_preview_dialog.py` (lines 85-109)
- **Cause:** Loads full image bytes via BytesIO; no size limit or progressive loading
- **Improvement path:** Add size limits for preview (e.g., 10MB max); implement thumbnail generation or streaming

### Search Filter Client-Side Only
- **Problem:** Search only filters already-loaded objects; does not search S3 prefix
- **Files:** `src/presenters/bucket_browser_presenter.py` (_apply_search_filter method, lines 405-416)
- **Cause:** S3 ListObjectsV2 API doesn't support content search; prefix matching only
- **Limitation:** Cannot be fixed without building separate indexing service; document this limitation

## Fragile Areas

### Signal/Slot Connection Chain
- **Files:** `src/mvp/base_presenter.py` (lines 24-28), `src/mvp/base_model.py` (lines 27-60)
- **Why fragile:** Multiple signal connections between Model-Presenter-View; if signals not properly disconnected on cleanup, can cause crashes when accessing deleted objects
- **Safe modification:** Always ensure worker threads complete and signals are disconnected before view destruction; add try/except in signal handlers
- **Test coverage:** Limited tests for signal cleanup scenarios

### Drag-and-Drop Validation
- **Files:** `src/presenters/bucket_browser_presenter.py` (on_drag_enter, on_drag_move, on_files_dropped, lines 471-601)
- **Why fragile:** Complex validation logic spread across multiple methods; relies on Qt's mimeData handling which varies by platform
- **Safe modification:** Add integration tests with actual file drops; test on all target platforms (Windows, macOS, Linux)
- **Test coverage:** Test coverage exists but mocked; real drag-drop behavior not verified

### Bucket Object Icon Type Detection
- **Files:** `src/models/bucket_object.py` (get_icon_type, lines 40-67)
- **Why fragile:** Simple extension-based detection; can misidentify files with no extension or unusual extensions
- **Safe modification:** Add MIME type detection as fallback; use python-magic library for robust type detection
- **Test coverage:** Tests exist for file_icons.py but not for edge cases like no-extension files

## Scaling Limits

### S3 Object Listing
- **Current capacity:** Loads up to 50 objects per API call; concatenates all pages
- **Limit:** Memory bound by available RAM; will fail for buckets with millions of objects
- **Scaling path:** Implement virtual scrolling with on-demand loading; remove pagination concatenation in list_objects

### Concurrent Uploads/Downloads
- **Current capacity:** Single upload or download at a time (workers cancelled before new operation)
- **Limit:** User cannot queue multiple operations
- **Scaling path:** Implement operation queue; allow parallel transfers with bandwidth limiting

### SQLite Database
- **Current capacity:** Single-user local configuration storage
- **Limit:** Not designed for concurrent access or cloud sync
- **Scaling path:** Consider cloud-based config sync for multi-device usage (future feature)

## Dependencies at Risk

### PySide6 Version Pinning
- **Risk:** `PySide6>=6.6.0` allows major version updates that may break API compatibility
- **Impact:** Signal/slot syntax or widget behavior changes could cause runtime errors
- **Migration plan:** Pin to minor version (e.g., `~=6.6.0`); add CI tests with latest PySide6 version

### boto3 Botocore Compatibility
- **Risk:** boto3's underlying botocore library may deprecate API response formats
- **Impact:** Error code parsing (e.g., lines 129-135 in s3_service.py) depends on specific response structure
- **Migration plan:** Use boto3's built-in exception types where possible; add response validation tests

## Missing Critical Features

### Folder Deletion
- **Problem:** Users cannot delete folders; error message shown but no recursive delete option
- **Files:** `src/views/bucket_browser_view.py` (lines 574-583)
- **Blocks:** Managing folder lifecycle in S3 buckets

### Batch Operations
- **Problem:** Cannot select and delete/download multiple files at once
- **Files:** `src/views/bucket_browser_view.py` (selection behavior set to single row)
- **Blocks:** Efficient bulk file management

### File Rename/Move
- **Problem:** No ability to rename files or move between folders
- **Blocks:** File organization workflows

### Upload Progress for Multiple Files
- **Problem:** Drag-drop only supports single file; upload dialog only allows single selection
- **Blocks:** Batch upload workflows

## Test Coverage Gaps

### Config Presenter Error Handling
- **What's not tested:** Error paths in ConfigPresenter when database operations fail
- **Files:** `src/presenters/config_presenter.py`
- **Risk:** SQLite errors (disk full, permission denied) not handled gracefully
- **Priority:** Medium

### Image Preview Error Paths
- **What's not tested:** Malformed image data handling; very large image handling
- **Files:** `src/views/image_preview_dialog.py`
- **Risk:** Application crash on corrupted image files
- **Priority:** Low

### Network Failure Scenarios
- **What's not tested:** Intermittent network failures during long uploads/downloads; retry exhaustion
- **Files:** `src/presenters/bucket_browser_presenter.py` (worker error handling)
- **Risk:** Partial uploads leave orphaned multipart uploads in S3 (cost implication)
- **Priority:** High

### Cross-Platform Path Handling
- **What's not tested:** Windows path separators, Unicode filenames, path length limits
- **Files:** `src/services/s3_service.py` (key construction)
- **Risk:** Filename corruption or upload failures on Windows
- **Priority:** Medium

## Code Quality Issues

### Dead Code
- **Issue:** `CreateFolderDialog` has `_on_search_text_changed` and `set_on_search_callback` methods (lines 1076-1091) that are never used; these are likely copy-paste errors from the main view
- **Files:** `src/views/bucket_browser_view.py`

### Incomplete Methods
- **Issue:** Several presenter methods are empty stubs (pass statements)
- **Files:** `src/presenters/config_presenter.py` (lines 61, 103, 119, 136, 146)
- **Impact:** Unclear if these are intentional no-ops or incomplete implementations

### Inconsistent Error Handling
- **Issue:** Some methods catch generic Exception and wrap it; others let exceptions bubble up
- **Example:** `handle_delete_file` catches Exception (line 632) but `handle_preview_request` has specific S3 error catches (lines 788-799)
- **Recommendation:** Standardize error handling strategy across all user-facing operations

---

*Concerns audit: 2026-04-04*
