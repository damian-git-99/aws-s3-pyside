# Pre-signed URL Generation

## Summary

Generate temporary download links for S3 objects that can be shared with users who don't have AWS credentials.

## User Interface

### Toolbar Button
- **Location**: Toolbar, after Preview button
- **Label**: "Generate Link"
- **Color**: Orange (#f39c12)
- **States**:
  - Disabled: When no file selected or folder selected
  - Enabled: When a file (not folder) is selected

### Generate Link Dialog
- **Title**: "Generate Link - {filename}"
- **Modal**: Yes (blocks main window)
- **Size**: 600x250 pixels

#### Components:
1. **Filename display**: "File: {filename}" (bold)
2. **Expiration dropdown**: 
   - "1 hour" (data: 1)
   - "1 day" (data: 24)
   - "7 days" (data: 168)
   - "30 days" (data: 720)
3. **Generate button**: Blue (#3498db), "Generate Link"
4. **URL display**: Read-only QLineEdit with placeholder
5. **Copy button**: Green (#27ae60), "Copy to Clipboard" (disabled until URL generated)
6. **Close button**: Closes dialog

## Functionality

### URL Generation
- Uses boto3 `generate_presigned_url('get_object', ...)`
- Default expiration: 1 hour
- URL is valid for specified duration without AWS credentials

### Error Handling
- **Access Denied (403)**: Show "Access denied to bucket" error
- **Object Not Found (404)**: Show "File not found" error
- **No Credentials**: Show credentials error message
- **Connection Error**: Show network error with retry option

### Clipboard
- Uses `QGuiApplication.clipboard()` (not QClipboard directly)
- Shows confirmation: "Link copied to clipboard!"

## Files Modified

| File | Change |
|------|--------|
| `src/services/s3_service.py` | + `generate_presigned_url()` method |
| `src/services/s3_errors.py` | + `S3PresignedUrlError` class |
| `src/views/generate_link_dialog.py` | **NEW** - Dialog component |
| `src/views/bucket_browser_view.py` | + Toolbar button, handlers |
| `src/presenters/bucket_browser_presenter.py` | + Link generation logic |

## Security Considerations

- URLs are temporary (expire after selected duration)
- No URL history stored (security requirement)
- URLs require bucket read permission

## Testing Checklist

- [ ] Button disabled when no selection
- [ ] Button disabled when folder selected  
- [ ] Button enabled when file selected
- [ ] Dialog opens with correct title
- [ ] All 4 expiration options work
- [ ] URL generates successfully
- [ ] Copy to clipboard works
- [ ] Generated URL downloads file in browser
- [ ] Error messages display for failures