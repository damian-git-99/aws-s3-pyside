# file-drag-drop-upload Specification

## Purpose
Allow users to upload files to S3 buckets using drag-and-drop operations directly onto the file browser view, complementing the existing file picker upload method.

## Requirements

### Requirement: User can drag and drop a file to upload
The system SHALL accept a single file dropped onto the file browser area and upload it to the current folder with progress tracking, identical to file picker uploads.

#### Scenario: Successful drag-drop upload to root folder
- **WHEN** the user drags a file over the bucket browser view
- **AND** the user drops a single file
- **THEN** a progress dialog SHALL appear showing upload percentage
- **AND** the progress SHALL update from 0% to 100%
- **AND** the file SHALL be uploaded to the root of the bucket
- **AND** the file list SHALL refresh to show the new file
- **AND** the progress dialog SHALL close automatically

#### Scenario: Successful drag-drop upload to subfolder
- **WHEN** the user is viewing the `/documents` folder
- **AND** the user drags a file over the bucket browser view
- **AND** the user drops a file
- **THEN** the file SHALL be uploaded to the `/documents` folder
- **AND** the progress SHALL be displayed from 0% to 100%
- **AND** the file list SHALL refresh to show the new file

#### Scenario: Visual feedback during drag over drop zone
- **WHEN** the user drags a file over the bucket browser area
- **THEN** the view SHALL highlight to indicate it is a valid drop target
- **AND** the mouse cursor SHALL change to indicate a drop action is available
- **AND** the highlight SHALL persist while the file remains over the view

#### Scenario: Drop zone highlight removed on drag exit
- **WHEN** the user drags a file over the bucket browser view
- **AND** the user moves the file outside the view boundaries
- **THEN** the highlight SHALL be removed
- **AND** the cursor SHALL return to normal

### Requirement: Invalid drops are rejected
The system SHALL validate dropped content and reject invalid operations with appropriate feedback.

#### Scenario: Multiple files rejected
- **WHEN** the user drags multiple files over the bucket browser view
- **AND** the user drops them
- **THEN** the drop SHALL be rejected
- **AND** an error message SHALL indicate "Only single file uploads are supported"
- **AND** no upload SHALL occur

#### Scenario: Folder drop rejected
- **WHEN** the user drags a folder over the bucket browser view
- **AND** the user drops the folder
- **THEN** the drop SHALL be rejected
- **AND** an error message SHALL indicate "Folders cannot be uploaded"
- **AND** no upload SHALL occur

#### Scenario: Non-file content rejected
- **WHEN** the user drags non-file content (e.g., text, URLs) over the bucket browser view
- **AND** the user drops the content
- **THEN** the drop SHALL be rejected
- **AND** the view SHALL show no error message
- **AND** no upload SHALL occur

### Requirement: Drag-drop uploads provide progress feedback
The system SHALL provide identical progress tracking for drag-drop uploads as file picker uploads.

#### Scenario: Progress updates during drag-drop transfer
- **WHEN** the user uploads a large file via drag-drop
- **THEN** the progress bar SHALL update periodically
- **AND** the percentage text SHALL show current progress (e.g., "45%")
- **AND** the UI SHALL remain responsive during upload

#### Scenario: Drag-drop upload fails with error handling
- **WHEN** the user performs a drag-drop upload
- **AND** a network error occurs
- **THEN** the progress dialog SHALL close
- **AND** an error message SHALL be displayed
- **AND** the user SHALL be given the option to retry

### Requirement: File browser accepts drops
The file browser view SHALL accept drag-and-drop operations in addition to existing file picker interactions.

#### Scenario: File browser accepts drag events
- **WHEN** a user drags a file over the bucket browser widget
- **THEN** the system SHALL process the drag event
- **AND** the view SHALL indicate drop zone validity via visual feedback
- **AND** dropEvent SHALL be triggered when the file is released

#### Scenario: File browser rejects invalid drops
- **WHEN** a user attempts to drop invalid content (multiple files, folders)
- **THEN** the drag event handler SHALL reject the drop
- **AND** the view SHALL remain unchanged
- **AND** no upload operation SHALL be initiated