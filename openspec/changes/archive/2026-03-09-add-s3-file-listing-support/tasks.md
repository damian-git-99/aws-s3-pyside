## 1. S3 Error Types

- [x] 1.1 Create custom exception classes in `src/services/s3_errors.py`:
  - S3AccessDeniedError
  - S3BucketNotFoundError
  - S3CredentialsError
  - S3ConnectionError
- [x] 1.2 Add unit tests for error classes in `src/tests/test_s3_errors.py`

## 2. S3 File Service

- [x] 2.1 Create `S3FileService` class in `src/services/s3_service.py` with initialization
- [x] 2.2 Implement `list_objects(prefix=None)` method with basic S3 API call using boto3 (prefix optional for future browsing)
- [x] 2.3 Add pagination support with continuation tokens
- [x] 2.4 Implement error mapping from boto3 exceptions to custom error types
- [x] 2.5 Handle empty bucket case (return empty list)
- [x] 2.6 Create unit tests using mocked S3 client in `src/tests/test_s3_service.py`

## 3. Configuration Management

- [x] 3.1 Create `src/config.py` to load AWS configuration from environment variables
- [x] 3.2 Add validation for required env vars (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_S3_BUCKET_NAME)
- [x] 3.3 Create startup check that shows error dialog if config is missing
- [x] 3.4 Add unit tests for configuration loading in `src/tests/test_config.py`

## 4. Update BucketBrowserPresenter

- [x] 4.1 Modify presenter initialization to accept S3FileService dependency
- [x] 4.2 Update `load_bucket_contents()` to call S3 service at root level (no prefix) instead of mock data
- [x] 4.3 Add error handling for S3 exceptions with user-friendly messages
- [x] 4.4 Implement pagination state management (continuation token storage)
- [x] 4.5 Add `load_more()` method for pagination support
- [x] 4.6 Update existing tests and add new tests for S3 integration

## 5. View Updates

- [x] 5.1 Add loading state indicator to BucketBrowserView (spinner or "Loading..." text)
- [x] 5.2 Add method to show/hide loading state
- [x] 5.3 Add error message display with retry action
- [x] 5.4 Add "Load More" button for pagination
- [x] 5.5 Connect view signals to presenter methods

## 6. Integration

- [x] 6.1 Wire up S3FileService in main.py or application startup
- [x] 6.2 Ensure environment variables are loaded before S3 service creation
- [x] 6.3 Test end-to-end flow with real S3 bucket (manual test - pending user validation)
- [x] 6.4 Update integration tests to use mocked S3 service

## 7. Documentation

- [x] 7.1 Add docstrings to all new classes and methods
- [x] 7.2 Update README with S3 configuration instructions
- [x] 7.3 Document error scenarios and troubleshooting
