# Phase 1: Foundation

**Phase:** 1  
**Wave:** 1  
**Depends On:** (none - first phase)  
**Files Modified:** 
- src/services/s3_service.py
- src/services/s3_errors.py
- src/views/bucket_browser_view.py
- src/presenters/bucket_browser_presenter.py
- src/views/generate_link_dialog.py (new file)

---

## Objective

Add right-click context menu and basic pre-signed URL generation capability. User can right-click any file, select "Generate Link", and see a valid pre-signed URL in a modal dialog.

---

## Requirements Addressed

- **URL-01**: Context menu with "Generate Link" option
- **URL-03**: Generate pre-signed URL via boto3
- **URL-04**: Display URL in modal dialog
- **UI-01**: Right-click context menu on file rows
- **UI-04**: Loading state during generation

---

## Tasks

### Task 1: Add S3FileService.generate_presigned_url() method

<read_first>
- src/services/s3_service.py (existing S3FileService class)
- src/services/s3_errors.py (existing error hierarchy)
</read_first>

<action>
Add the `generate_presigned_url()` method to the S3FileService class in src/services/s3_service.py after the download_fileobj method (around line 385).

The method should:
1. Accept parameters: `key: str`, `expiration_hours: int = 1`
2. Generate a pre-signed URL using boto3's `generate_presigned_url()` method
3. Handle ClientError exceptions and convert to appropriate S3Error types
4. Return the pre-signed URL string

Also add `S3PresignedUrlError` exception class to src/services/s3_errors.py following the existing pattern (similar to S3DownloadError).

Method signature:
```python
def generate_presigned_url(self, key: str, expiration_hours: int = 1) -> str:
    """Generate a pre-signed URL for downloading an S3 object.
    
    Creates a temporary URL that allows access to the object without
    AWS credentials. The URL expires after the specified duration.
    
    Args:
        key: The S3 key (path) of the object
        expiration_hours: URL validity duration in hours (default: 1, max: 168)
        
    Returns:
        Pre-signed URL string
        
    Raises:
        S3AccessDeniedError: If credentials lack bucket read permission
        S3BucketNotFoundError: If bucket doesn't exist
        S3ObjectNotFoundError: If object doesn't exist in bucket
        S3CredentialsError: If AWS credentials are missing/invalid
        S3ConnectionError: If cannot connect to AWS
        S3PresignedUrlError: If URL generation fails for other reasons
    """
```
</action>

<acceptance_criteria>
- src/services/s3_service.py contains `def generate_presigned_url(self, key: str, expiration_hours: int = 1) -> str:` method
- Method uses `self._s3.generate_presigned_url('get_object', ...)` with ExpiresIn calculated as `expiration_hours * 3600`
- Method handles ClientError with error_code checks for '403', 'AccessDenied', '404', 'NoSuchBucket', 'NoSuchKey'
- src/services/s3_errors.py contains `class S3PresignedUrlError(S3Error):` with proper constructor
- All error cases raise appropriate S3Error subclasses
</acceptance_criteria>

---

### Task 2: Create GenerateLinkDialog class

<read_first>
- src/views/image_preview_dialog.py (reference for dialog structure)
- src/utils/styles.py (for consistent styling)
</read_first>

<action>
Create new file src/views/generate_link_dialog.py with the GenerateLinkDialog class.

The dialog should:
1. Extend QDialog
2. Accept filename and generated URL as constructor parameters
3. Display the filename prominently at the top
4. Show the full URL in a read-only QLineEdit (selectable, copyable)
5. Include a "Close" button
6. Set minimum size of 500x200 pixels
7. Make URL text selectable for manual copy
8. Follow existing dialog patterns from ImagePreviewDialog

Dialog structure:
- Title: "Generate Link - {filename}"
- Label: "Pre-signed URL (expires in 1 hour):"
- URL display: read-only QLineEdit with the URL
- Close button: QPushButton that closes the dialog

Apply consistent styling using the application's style patterns.
</action>

