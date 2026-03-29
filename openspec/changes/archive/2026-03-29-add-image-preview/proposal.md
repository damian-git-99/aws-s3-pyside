## Why

Users need a way to quickly preview images stored in S3 buckets without downloading them first. Currently, to view an image, users must download it to their local filesystem and open it with an external application. A built-in preview feature would streamline the workflow and provide immediate visual feedback when browsing image assets.

## What Changes

- Add a "Preview" button to the toolbar in the bucket browser view
- Button is enabled only when a supported image file is selected (jpg, jpeg, png, gif, bmp, svg, webp)
- Clicking Preview opens a modal dialog displaying the image
- Images are downloaded to memory (BytesIO) and displayed using QPixmap
- Preview dialog includes image filename and basic metadata (size, dimensions if available)
- Dialog is resizable and scrollable for large images
- Loading state shown while image is being fetched from S3

## Capabilities

### New Capabilities
- `image-preview`: Image preview functionality for supported image formats in the bucket browser

### Modified Capabilities
- None (this is a purely additive feature that doesn't change existing requirements)

## Impact

- **UI Layer**: [`BucketBrowserView`](src/views/bucket_browser_view.py:1) - Add Preview button and preview dialog
- **Presenter Layer**: [`BucketBrowserPresenter`](src/presenters/bucket_browser_presenter.py:1) - Handle preview requests, download image data
- **Service Layer**: [`S3FileService`](src/services/s3_service.py:40) - Use existing `download_fileobj()` method
- **Model Layer**: [`BucketObject`](src/models/bucket_object.py:7) - Leverage existing `get_icon_type()` for image detection
- **Dependencies**: No new dependencies (uses existing PySide6 and boto3)
