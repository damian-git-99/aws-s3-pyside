# pre-signed-url Specification

## Purpose
Provide ability to generate temporary download links for S3 objects that can be shared with users who don't have AWS credentials.

## Requirements

### Requirement: Generate pre-signed URL for S3 object
The bucket browser SHALL provide functionality to generate pre-signed URLs for downloading S3 objects.

#### Scenario: Generate URL for selected file
- **WHEN** user selects a file (not folder) and clicks "Generate Link" button
- **THEN** a dialog opens with filename and expiration options

#### Scenario: Select URL expiration time
- **WHEN** user selects expiration time from dropdown
- **THEN** the URL will be valid for the selected duration (1 hour, 1 day, 7 days, or 30 days)

#### Scenario: URL generated with selected expiration
- **WHEN** user clicks "Generate Link" button in dialog
- **THEN** a valid pre-signed URL is generated using the selected expiration time

#### Scenario: Copy URL to clipboard
- **WHEN** user clicks "Copy to Clipboard" button
- **THEN** the URL is copied to system clipboard and a confirmation message is shown

### Requirement: Button enabled only for files
The "Generate Link" button SHALL only be enabled when a file is selected, not for folders.

#### Scenario: Button disabled when no selection
- **WHEN** no file or folder is selected
- **THEN** the "Generate Link" button is disabled

#### Scenario: Button disabled when folder selected
- **WHEN** user selects a folder
- **THEN** the "Generate Link" button is disabled

#### Scenario: Button enabled when file selected
- **WHEN** user selects a file
- **THEN** the "Generate Link" button is enabled

### Requirement: Error handling for URL generation
The system SHALL display appropriate error messages when URL generation fails.

#### Scenario: Access denied error
- **WHEN** user doesn't have permission to access the object
- **THEN** error message "Access denied" is displayed

#### Scenario: Object not found error
- **WHEN** the selected object no longer exists in S3
- **THEN** error message "File not found" is displayed

#### Scenario: Network connection error
- **WHEN** cannot connect to AWS
- **THEN** error message with retry option is displayed

### Requirement: Temporary URL with expiration
The generated URL SHALL be temporary and expire after the selected duration.

#### Scenario: URL expires after 1 hour
- **WHEN** user selects "1 hour" expiration and generates URL
- **THEN** the URL is valid for 1 hour from generation time

#### Scenario: URL expires after 1 day
- **WHEN** user selects "1 day" expiration and generates URL
- **THEN** the URL is valid for 24 hours from generation time

#### Scenario: URL expires after 7 days
- **WHEN** user selects "7 days" expiration and generates URL
- **THEN** the URL is valid for 7 days from generation time

#### Scenario: URL expires after 30 days
- **WHEN** user selects "30 days" expiration and generates URL
- **THEN** the URL is valid for 30 days from generation time