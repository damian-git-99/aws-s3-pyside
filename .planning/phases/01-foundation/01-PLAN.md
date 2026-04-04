# Phase 1: Generate Pre-signed Links

**Phase:** 1  
**Wave:** 1  
**Depends On:** (none)  
**Files Modified:** 
- src/services/s3_service.py
- src/services/s3_errors.py
- src/views/bucket_browser_view.py
- src/presenters/bucket_browser_presenter.py
- src/views/generate_link_dialog.py (new file)

---

## Objective

Add a "Generate Link" button to the toolbar. When clicked with a file selected, opens a dialog to generate pre-signed URLs with configurable expiration. User can generate URL and copy to clipboard.

---

## Requirements

- User clicks "Generate Link" button in toolbar
- If no file selected → error message
- If folder selected → error message (links only for files)
- Dialog opens with:
  - Selected filename displayed
  - Expiration dropdown (1 hour, 1 day, 7 days, 30 days)
  - "Generate" button
  - Generated URL display area (hidden until generated)
  - "Copy to Clipboard" button (enabled after generation)
  - "Close" button
- URL is copied when user clicks "Copy"

---

## Tasks

### Task 1: Add S3FileService.generate_presigned_url() method

<read_first>
- src/services/s3_service.py
- src/services/s3_errors.py
</read_first>

<action>
Add method to S3FileService class:

```python
def generate_presigned_url(self, key: str, expiration_hours: int = 1) -> str:
    """Generate a pre-signed URL for downloading an S3 object."""
    try:
        url = self._s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key},
            ExpiresIn=expiration_hours * 3600
        )
        return url
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code in ('403', 'AccessDenied'):
            raise S3AccessDeniedError(self.bucket_name) from e
        elif error_code in ('404', 'NoSuchBucket'):
            raise S3BucketNotFoundError(self.bucket_name) from e
        elif error_code == 'NoSuchKey':
            raise S3ObjectNotFoundError(key) from e
        else:
            raise S3PresignedUrlError(key, str(e)) from e
    except NoCredentialsError as e:
        raise S3CredentialsError() from e
    except EndpointConnectionError as e:
        raise S3ConnectionError() from e
```

Add to src/services/s3_errors.py:
```python
class S3PresignedUrlError(S3Error):
    """Error generating pre-signed URL."""
    def __init__(self, key: str, message: str = ""):
        self.key = key
        super().__init__(f"Failed to generate link for '{key}': {message}")
```
</action>

<acceptance_criteria>
- S3FileService has generate_presigned_url method
- Method accepts key and expiration_hours parameters
- Method returns pre-signed URL string
- All error cases raise appropriate S3Error
- S3PresignedUrlError class exists in s3_errors.py
</acceptance_criteria>

---

### Task 2: Create GenerateLinkDialog

<read_first>
- src/views/image_preview_dialog.py (reference)
</read_first>

<action>
Create src/views/generate_link_dialog.py:

```python
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard


class GenerateLinkDialog(QDialog):
    """Dialog for generating pre-signed URLs."""
    
    def __init__(self, filename: str, parent=None):
        super().__init__(parent)
        self._filename = filename
        self._generated_url = ""
        self.setWindowTitle(f"Generate Link - {filename}")
        self.setModal(True)
        self.resize(600, 250)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Filename label
        file_label = QLabel(f"File: <b>{self._filename}</b>")
        layout.addWidget(file_label)
        
        # Expiration selection
        expiration_layout = QHBoxLayout()
        expiration_label = QLabel("Link expires in:")
        self._expiration_combo = QComboBox()
        self._expiration_combo.addItem("1 hour", 1)
        self._expiration_combo.addItem("1 day", 24)
        self._expiration_combo.addItem("7 days", 168)
        self._expiration_combo.addItem("30 days", 720)
        expiration_layout.addWidget(expiration_label)
        expiration_layout.addWidget(self._expiration_combo)
        expiration_layout.addStretch()
        layout.addLayout(expiration_layout)
        
        # Generate button
        self._generate_btn = QPushButton("Generate Link")
        self._generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(self._generate_btn)
        
        # URL display (hidden initially)
        url_label = QLabel("Generated URL:")
        layout.addWidget(url_label)
        
        self._url_input = QLineEdit()
        self._url_input.setReadOnly(True)
        self._url_input.setPlaceholderText("Click 'Generate Link' to create URL")
        layout.addWidget(self._url_input)
        
        # Copy button (disabled initially)
        self._copy_btn = QPushButton("Copy to Clipboard")
        self._copy_btn.setEnabled(False)
        self._copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        layout.addWidget(self._copy_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def get_selected_expiration_hours(self) -> int:
        """Return selected expiration in hours."""
        return self._expiration_combo.currentData()
    
    def set_generated_url(self, url: str):
        """Display the generated URL."""
        self._generated_url = url
        self._url_input.setText(url)
        self._copy_btn.setEnabled(True)
    
    def get_generate_button(self) -> QPushButton:
        """Return generate button for connecting signals."""
        return self._generate_btn
    
    def get_copy_button(self) -> QPushButton:
        """Return copy button for connecting signals."""
        return self._copy_btn
    
    def copy_to_clipboard(self):
        """Copy URL to clipboard and show confirmation."""
        if self._generated_url:
            clipboard = QClipboard()
            clipboard.setText(self._generated_url)
            QMessageBox.information(self, "Copied", "Link copied to clipboard!")
```
</action>

<acceptance_criteria>
- GenerateLinkDialog class exists in src/views/generate_link_dialog.py
- Dialog shows filename in title
- Dialog has expiration dropdown with 4 options
- Dialog has Generate, Copy, and Close buttons
- URL display shows placeholder until generated
- Copy button is disabled until URL is generated
</acceptance_criteria>

