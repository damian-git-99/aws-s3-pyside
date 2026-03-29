## Why

Currently, the application only supports file uploads through a traditional file picker dialog. Adding drag-and-drop support provides a more intuitive user experience and aligns with modern desktop application standards. Users can now drag files directly onto the target folder area in the UI, making file uploads faster and more discoverable. This improves usability and reduces friction in the file upload workflow.

## What Changes

- File picker view now accepts drag-and-drop file operations
- Visual feedback displayed when dragging files over drop zone (e.g., highlight effect)
- Single file drops are processed immediately and uploaded to the current folder
- Invalid drops (multiple files, folders, non-files) are rejected with user feedback
- Drop zone boundaries are clearly defined in the UI
- Logging added to track drag-and-drop upload events for debugging

## Capabilities

### New Capabilities
- `file-drag-drop-upload`: Enable users to drag and drop files onto the file picker view for immediate upload to the current folder. Includes drop zone visual feedback and validation.

### Modified Capabilities
- `file-picker-view`: Enhanced to accept drop events and provide visual feedback during drag-and-drop operations.

## Impact

- **Code**: New DragDropHandler presenter logic, updated FilePickerView widget
- **APIs**: No breaking changes; new presenter methods added for drag-and-drop handling
- **UI**: New visual feedback during drag operations (highlight effect, cursor changes)
- **Dependencies**: Uses existing PySide6 drag-and-drop APIs (QDrag, QMimeData, QDropEvent)
