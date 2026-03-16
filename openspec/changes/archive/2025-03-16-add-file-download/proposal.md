## Why

The bucket browser currently allows users to view, upload, and delete files, but lacks the ability to download files back to their local machine. Users need a way to retrieve files from S3 to work with them locally, which is a fundamental operation for any file management interface.

## What Changes

- Add a **Download** button to the toolbar (next to the Delete button)
- Implement file download functionality that:
  - Allows selecting a single file from the table
  - Opens a save file dialog for choosing download location
  - Downloads the file from S3 to the selected location
  - Shows progress during download
  - Handles errors gracefully (network issues, permissions, etc.)
- **BREAKING**: New method `download_file()` in S3 service
- **BREAKING**: New signal `file_downloaded` in bucket browser model
- **BREAKING**: New view methods for download dialog and progress
- **BREAKING**: New presenter method to coordinate download flow

## Capabilities

### New Capabilities
- `file-download`: Single file download from S3 with save dialog and progress indication

### Modified Capabilities
- *(none)*

## Impact

- **View**: New download button in toolbar, save file dialog, download progress dialog
- **Presenter**: Download coordination logic, error handling
- **Model**: New signal for download completion
- **S3 Service**: New `download_file()` method for S3 retrieval
- **Tests**: Unit tests for download flow in presenter and model