---

### Task 3: Add "Generate Link" button to toolbar

<read_first>
- src/views/bucket_browser_view.py (_setup_toolbar method)
</read_first>

<action>
Add button to toolbar in _setup_toolbar() method, after Preview button (line 255) and before Settings button:

```python
# Generate Link button - creates pre-signed URL for selected file
self._generate_link_btn = QPushButton("Generate Link")
self._generate_link_btn.setObjectName("generate_link_btn")
self._generate_link_btn.setFixedSize(100, 28)
self._generate_link_btn.setEnabled(False)  # Disabled by default
self._generate_link_btn.setStyleSheet("""
    QPushButton {
        background-color: #f39c12;
        color: white;
        border: none;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #e67e22;
    }
    QPushButton:disabled {
        background-color: #bdc3c7;
        color: #7f8c8d;
    }
""")
self._generate_link_btn.clicked.connect(self._on_generate_link_clicked)
self._toolbar.addWidget(self._generate_link_btn)
```

Add callback handler:
```python
def _on_generate_link_clicked(self) -> None:
    """Handle Generate Link button click."""
    if not self._presenter:
        return
    
    selected_rows = self._table.selectionModel().selectedRows()
    if not selected_rows:
        self.show_error("Please select a file first")
        return
    
    row = selected_rows[0].row()
    name_item = self._table.item(row, 0)
    if not name_item:
        return
    
    filename = name_item.text()
    
    # Check if folder
    is_folder = False
    for obj in getattr(self, "_current_data", []):
        if obj.name == filename:
            is_folder = obj.is_folder
            break
    
    if is_folder:
        self.show_error("Please select a file, not a folder")
        return
    
    self._presenter.handle_generate_link(filename)
```

Add method to enable/disable button:
```python
def enable_generate_link_button(self, enabled: bool) -> None:
    """Enable or disable the generate link button."""
    if self._generate_link_btn:
        self._generate_link_btn.setEnabled(enabled)
```

Update selection change handler to enable button for files:
```python
def _on_selection_changed(self) -> None:
    """Handle table selection change."""
    selected_rows = self._table.selectionModel().selectedRows()
    if not selected_rows:
        self.enable_preview_button(False)
        self.enable_generate_link_button(False)
        return
    
    row = selected_rows[0].row()
    name_item = self._table.item(row, 0)
    if not name_item:
        return
    
    filename = name_item.text()
    
    # Find the object
    for obj in getattr(self, "_current_data", []):
        if obj.name == filename:
            is_image = obj.get_icon_type() == "image"
            is_folder = obj.is_folder
            self.enable_preview_button(is_image and not is_folder)
            self.enable_generate_link_button(not is_folder)
            break
```

Import GenerateLinkDialog at top of file.
</action>

<acceptance_criteria>
- Toolbar has "Generate Link" button with orange color (#f39c12)
- Button is disabled by default
- Button is enabled when a file (not folder) is selected
- Button is disabled when a folder is selected
- Button click calls presenter method with filename
</acceptance_criteria>

---

### Task 4: Add presenter logic

<read_first>
- src/presenters/bucket_browser_presenter.py
</read_first>

<action>
Add to BucketBrowserPresenter:

```python
def handle_generate_link(self, filename: str) -> None:
    """Handle generate link request from view."""
    # Construct full S3 key
    if self._current_prefix:
        key = f"{self._current_prefix}{filename}"
    else:
        key = filename
    
    # Show dialog
    from src.views.generate_link_dialog import GenerateLinkDialog
    dialog = GenerateLinkDialog(filename, self._view)
    
    # Connect generate button
    dialog.get_generate_button().clicked.connect(
        lambda: self._generate_link(dialog, key)
    )
    
    # Connect copy button
    dialog.get_copy_button().clicked.connect(dialog.copy_to_clipboard)
    
    dialog.exec()

def _generate_link(self, dialog, key: str) -> None:
    """Generate the pre-signed URL."""
    try:
        self._view.show_loading(True)
        
        expiration_hours = dialog.get_selected_expiration_hours()
        url = self._s3_service.generate_presigned_url(key, expiration_hours)
        
        dialog.set_generated_url(url)
        self._view.show_message("Link generated successfully")
        
    except S3Error as e:
        self._view.show_error(str(e))
    finally:
        self._view.show_loading(False)
```
</action>

<acceptance_criteria>
- Presenter has handle_generate_link method
- Method constructs full S3 key from current prefix + filename
- Method creates and shows GenerateLinkDialog
- Generate button connected to _generate_link method
- Copy button connected to dialog's copy_to_clipboard method
- _generate_link gets expiration from dialog
- _generate_link calls s3_service.generate_presigned_url
- Loading state shown during generation
- Errors shown via show_error
</acceptance_criteria>

---

## Verification

1. Launch app
2. Select a file (not folder)
3. Click "Generate Link" button
4. Dialog opens showing filename
5. Select expiration (e.g., 7 days)
6. Click "Generate"
7. URL appears in text field
8. Click "Copy to Clipboard"
9. Confirmation message appears
10. Paste URL in browser → file downloads
11. Close dialog

---

## Success Criteria

- [ ] "Generate Link" button visible in toolbar
- [ ] Button disabled when no selection or folder selected
- [ ] Dialog opens with filename and expiration options
- [ ] URL generates successfully
- [ ] URL can be copied to clipboard
- [ ] Copied URL works in browser
- [ ] Error handling works for network/permission issues

---

*Plan simplified for single-phase implementation*