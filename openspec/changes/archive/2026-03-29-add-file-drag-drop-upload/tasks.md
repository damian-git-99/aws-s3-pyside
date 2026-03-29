## 1. Update BucketBrowserView for Drag-Drop Support

- [x] 1.1 Enable drop acceptance on BucketBrowserView widget via `setAcceptDrops(True)`
- [x] 1.2 Implement `dragEnterEvent` handler to validate MIME data and provide visual feedback
- [x] 1.3 Implement `dragMoveEvent` handler to maintain visual feedback during drag
- [x] 1.4 Implement `dragLeaveEvent` handler to remove visual feedback when drag exits
- [x] 1.5 Implement `dropEvent` handler to extract file paths and delegate to presenter

## 2. Add Visual Feedback Styling

- [x] 2.1 Create stylesheet for drop zone highlight effect in BucketBrowserView
- [x] 2.2 Add highlight CSS class to widget when valid drag detected
- [x] 2.3 Add cursor change via Qt cursor API during drag operations
- [x] 2.4 Verify highlight and cursor changes work on Windows, macOS, and Linux

## 3. Implement Drop Validation in BucketBrowserPresenter

- [x] 3.1 Add `on_drag_enter` method to validate MIME data contains files only
- [x] 3.2 Add validation to reject multiple files (accept only single file)
- [x] 3.3 Add validation to reject folder paths (check for directory types)
- [x] 3.4 Add `on_drag_leave` method to clear visual feedback state
- [x] 3.5 Add `on_files_dropped` method to extract and process dropped file path

## 4. Connect Drop Events to Upload Logic

- [x] 4.1 In `on_files_dropped`, extract file path from MIME data using QUrl parsing
- [x] 4.2 Validate extracted path is a valid file (not empty, exists on filesystem)
- [x] 4.3 Reuse existing UploadWorker to perform upload with progress tracking
- [x] 4.4 Connect UploadWorker signals (progress, finished, error) to existing UI handlers
- [x] 4.5 Verify upload destination is current folder (use existing prefix logic)

## 5. Error Handling and User Feedback

- [x] 5.1 Add error handling for invalid drop scenarios (multiple files, folders, non-files)
- [x] 5.2 Display user-friendly error messages via QMessageBox for each invalid case
- [x] 5.3 Add logging for drag-drop operations (drag enter/leave, drop events, validation failures)
- [x] 5.4 Ensure error messages don't interfere with existing error handling

## 6. Testing

- [x] 6.1 Create unit tests for drop validation methods in presenter
- [x] 6.2 Create unit tests for MIME data parsing and file path extraction
- [x] 6.3 Create manual test cases for single file upload via drag-drop
- [x] 6.4 Create manual test cases for invalid drops (multiple files, folders)
- [x] 6.5 Test upload progress dialog appears and updates during drag-drop upload
- [x] 6.6 Test error handling for network failures during drag-drop upload
- [x] 6.7 Test drag-drop works in both root and subfolder contexts

## 7. Integration and Documentation

- [x] 7.1 Verify no breaking changes to existing file picker upload functionality
- [x] 7.2 Add inline code comments documenting drag-drop event handlers
- [x] 7.3 Update CHANGELOG.md with new drag-drop upload feature (skipped - no CHANGELOG.md exists)
- [x] 7.4 Run full test suite to ensure no regressions
