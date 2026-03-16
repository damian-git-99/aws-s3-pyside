## Context

The bucket browser is a PySide6 application following the MVP (Model-View-Presenter) architecture. It allows users to browse, upload, and delete files from S3 buckets. The current implementation includes:

- **View**: `BucketBrowserView` - displays files in a table, toolbar with action buttons
- **Presenter**: `BucketBrowserPresenter` - coordinates between view and model
- **Model**: `BucketBrowserModel` - manages data and business logic, emits Qt signals
- **Service**: `S3FileService` - handles S3 operations

The delete functionality already implements a similar pattern:
1. User selects a file in the table
2. Clicks Delete button in toolbar
3. Confirmation dialog appears
4. File is deleted from S3
5. File list refreshes

The download feature will follow this same interaction pattern but add:
- Save file dialog for choosing download location
- Progress indication during download
- Local file system operations

## Goals / Non-Goals

**Goals:**
- Allow users to download a single file at a time from S3 to their local machine
- Provide clear progress indication during download
- Maintain consistency with existing UI patterns (similar to delete flow)
- Handle errors gracefully with user-friendly messages
- Support cancellation during the save dialog phase

**Non-Goals:**
- Multiple file/batch downloads
- Resume interrupted downloads
- Download queue management
- Download history or recently downloaded files
- Auto-download on double-click (explicit button only)

## Decisions

### 1. Use QFileDialog for save location
**Decision**: Use `QFileDialog.getSaveFileName()` for selecting download location.

**Rationale**: 
- Native OS file picker provides familiar UX
- Pre-fills filename from S3 object name
- Validates write permissions before download starts

**Alternative considered**: Custom save dialog with recent locations. Rejected as overkill for MVP.

### 2. Progress dialog similar to upload
**Decision**: Reuse the upload progress dialog pattern with `QProgressDialog`.

**Rationale**:
- Consistent UI across upload/download operations
- Users already familiar with the pattern
- Non-modal allows user to continue browsing

**Alternative considered**: Status bar progress only. Rejected as less visible for large files.

### 3. Download in background thread
**Decision**: Use `QThread` worker (similar to `UploadWorker`) for downloads.

**Rationale**:
- Prevents UI freezing during download
- Allows progress updates
- Consistent with upload implementation

**Alternative considered**: Download in main thread with async/await. Rejected to maintain consistency with existing patterns.

### 4. Error handling via existing pattern
**Decision**: Use existing error handling patterns from upload/delete operations.

**Rationale**:
- Consistent error messages and recovery
- Leverages existing `show_error()` and `show_error_with_retry()` methods

### 5. S3 download via boto3
**Decision**: Use boto3's `download_fileobj()` with a callback for progress.

**Rationale**:
- boto3 handles retry logic, multipart downloads automatically
- Callback mechanism allows progress updates
- Similar to how upload is implemented

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Large files causing memory issues | Use streaming download with `download_fileobj()` instead of loading entire file into memory |
| Network interruptions during download | boto3 handles retries; user can retry via error dialog |
| Permission denied on local disk | QFileDialog validates location before download starts |
| File name conflicts | QFileDialog allows user to choose different name/location |
| S3 rate limiting | boto3 handles retry with exponential backoff |

### Trade-offs:
- **Single file only**: Limits complexity but requires multiple clicks for batch operations
- **No resume capability**: Simpler implementation but re-downloads on failure
- **Overwrite without warning**: QFileDialog warns about existing files at OS level

## Migration Plan

No migration required - this is an additive feature. Existing functionality unchanged.

Deployment checklist:
1. Verify S3 permissions include `s3:GetObject`
2. Test with various file sizes (small, large, very large)
3. Test error scenarios (no network, no permissions, disk full)
4. Verify progress dialog behavior with slow connections

## Open Questions

None - design is complete.
