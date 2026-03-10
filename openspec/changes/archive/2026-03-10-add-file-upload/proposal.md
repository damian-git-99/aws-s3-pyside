## Why

The application currently allows browsing the file system but lacks the ability to upload files. Users need the capability to add files to the current directory they're viewing, whether it's the root folder or any subfolder like `/tests`.

## What Changes

- Add file upload button to the toolbar in the main view
- Implement file picker dialog to select a single file from the local system
- Upload the selected file to the currently viewed folder location
- Show upload progress and success/error feedback to the user
- Refresh the file list after successful upload

## Capabilities

### New Capabilities
- `file-upload`: Single file upload with current folder as destination

### Modified Capabilities
<!-- No existing capabilities are being modified at the requirements level -->

## Impact

- **Model**: Add method to handle file upload to specific path
- **View**: Add upload button and file picker dialog integration
- **Presenter**: Connect upload button click to model upload action
- **UI**: New button in toolbar, progress feedback
