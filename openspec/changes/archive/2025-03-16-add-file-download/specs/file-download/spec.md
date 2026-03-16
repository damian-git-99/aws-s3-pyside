## ADDED Requirements

### Requirement: User can download files from S3
The system SHALL provide a download button that allows users to save a selected file from S3 to their local machine. The system SHALL prompt for a save location, show download progress, and handle errors gracefully.

#### Scenario: Download button visible in toolbar
- **WHEN** user views the bucket browser
- **THEN** a download button is visible in the toolbar

#### Scenario: Download requires file selection
- **WHEN** user clicks the download button without selecting a file
- **THEN** an error message displays "Please select a file to download"

#### Scenario: Folders cannot be downloaded
- **WHEN** user selects a folder and clicks the download button
- **THEN** an error message displays "Folders cannot be downloaded. Please select a file."

#### Scenario: Save dialog opens on download click
- **WHEN** user selects a file and clicks the download button
- **THEN** a save file dialog opens with the filename pre-filled

#### Scenario: Cancel download
- **WHEN** user clicks "Cancel" in the save dialog
- **THEN** the dialog closes and no download occurs

#### Scenario: Download succeeds
- **WHEN** user selects a location and confirms the save dialog
- **THEN** the file downloads from S3 to the selected location
- **THEN** a progress dialog shows during download
- **THEN** the file is saved to the selected location
- **THEN** a success message displays "File downloaded successfully"

### Requirement: Download progress indication
The system SHALL display download progress to the user during file retrieval from S3.

#### Scenario: Progress dialog during download
- **WHEN** a file download starts
- **THEN** a progress dialog displays with the filename and download percentage

#### Scenario: Progress updates during download
- **WHEN** download progresses
- **THEN** the progress bar updates to reflect the percentage complete

### Requirement: S3 download error handling
The system SHALL handle S3 download failures gracefully and inform the user of any errors.

#### Scenario: Access denied error
- **WHEN** file download fails due to insufficient S3 permissions
- **THEN** an error message displays "Access Denied: You don't have permission to download this file"

#### Scenario: File not found error
- **WHEN** the file no longer exists in S3
- **THEN** an error message displays "File Not Found: The file has been removed from S3"

#### Scenario: Connection error
- **WHEN** the S3 download fails due to network issues
- **THEN** an error message displays "Connection Error: Unable to reach AWS S3. Check your internet connection."

#### Scenario: Disk full error
- **WHEN** the download cannot complete due to insufficient disk space
- **THEN** an error message displays "Insufficient Space: Not enough disk space to save the file"
