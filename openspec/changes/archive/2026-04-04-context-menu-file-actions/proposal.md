## Why

The toolbar currently contains 5 action buttons (Delete, Download, Preview, Generate Link) plus navigation and folder action buttons. This crowded layout reduces vertical space for the file list and creates visual clutter. Moving file-specific actions (Delete, Download, Preview, Generate Link) to a context menu will free toolbar space and maintain all functionality while providing a cleaner interface.

## What Changes

- **Remove** Delete, Download, Preview, and Generate Link buttons from the toolbar
- **Add** context menu to table that appears on right-click with these actions
- **Add** visual hint when a file is selected to indicate context menu availability (status bar message)
- **Preserve** existing behavior: Preview only for images, Delete requires confirmation, single-file only (no multi-select)

## Capabilities

### New Capabilities
- `context-menu-file-actions`: Right-click context menu providing file actions (Preview, Download, Generate Link, Delete) for single file selection

### Modified Capabilities
- `bucket-browser-main-window`: Remove toolbar buttons for file actions, update toolbar requirements to only include navigation and folder operations

## Impact

- **Modified**: `src/views/bucket_browser_view.py` - Remove 5 buttons from toolbar, add context menu
- **Modified**: `src/presenters/bucket_browser_presenter.py` - May need context menu action handlers
- **No change** to S3 service layer or data model
