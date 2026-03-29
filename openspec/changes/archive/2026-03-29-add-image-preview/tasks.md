## 1. View Layer - Preview Button and Dialog

- [x] 1.1 Add Preview button to toolbar in `BucketBrowserView._setup_toolbar()`
- [x] 1.2 Add selection change handler to enable/disable Preview button based on image selection
- [x] 1.3 Create `ImagePreviewDialog` class in new file `src/views/image_preview_dialog.py`
- [x] 1.4 Implement `show_image_preview()` method in `BucketBrowserView` to open the dialog
- [x] 1.5 Add `enable_preview_button()` method to `BucketBrowserView` for button state control

## 2. Presenter Layer - Preview Request Handler

- [x] 2.1 Add `handle_preview_request()` method to `BucketBrowserPresenter`
- [x] 2.2 Implement image download to BytesIO using `S3FileService.download_fileobj()`
- [x] 2.3 Add error handling for failed downloads with user-friendly messages
- [x] 2.4 Add loading state while fetching image from S3

## 3. Integration - Wire View to Presenter

- [x] 3.1 Add `_on_preview_clicked()` callback in `BucketBrowserView`
- [x] 3.2 Connect Preview button click to presenter handler
- [x] 3.3 Add `is_image_selected` helper property in view for button state management

## 4. Testing

- [x] 4.1 Write unit tests for `ImagePreviewDialog`
- [x] 4.2 Add tests for `handle_preview_request()` in presenter tests
- [x] 4.3 Test button enable/disable logic for different file types
- [x] 4.4 Test error handling when S3 download fails

## 5. Manual Verification

- [x] 5.1 Test preview button appears in toolbar
- [x] 5.2 Verify button enables only for image files (jpg, png, gif, etc.)
- [x] 5.3 Test preview dialog opens and displays image correctly
- [x] 5.4 Test error handling for corrupted/invalid images
- [x] 5.5 Test with large images (scroll functionality)
- [x] 5.6 Test in nested folders (verify correct S3 key construction)
