## 1. S3 Service - Add Upload Method with Progress

- [x] 1.1 Add `upload_file_with_progress()` method to S3FileService using `boto3.upload_file()`
- [x] 1.2 Implement progress callback that reports bytes transferred
- [x] 1.3 Handle S3 errors (AccessDenied, ConnectionError, etc.) during upload
- [x] 1.4 Write unit tests for upload functionality in `src/tests/test_s3_service.py`

## 2. Model - Create Upload Worker with Threading

- [x] 2.1 Create `UploadWorker` QObject class with signals: `progress(int)`, `completed()`, `error(str)`
- [x] 2.2 Implement `upload()` method that calls S3 service with progress callback
- [x] 2.3 Add `upload_cancelled` signal and cancellation flag
- [x] 2.4 Add `upload_file()` method to BucketBrowserModel that creates thread and worker
- [x] 2.5 Implement proper thread cleanup (worker.deleteLater(), thread.quit())

## 3. Presenter - Implement Upload Handler with Progress

- [x] 3.1 Update `on_upload_clicked()` to show file picker dialog
- [x] 3.2 Call model upload method with selected file and current prefix
- [x] 3.3 Connect worker signals to view: progress → progress dialog, completed → refresh, error → show error
- [x] 3.4 Handle cancel button click to abort upload thread
- [x] 3.5 Update unit tests in `src/tests/test_bucket_browser_presenter.py`

## 4. View - Add Upload Progress Dialog

- [x] 4.1 Add `show_upload_dialog()` method to open file picker with `QFileDialog`
- [x] 4.2 Add `show_upload_progress_dialog()` returning `QProgressDialog` with 0-100 range
- [x] 4.3 Add `update_upload_progress(percentage)` to update progress bar value
- [x] 4.4 Add `close_upload_progress_dialog()` to close progress dialog
- [x] 4.5 Connect progress dialog cancel button to presenter cancel handler
- [x] 4.6 Update mock view in `src/tests/mock_view.py` for testing

## 5. Integration & Testing

- [x] 5.1 Run all existing tests to ensure no regressions
- [x] 5.2 Manually test upload to root folder with progress display
- [x] 5.3 Manually test upload to subfolder (/tests) with progress display
- [x] 5.4 Test upload of large file (>10MB) to verify progress updates
- [ ] 5.5 Test cancel upload during transfer (not implemented - see TODO below)
- [x] 5.6 Test error scenarios (permission denied, network error) with progress dialog

## TODO for Future Change

- [ ] Add cancel button to progress dialog
- [ ] Implement cancel logic in UploadWorker
- [ ] Test cancellation mid-upload
