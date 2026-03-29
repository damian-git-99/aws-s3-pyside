## Context

The application follows an MVP (Model-View-Presenter) architecture using PySide6. The bucket browser displays S3 objects in a table with a toolbar containing action buttons (Download, Delete, Upload, etc.).

Currently, users must download images to their local filesystem to view them. This design adds an in-app preview capability that downloads images to memory and displays them in a modal dialog.

### Current Architecture

```
┌─────────────────────────────────────────────────────────┐
│  BucketBrowserView                                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Toolbar: [Home] [Up] [Refresh] [Upload]         │   │
│  │          [Delete] [Download] [Settings]         │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Table: Name | Size | Modified | Storage Class   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
              BucketBrowserPresenter
                           │
                           ▼
                 S3FileService (boto3)
```

The existing `BucketObject.get_icon_type()` already identifies image files by extension (jpg, jpeg, png, gif, bmp, svg, webp). The `S3FileService.download_fileobj()` method supports downloading to file-like objects (BytesIO).

## Goals / Non-Goals

**Goals:**
- Add a Preview button to the toolbar that enables only for image files
- Open a modal dialog displaying the selected image
- Download images from S3 to memory (not filesystem) for preview
- Support all common image formats (jpg, png, gif, bmp, svg, webp)
- Show loading state while fetching image from S3
- Graceful error handling for failed downloads

**Non-Goals:**
- Image editing capabilities
- Zoom/pan functionality (scroll is sufficient)
- Previewing non-image files (PDFs, videos, etc.)
- Caching previewed images
- Full-screen mode

## Decisions

### Decision: Use QDialog with QLabel + QPixmap for image display

**Rationale:**
- QLabel with QPixmap is the standard PySide6 way to display images
- QDialog provides modal behavior and built-in window controls
- ScrollArea can be added for large images

**Alternatives considered:**
- Custom widget with OpenGL rendering → Overkill for simple preview
- External image viewer → Requires temp files, breaks in-app experience

### Decision: Download to BytesIO in memory, not temporary files

**Rationale:**
- No cleanup needed (no temp files left behind)
- Faster (no disk I/O)
- Works with existing `download_fileobj()` method
- Security (no files written to disk)

**Trade-off:** Large images consume memory, but acceptable for MVP

### Decision: Button state managed by View based on selection

**Rationale:**
- Consistent with existing Delete/Download button patterns
- View has direct access to selection model
- Reduces Presenter complexity

**Implementation:**
- Connect to table's `itemSelectionChanged` signal
- Check if selected row is an image via `BucketObject.get_icon_type()`
- Enable/disable Preview button accordingly

### Decision: Async download with loading indicator

**Rationale:**
- S3 operations can be slow (network latency)
- Blocking UI would freeze the application
- Consistent with existing upload/download patterns (workers)

**Implementation approach:**
```python
# Presenter creates worker thread
worker = PreviewDownloadWorker(s3_service, key)
worker.finished.connect(self._on_preview_data_ready)
worker.start()
```

Or simpler: use existing pattern with callback and show modal immediately with loading state.

## Risks / Trade-offs

**[Risk]** Large images (>100MB) could cause memory issues
- **Mitigation:** Set a reasonable max size limit (e.g., 50MB). Show error for oversized images.

**[Risk]** SVG rendering may have platform differences
- **Mitigation:** Use QSvgRenderer if available, fallback to generic icon for unsupported SVGs

**[Risk]** Animated GIFs will only show first frame
- **Mitigation:** Document this limitation. Full animation support is out of scope.

**[Risk]** Slow network could make preview feel unresponsive
- **Mitigation:** Show loading spinner immediately with cancel option

## Implementation Sketch

### View Changes (`bucket_browser_view.py`)

```python
# In _setup_toolbar()
self._preview_btn = QPushButton("Preview")
self._preview_btn.setObjectName("preview_btn")
self._preview_btn.setEnabled(False)  # Disabled by default
self._preview_btn.clicked.connect(self._on_preview_clicked)
self._toolbar.addWidget(self._preview_btn)

# New method
@property
def is_image_selected(self) -> bool:
    """Check if currently selected item is an image."""
    # Get selected row, check BucketObject.get_icon_type() == 'image'
    pass

def enable_preview_button(self, enabled: bool) -> None:
    """Enable/disable preview button."""
    if self._preview_btn:
        self._preview_btn.setEnabled(enabled)

def show_image_preview(self, image_data: bytes, filename: str) -> None:
    """Open modal dialog with image preview."""
    dialog = ImagePreviewDialog(image_data, filename, self)
    dialog.exec()
```

### New File: `views/image_preview_dialog.py`

```python
class ImagePreviewDialog(QDialog):
    """Modal dialog for previewing images."""
    
    def __init__(self, image_data: bytes, filename: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Preview - {filename}")
        self.resize(800, 600)
        
        # Layout with scroll area
        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        label.setPixmap(pixmap)
        scroll.setWidget(label)
        layout.addWidget(scroll)
```

### Presenter Changes (`bucket_browser_presenter.py`)

```python
def handle_preview_request(self, filename: str) -> None:
    """Handle preview button click."""
    key = self._current_prefix + filename if self._current_prefix else filename
    
    # Show loading dialog or update status
    self._view.show_loading(True)
    
    try:
        buffer = BytesIO()
        self._s3_service.download_fileobj(key, buffer)
        buffer.seek(0)
        self._view.show_image_preview(buffer.getvalue(), filename)
    except Exception as e:
        self._view.show_error(f"Failed to load preview: {e}")
    finally:
        self._view.show_loading(False)
```

## Open Questions

None - design is ready for implementation.
