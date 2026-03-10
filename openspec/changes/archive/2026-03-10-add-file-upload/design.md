## Context

The application follows an MVP (Model-View-Presenter) architecture using PySide6. Currently, the bucket browser allows users to navigate folders and view files, but lacks file upload functionality. The view already has an "Upload" button placeholder that calls `presenter.on_upload_clicked()`, but the presenter method is empty.

**Current State:**
- View: Has upload button in toolbar (line 91-94 in bucket_browser_view.py)
- Presenter: `on_upload_clicked()` is a placeholder (line 222-226)
- Model: No upload method exists
- S3 Service: No upload method exists

## Goals / Non-Goals

**Goals:**
- Allow users to upload a single file to the current folder location
- Show upload progress with percentage (0-100%)
- Use background thread to prevent UI blocking during upload
- Refresh file list after successful upload
- Handle errors gracefully with user feedback

**Non-Goals:**
- Multiple file upload
- Drag-and-drop upload
- Folder upload
- Pause/resume upload capability

## Decisions

### 1. File Picker Dialog
**Decision:** Use PySide6's `QFileDialog.getOpenFileName()` for file selection.
**Rationale:** Native OS file picker provides best user experience. Single file selection aligns with MVP scope.

### 2. Upload Destination Logic
**Decision:** Upload to the current prefix path (`self._current_prefix` in presenter).
**Rationale:** User is already viewing the destination folder, so uploading "here" is intuitive. The presenter tracks current location via `_current_prefix`.

### 3. Threading Architecture
**Decision:** Use `QThread` with a worker object that emits progress signals.
**Rationale:** 
- PySide6's `QThread` integrates natively with signal/slot mechanism
- Keeps UI responsive during large file uploads
- Progress updates via `pyqtSignal(int)` for percentage
- Clean separation: worker handles S3 upload, main thread handles UI

**Implementation Pattern:**
```python
class UploadWorker(QObject):
    progress = Signal(int)  # 0-100
    completed = Signal()
    error = Signal(str)
    
    def upload(self, file_path, destination):
        # Use S3 multipart upload with callback
        s3.upload_file(file_path, bucket, key, 
                      Callback=self._on_progress)
    
    def _on_progress(self, bytes_transferred):
        percentage = (bytes_transferred / total) * 100
        self.progress.emit(percentage)
```

### 4. S3 Upload Method with Progress
**Decision:** Use `boto3`'s `upload_file()` with `Callback` for progress tracking.
**Rationale:** 
- `upload_file` automatically handles multipart upload for large files
- `Callback` function called periodically with bytes transferred
- Enables accurate percentage calculation
- More efficient than `put_object` for files > 8MB

### 5. Progress UI
**Decision:** Use `QProgressDialog` with cancel button.
**Rationale:**
- Native Qt dialog with progress bar
- Built-in cancel button to abort upload
- Modal dialog prevents other interactions during upload
- Auto-closes on completion

### 6. Error Handling Strategy
**Decision:** Follow existing pattern in presenter - use `show_error()` for simple errors, `show_error_with_retry()` for recoverable errors.
**Rationale:** Consistent with existing S3 error handling (access denied, connection errors, etc.).

### 7. Signal-Based Communication
**Decision:** 
- Worker emits: `progress(int)`, `completed()`, `error(str)`
- Presenter connects worker signals to view methods
- Model coordinates worker lifecycle (start/stop)

**Rationale:** Clean separation of concerns, thread-safe communication via Qt's queued connections.

## Risks / Trade-offs

- **[Risk]** Thread management complexity → **Mitigation:** Use `QObject.moveToThread()` pattern, proper cleanup with `worker.deleteLater()`
- **[Risk]** Progress callback frequency → **Mitigation:** S3 calls callback every ~8MB, sufficient for large files
- **[Risk]** Cancel upload mid-way → **Mitigation:** Implement thread-safe cancellation flag
- **[Risk]** File with same name exists → **Mitigation:** S3 overwrites by default, acceptable for MVP

## Migration Plan

Not applicable - this is a new feature with no breaking changes.

## Open Questions

None - requirements are clear for MVP scope.
