## Why

Users need to share S3 files with others who don't have AWS credentials. Currently, there's no way to generate shareable links. Adding pre-signed URL generation allows users to create temporary download links that can be shared via email, chat, or other channels.

## What Changes

- Add "Generate Link" button in toolbar (next to Preview button)
- Button is enabled only when a file is selected (not folders)
- Dialog opens with expiration options: 1 hour, 1 day, 7 days, 30 days
- Generate URL using boto3 generate_presigned_url API
- Copy to clipboard functionality with confirmation message
- Error handling for permission/network issues

## Capabilities

### New Capabilities
- `pre-signed-url`: Generate temporary download links for S3 objects with configurable expiration

### Modified Capabilities
- None - this is a new capability

## Impact

- **Files modified**: 
  - `src/services/s3_service.py` - add generate_presigned_url method
  - `src/services/s3_errors.py` - add S3PresignedUrlError exception
  - `src/views/bucket_browser_view.py` - add toolbar button
  - `src/presenters/bucket_browser_presenter.py` - add link generation handlers
- **New components**: 
  - `src/views/generate_link_dialog.py` - dialog UI for URL generation
- **Dependencies**: No new external dependencies - uses existing boto3 and PySide6