<acceptance_criteria>
- File src/views/generate_link_dialog.py exists
- Class `GenerateLinkDialog(QDialog)` is defined
- Constructor signature: `__init__(self, filename: str, url: str, parent=None)`
- Dialog displays filename in window title: `f"Generate Link - {filename}"`
- Dialog contains QLineEdit displaying the URL with `setReadOnly(True)`
- Dialog has Close button that calls `self.accept()`
- Dialog minimum size is 500x200 pixels
</acceptance_criteria>

---

### Task 3: Add context menu to BucketBrowserView

<read_first>
- src/views/bucket_browser_view.py (table setup and event handling)
- PySide6.QtWidgets.QMenu documentation for context menu
</read_first>

<action>
Add context menu support to the table in BucketBrowserView.

In src/views/bucket_browser_view.py:
1. Import QMenu from PySide6.QtWidgets (add to existing imports)
2. In _setup_table() method, set table context menu policy: `self._table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)`
3. Connect the customContextMenuRequested signal to a new handler: `self._table.customContextMenuRequested.connect(self._on_table_context_menu)`
4. Add callback handler `_on_table_context_menu(self, position)` that:
   - Gets the selected row at the click position
   - Checks if a file (not folder) is selected
   - Creates QMenu with "Generate Link" action
   - Calls presenter method when action is triggered

Add presenter callback pattern (similar to other callbacks in the view):
- Add `_on_generate_link_callback: Optional[callable] = None` in __init__
- Add `set_on_generate_link_callback(self, callback: callable)` method
- Call `self._on_generate_link_callback(filename)` when "Generate Link" is selected

Ensure the context menu only appears for files (not folders) and when a row is selected.
</action>

<acceptance_criteria>
- src/views/bucket_browser_view.py imports QMenu
- _setup_table() sets `self._table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)`
- _setup_table() connects `self._table.customContextMenuRequested.connect(self._on_table_context_menu)`
- Method `_on_table_context_menu(self, position)` exists and handles right-click
- Method checks if selected item is a file (not folder) before showing menu
- Context menu contains QAction with text "Generate Link"
- View has `set_on_generate_link_callback(self, callback: callable)` method
- When "Generate Link" is clicked, it calls the callback with the filename
</acceptance_criteria>

---

### Task 4: Add presenter methods for link generation

<read_first>
- src/presenters/bucket_browser_presenter.py (existing presenter structure)
- src/presenters/bucket_browser_presenter.py (UploadWorker/DownloadWorker patterns)
</read_first>

<action>
Add methods to BucketBrowserPresenter for handling link generation.

In src/presenters/bucket_browser_presenter.py:

1. Add callback registration in view setup:
   - In the presenter initialization, call `self._view.set_on_generate_link_callback(self._on_generate_link_clicked)`

2. Add `_on_generate_link_clicked(self, filename: str)` method that:
   - Constructs the full S3 key using current prefix and filename
   - Calls `self._generate_link(key)`

3. Add `_generate_link(self, key: str)` method that:
   - Shows loading state via view
   - Calls `self._s3_service.generate_presigned_url(key, expiration_hours=1)`
   - On success: extracts filename from key, calls `self._view.show_generate_link_dialog(filename, url)`
   - On error: catches S3Error exceptions, shows error via `self._view.show_error()`
   - Finally: hides loading state

4. Import GenerateLinkDialog at top of file

Follow the existing error handling pattern used in handle_delete_file() and handle_download_file().
</action>

<acceptance_criteria>
- Presenter calls `self._view.set_on_generate_link_callback(self._on_generate_link_clicked)` during initialization
- Method `_on_generate_link_clicked(self, filename: str)` exists and constructs S3 key
- Method `_generate_link(self, key: str)` exists and handles URL generation
- Method calls `self._s3_service.generate_presigned_url(key, expiration_hours=1)`
- On success, calls `self._view.show_generate_link_dialog(filename, url)`
- On S3Error, calls `self._view.show_error(str(error))`
- Loading state is shown/hidden around the operation
</acceptance_criteria>

---

