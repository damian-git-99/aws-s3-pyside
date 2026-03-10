## Why

Users need to organize objects in S3 buckets with folder structure. By creating "folders" (S3 prefixes), they can logically group related objects. Currently the browser is read-only - users cannot create folder structure from the UI.

## What Changes

- Add "Create Folder" button to the bucket browser UI
- User clicks button → enters folder name → folder prefix is created in S3 at current location
- New folder appears immediately in the tree view
- Folders can be created at root or within existing prefixes (nested folders)

## Capabilities

### New Capabilities
- `create-s3-folder`: Users can create S3 folder prefixes via UI button with name input dialog, created in current prefix location

### Modified Capabilities
<!-- None -->

## Impact

- **View**: Add "Create Folder" button and folder name input dialog
- **Presenter**: Handle folder creation requests and tree refresh
- **Model**: Add method to track folder creation state
- **S3 Service**: Add method to create empty prefix object (key ending with /) in S3
