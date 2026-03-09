## Why

Currently the bucket browser displays files and folders intermixed when users click column headers to sort. Folders should always appear first in the file listing for better UX and consistency with standard file browsers, regardless of how the user sorts the table.

## What Changes

- Modify the bucket browser table to always sort folders before files
- Ensure folders-first sorting persists even when users click column headers
- Add visual separator or grouping indicator between folders and files sections
- Update sorting logic to be consistent across service and view layers

## Capabilities

### New Capabilities
- `folder-first-sorting`: Guaranteed folders-first sorting in file listings that cannot be overridden by user interactions

### Modified Capabilities
<!-- No existing spec-level requirement changes - implementation refinement only -->

## Impact

- `src/views/bucket_browser_view.py`: Table sorting configuration and display logic
- `src/services/s3_service.py`: Sorting logic verification
- `src/presenters/bucket_browser_presenter.py`: May need to handle sorting state
- No API or dependency changes
