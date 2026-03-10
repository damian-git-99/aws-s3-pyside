## 1. S3 Service Layer

- [x] 1.1 Add `create_folder(prefix: str, folder_name: str) -> str` method to S3FileService
- [x] 1.2 Construct full S3 key as `prefix + folder_name + "/"`
- [x] 1.3 Use `put_object()` with empty body to create prefix object in S3
- [x] 1.4 Add error handling for S3 permission, connection, and other errors
- [x] 1.5 Return the created folder key on success

## 2. Model Layer

- [x] 2.1 Add `create_s3_folder` signal to BucketBrowserModel
- [x] 2.2 Add `folder_creation_error` signal to BucketBrowserModel
- [x] 2.3 Add method to emit signals for folder creation success/failure

## 3. View Layer

- [x] 3.1 Add "Create Folder" button to BucketBrowserView toolbar
- [x] 3.2 Create `CreateFolderDialog` class with text input field
- [x] 3.3 Implement input validation in dialog (reject empty names)
- [x] 3.4 Add error dialog component to display creation errors
- [x] 3.5 Connect button click to open dialog

## 4. Presenter Layer

- [x] 4.1 Get current prefix from selected tree item
- [x] 4.2 Handle "Create Folder" button click event
- [x] 4.3 Open dialog and get folder name from user
- [x] 4.4 Call S3FileService `create_folder()` with current prefix and name
- [x] 4.5 Listen to Model signals for success/error
- [x] 4.6 On success, refresh tree view to show new folder
- [x] 4.7 On error, display error dialog to user

## 5. Testing

- [x] 5.1 Test folder creation at S3 root level
- [x] 5.2 Test folder creation in S3 prefix
- [x] 5.3 Test nested folder creation (multiple prefix levels)
- [x] 5.4 Test validation - prefix normalization
- [x] 5.5 Test S3 error handling - permission denied
- [x] 5.6 Test S3 error handling - connection error
- [x] 5.7 Test S3 error handling - bucket not found
- [x] 5.8 Test S3 error handling - credentials error
- [x] 5.9 Test S3 error handling - generic error