### Task 5: Add show_generate_link_dialog to view

<read_first>
- src/views/bucket_browser_view.py (existing dialog methods)
- src/views/generate_link_dialog.py (the dialog created in Task 2)
</read_first>

<action>
Add the show_generate_link_dialog method to BucketBrowserView.

In src/views/bucket_browser_view.py:

1. Import GenerateLinkDialog at the top (with other dialog imports)

2. Add method:
```python
def show_generate_link_dialog(self, filename: str, url: str) -> None:
    """Show dialog with generated pre-signed URL.
    
    Args:
        filename: Name of the file
        url: The pre-signed URL
    """
    dialog = GenerateLinkDialog(filename, url, self)
    dialog.exec()
```

3. Ensure the dialog is modal (blocks interaction with main window until closed)

Follow the same pattern as show_image_preview() method.
</action>

<acceptance_criteria>
- src/views/bucket_browser_view.py imports GenerateLinkDialog
- Method `show_generate_link_dialog(self, filename: str, url: str)` exists
- Method creates GenerateLinkDialog with filename and url parameters
- Method calls dialog.exec() to show modal dialog
</acceptance_criteria>

---

### Task 6: Add loading state during URL generation

<read_first>
- src/views/bucket_browser_view.py (existing show_loading method)
</read_first>

<action>
Ensure loading state is properly shown during URL generation.

In src/presenters/bucket_browser_presenter.py, verify the _generate_link method:
1. Calls `self._view.show_loading(True)` before starting URL generation
2. Calls `self._view.show_loading(False)` in a finally block after generation completes (success or error)

The view's show_loading() method should already exist and update the status label. Verify it works correctly by checking that:
- When called with True: status label shows "Loading..."
- When called with False: status label returns to "Ready" or previous state

No changes needed to view if show_loading() already exists (which it should from existing code).
</action>

<acceptance_criteria>
- Presenter's `_generate_link()` method calls `self._view.show_loading(True)` before S3 call
- Presenter's `_generate_link()` method has try/finally block
- Finally block calls `self._view.show_loading(False)`
- View's show_loading() method updates status label text
</acceptance_criteria>

---

## Verification

### Manual Testing Steps

1. Launch application and navigate to a bucket with files
2. Right-click on a file (not folder)
3. Verify context menu appears with "Generate Link" option
4. Click "Generate Link"
5. Verify loading indicator shows briefly
6. Verify modal dialog opens showing:
   - Title: "Generate Link - {filename}"
   - The full pre-signed URL
7. Verify URL can be selected/copied from the dialog
8. Verify URL works when pasted in browser (downloads file)
9. Click Close button - dialog should close

### Error Cases to Test

1. Right-click on folder - no "Generate Link" option should appear
2. Right-click on empty space - no context menu should appear
3. Generate link with no network - error message should display
4. Generate link for deleted file - error message should display

---

## Must-Haves

- [ ] Context menu infrastructure in view layer
- [ ] S3FileService.generate_presigned_url() method
- [ ] GenerateLinkDialog for URL display
- [ ] Presenter methods to wire view to service
- [ ] Error handling for S3 API failures
- [ ] Loading state during generation

---

## Implementation Notes

**MVP Pattern Compliance:**
- View: Shows context menu, displays dialog
- Presenter: Handles user action, calls service, updates view
- Service: Generates pre-signed URL via boto3
- Model: BucketObject data used for determining file vs folder

**boto3 generate_presigned_url Parameters:**
```python
url = self._s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': self.bucket_name, 'Key': key},
    ExpiresIn=expiration_hours * 3600
)
```

**Qt Context Menu:**
- Use `Qt.ContextMenuPolicy.CustomContextMenu`
- Signal: `customContextMenuRequested(QPoint)`
- Map position to row: `table.rowAt(position.y())`

**Security Note:**
- Pre-signed URLs are temporary (default 1 hour)
- No URL persistence (as per requirement URL-10)
- URLs generated fresh each time (no caching)

---

*Plan created: 2025-01-20*