## Why

The application currently uses mock file data. Adding real AWS S3 file listing support at the root level will enable users to view files stored in S3 buckets directly from the application, making it production-ready for cloud storage scenarios.

## What Changes

- Add AWS S3 SDK integration (`boto3` library)
- Implement S3 file listing functionality for root level with pagination support
- Add authentication configuration for AWS credentials
- Create S3 service layer to abstract S3 operations (designed to support prefix browsing in future)
- Update existing UI to display real S3 file data instead of mock data
- Implement error handling for S3-specific scenarios (access denied, bucket not found, etc.)

## Capabilities

### New Capabilities
- `s3-file-listing`: List files from AWS S3 bucket root level with pagination support. Service layer designed to support prefix-based browsing in future iterations
- `aws-authentication`: Configure and manage AWS credentials securely for S3 access

### Modified Capabilities
- None (this is purely additive)

## Impact

- **Dependencies**: Adds `boto3` and `botocore` as new dependencies
- **Configuration**: Requires AWS credentials configuration (access key, secret key, region)
- **Security**: Credentials must be stored securely (environment variables or AWS credential files)
- **Testing**: Requires mocked S3 responses or test S3 bucket for unit tests
- **UI**: Updates existing bucket browser to display real S3 data
