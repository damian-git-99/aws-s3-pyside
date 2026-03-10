## Why

The application currently allows users to view and manage files but lacks the ability to delete them. Adding delete functionality with a confirmation dialog improves user control over data and follows standard UI/UX patterns for destructive actions.

## What Changes

- Add a "Delete" button to each file row in the file list view
- Display a confirmation dialog when delete is clicked to prevent accidental deletion
- Implement backend file deletion logic in the Model
- Update the Presenter to handle delete events and confirmation

## Capabilities

### New Capabilities
- `file-deletion`: Users can delete files with confirmation dialog to prevent accidental data loss

### Modified Capabilities
<!-- No existing spec-level requirements are changing -->

## Impact

- **View**: New delete button in file list UI, confirmation dialog widget
- **Presenter**: New delete event handler and confirmation logic
- **Model**: New delete file method and signal for deletion completion
- **File System**: Files will be permanently removed when user confirms deletion
