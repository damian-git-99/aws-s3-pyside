## 1. S3 Service - Add Download Support

- [x] 1.1 Add `download_fileobj()` method to `S3FileService` class
- [x] 1.2 Implement progress callback mechanism for downloads
- [x] 1.3 Add error handling for download failures (access denied, not found, connection)
- [x] 1.4 Write unit tests for `download_fileobj()` method

## 2. Model - Add Download Signals

- [x] 2.1 Add `file_downloaded` signal to `BucketBrowserModel` signals class
- [x] 2.2 Add `download_error` signal for download failures
- [x] 2.3 Write unit tests for model signals

## 3. View - Add Download UI Components

- [x] 3.1 Add Download button to toolbar (next to Delete button)
- [x] 3.2 Add `show_save_file_dialog()` method for choosing download location
- [x] 3.3 Add `show_download_progress_dialog()` method (similar to upload)
- [x] 3.4 Add `close_download_progress_dialog()` method
- [x] 3.5 Add `_on_download_clicked()` handler method

## 4. Presenter - Implement Download Coordination

- [x] 4.1 Create `DownloadWorker` class (similar to `UploadWorker`)
- [x] 4.2 Add `handle_download_file()` method to coordinate download flow
- [x] 4.3 Add `_on_download_finished()` callback method
- [x] 4.4 Add `_on_download_error()` callback method
- [x] 4.5 Connect view's download button to presenter
- [x] 4.6 Write unit tests for download presenter methods

## 5. Integration and Testing

- [x] 5.1 Verify download button appears correctly in toolbar
- [x] 5.2 Test file selection validation (no selection, folder selected)
- [x] 5.3 Test save dialog opens with correct filename
- [x] 5.4 Test successful download with progress indication
- [x] 5.5 Test error scenarios (access denied, file not found, connection error)
- [x] 5.6 Test cancel during save dialog
- [x] 5.7 Run full test suite to ensure no regressions

## 6. Documentation

- [x] 6.1 Update AGENTS.md if needed with new functionality
- [x] 6.2 Verify all new methods have docstrings
