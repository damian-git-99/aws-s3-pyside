## 1. S3FileService Implementation

- [x] 1.1 Add S3-specific delete error classes to s3_errors.py if needed
- [x] 1.2 Implement `delete_object(key)` method in S3FileService
- [x] 1.3 Handle S3 errors: AccessDenied, NoSuchBucket, ConnectionError, NoSuchKey
- [x] 1.4 Write unit tests for delete_object with mocked S3 client

## 2. Model Implementation

- [x] 2.1 Add `file_deleted` signal to BucketBrowserModel
- [x] 2.2 Implement `delete_file(filename)` method using S3FileService
- [x] 2.3 Add error handling for S3 delete failures
- [x] 2.4 Write unit tests for Model delete method

## 3. Presenter Implementation

- [x] 3.1 Add `handle_delete_file(filename)` method to Presenter
- [x] 3.2 Implement confirmation dialog logic using QMessageBox
- [x] 3.3 Connect Model's `file_deleted` signal to refresh file list
- [x] 3.4 Handle error signals from Model and display error dialogs
- [x] 3.5 Write unit tests for delete handling and confirmation (no Qt needed)

## 4. View Implementation

- [x] 4.1 Add delete button to file list row UI
- [x] 4.2 Connect delete button click to Presenter's delete handler
- [x] 4.3 Ensure delete button styling matches other row buttons
- [x] 4.4 Display loading indicator during deletion
- [x] 4.5 Verify file list updates correctly after deletion

## 5. Integration & Testing

- [x] 5.1 End-to-end test: delete button → confirmation → S3 deletion → list refresh
- [x] 5.2 Test error scenarios: AccessDenied, NoSuchBucket, ConnectionError
- [x] 5.3 Test concurrent deletion (file deleted by another client)
- [x] 5.4 Verify UI remains responsive during deletion
- [x] 5.5 Test with different S3 storage classes (STANDARD, IA, GLACIER, etc.)

## 6. Documentation

- [x] 6.1 Update AGENTS.md with S3 deletion capability notes
- [x] 6.2 Add docstrings to S3FileService.delete_object method
- [x] 6.3 Document S3-specific error handling in Model

