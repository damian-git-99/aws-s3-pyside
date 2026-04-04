## 1. Service Implementation

- [x] 1.1 Add S3PresignedUrlError exception to s3_errors.py
- [x] 1.2 Add S3FileService.generate_presigned_url(key, expiration_hours) method
- [x] 1.3 Handle ClientError cases (403, 404, NoSuchKey) with appropriate exceptions
- [x] 1.4 Handle NoCredentialsError and EndpointConnectionError

## 2. Dialog Implementation

- [x] 2.1 Create GenerateLinkDialog class in generate_link_dialog.py
- [x] 2.2 Add expiration dropdown with 4 options (1h, 1d, 7d, 30d)
- [x] 2.3 Add Generate button that creates pre-signed URL
- [x] 2.4 Add URL display field (read-only)
- [x] 2.5 Add Copy to Clipboard button with QGuiApplication.clipboard()
- [x] 2.6 Show confirmation message via QMessageBox

## 3. View Implementation

- [x] 3.1 Add "Generate Link" button to toolbar (after Preview button)
- [x] 3.2 Set button width to 130px to fit text
- [x] 3.3 Add orange styling (#f39c12)
- [x] 3.4 Add enable_generate_link_button() method
- [x] 3.5 Update _on_selection_changed to enable button for files only
- [x] 3.6 Add _on_generate_link_clicked handler

## 4. Presenter Implementation

- [x] 4.1 Add handle_generate_link(filename) method
- [x] 4.2 Construct full S3 key from current_prefix + filename
- [x] 4.3 Add _generate_link(dialog, key) method
- [x] 4.4 Connect Generate button to call _generate_link
- [x] 4.5 Connect Copy button to dialog.copy_to_clipboard
- [x] 4.6 Add loading state during URL generation
- [x] 4.7 Handle errors with show_error message

## 5. Testing

- [x] 5.1 Test button disabled when no selection
- [x] 5.2 Test button disabled when folder selected
- [x] 5.3 Test button enabled when file selected
- [x] 5.4 Test URL generation with different expirations
- [x] 5.5 Test copy to clipboard works
- [x] 5.6 Test error handling for access denied
- [x] 5.7 Test generated URL works in browser