## ADDED Requirements

### Requirement: User can delete files from S3
The system SHALL provide a delete button for each file that triggers a confirmation dialog before deletion. Upon confirmation, the file SHALL be permanently removed from S3 bucket. The system SHALL handle S3-specific errors gracefully.

#### Scenario: Delete button visible on file row
- **WHEN** user views the file list
- **THEN** each file row displays a delete button

#### Scenario: Confirmation dialog appears on delete click
- **WHEN** user clicks the delete button for a file
- **THEN** a confirmation dialog appears asking "Are you sure you want to delete this file? This action cannot be undone."

#### Scenario: Cancel deletion
- **WHEN** user clicks "Cancel" in the confirmation dialog
- **THEN** the dialog closes and the file remains unchanged in S3

#### Scenario: Confirm deletion
- **WHEN** user clicks "Delete" in the confirmation dialog
- **THEN** the file is permanently removed from the S3 bucket and the file list is refreshed

### Requirement: S3 delete error handling
The system SHALL handle S3 delete failures gracefully and inform the user of any errors.

#### Scenario: Deletion succeeds
- **WHEN** the file is successfully deleted from S3
- **THEN** the file list updates to remove the deleted file entry

#### Scenario: Access denied error
- **WHEN** file deletion fails due to insufficient S3 permissions
- **THEN** an error dialog displays "Access Denied: You don't have permission to delete this file"

#### Scenario: Bucket not found error
- **WHEN** the S3 bucket is deleted or inaccessible
- **THEN** an error dialog displays "Bucket Error: The S3 bucket is not accessible"

#### Scenario: Connection error
- **WHEN** the S3 delete operation fails due to network issues
- **THEN** an error dialog displays "Connection Error: Unable to reach AWS S3. Check your internet connection."

#### Scenario: File already deleted
- **WHEN** attempting to delete a file that no longer exists in S3
- **THEN** an error dialog displays "File Not Found: The file has already been deleted"

