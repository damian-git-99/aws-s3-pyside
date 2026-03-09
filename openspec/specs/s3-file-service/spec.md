# s3-file-service Specification

## Purpose
Service layer for interacting with AWS S3 buckets. Provides file listing, pagination, error handling, and configuration management for S3 operations.

## Requirements

### Requirement: S3 File Service provides bucket root listing
The system SHALL provide a service layer that lists files from the root of an S3 bucket using real AWS S3 API calls.

#### Scenario: Service lists bucket root contents
- **WHEN** the S3 file service is initialized with bucket name and credentials
- **AND** `list_objects()` is called without prefix
- **THEN** the service SHALL make an S3 API call using boto3 for root level
- **AND** return a list of S3Object items with name, size, last_modified, and storage_class
- **AND** only objects at root level SHALL be returned (not nested under prefixes)

#### Scenario: Service accepts optional prefix parameter
- **WHEN** `list_objects(prefix="folder/")` is called
- **THEN** the service SHALL accept the prefix parameter
- **AND** use it in the S3 API call
- **AND** return objects under that prefix (preparation for future browsing)
- **AND** for current iteration presenter always calls without prefix

#### Scenario: Service handles pagination
- **WHEN** listing a bucket with more than 50 objects
- **THEN** the service SHALL return the first 50 objects
- **AND** provide a continuation token for the next page
- **AND** subsequent calls with the token SHALL return the next page

#### Scenario: Service handles empty bucket
- **WHEN** listing an empty bucket
- **THEN** the service SHALL return an empty list
- **AND** not raise an error

### Requirement: S3 errors are mapped to application errors
The system SHALL translate S3-specific exceptions into application-specific error types.

#### Scenario: Access denied error
- **WHEN** the AWS credentials lack permission to list the bucket
- **THEN** an S3AccessDeniedError SHALL be raised
- **AND** the error message SHALL include the bucket name

#### Scenario: Bucket not found
- **WHEN** the specified bucket does not exist
- **THEN** an S3BucketNotFoundError SHALL be raised
- **AND** the error message SHALL include the attempted bucket name

#### Scenario: Invalid credentials
- **WHEN** AWS credentials are missing or invalid
- **THEN** an S3CredentialsError SHALL be raised
- **AND** the error SHALL indicate that credentials need to be configured

#### Scenario: Network connectivity issues
- **WHEN** the application cannot reach AWS endpoints
- **THEN** an S3ConnectionError SHALL be raised
- **AND** the error SHALL suggest checking network configuration

### Requirement: Presenter integrates with S3 service
The system SHALL update the BucketBrowserPresenter to use S3FileService instead of mock data.

#### Scenario: Presenter loads real bucket data on initialization
- **WHEN** the BucketBrowserPresenter is created
- **THEN** it SHALL initialize S3FileService with configured credentials
- **AND** load the first page of bucket contents
- **AND** display them in the view

#### Scenario: Presenter handles S3 errors gracefully
- **WHEN** an S3 error occurs during listing
- **THEN** the presenter SHALL catch the specific error
- **AND** display an appropriate error message in the view
- **AND** not crash the application

#### Scenario: Presenter supports pagination
- **WHEN** the user clicks "Load More"
- **THEN** the presenter SHALL request the next page using the continuation token
- **AND** append results to the existing list
- **AND** update the view

### Requirement: Configuration loads from environment
The system SHALL load AWS configuration from environment variables.

#### Scenario: All required variables are present
- **WHEN** the application starts
- **AND** AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, and AWS_S3_BUCKET_NAME are set
- **THEN** the configuration SHALL be loaded successfully
- **AND** S3 operations SHALL work

#### Scenario: Missing required variables
- **WHEN** any required AWS environment variable is missing
- **THEN** the application SHALL show an error dialog on startup
- **AND** explain which variables are missing
- **AND** provide instructions on how to set them
