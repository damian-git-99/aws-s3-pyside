## Why

Users need to quickly find files in folders with many objects. Currently, there's no way to filter the displayed files by name, forcing users to scroll through long lists. Adding local search with debounce improves usability without requiring additional API calls.

## What Changes

- Add search input field in toolbar for filtering loaded files by name
- Implement debounce (300ms) to avoid excessive filter operations while typing
- Filter applies to currently loaded objects in memory (not from S3)
- Clearing search or empty input shows all objects in current folder
- Case-insensitive partial matching on object name

## Capabilities

### New Capabilities
- `search-filter`: Local search filter with debounce for finding files by name in the bucket browser

### Modified Capabilities
- None - this is a new capability that doesn't change existing requirements

## Impact

- **Files modified**: `src/views/bucket_browser_view.py`, `src/presenters/bucket_browser_presenter.py`
- **New components**: Search input field in toolbar, debounce timer
- **Dependencies**: No new external dependencies - uses existing PySide6 widgets