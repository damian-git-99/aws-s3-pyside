## Context

The application is an S3 File Manager that uses MVP architecture with AWS S3 as the storage backend. The S3FileService handles all S3 operations (list, upload). Files are displayed in a list view with basic operations. The file deletion feature requires:
- Adding delete operation to S3FileService
- Integrating deletion into Model/Presenter/View layers
- Proper error handling for S3-specific issues (AccessDenied, BucketNotFound, etc.)

## Goals / Non-Goals

**Goals:**
- Add delete button to each file row in the list
- Implement a confirmation dialog to prevent accidental deletion
- Use S3 delete_object API for permanent deletion
- Handle S3-specific errors gracefully
- Maintain MVP architecture patterns

**Non-Goals:**
- Soft delete / trash/recycle bin functionality
- Batch deletion of multiple files
- Undo capability
- File recovery after deletion (S3 versioning not enabled)

## Decisions

### Decision 1: Confirmation Dialog in View
**Choice**: Use QMessageBox for confirmation dialog
**Rationale**: QMessageBox is a standard PySide6 component that handles user confirmation with minimal code. It's familiar to users and follows platform conventions.
**Alternatives**: 
- Custom dialog widget: More flexible but adds complexity and testing burden
- No confirmation: Risks accidental data loss

### Decision 2: S3 Delete Integration
**Choice**: Add `delete_object(key)` method to S3FileService
**Rationale**: S3FileService already abstracts all S3 operations. Delete fits naturally alongside list and upload. Centralizes error handling (AccessDenied, ConnectionError, etc.).
**Alternatives**:
- Put delete logic in Model: Violates separation - Model shouldn't directly use boto3
- Presenter calls S3 directly: Breaks abstraction layer

### Decision 3: Delete Signal Flow
**Choice**: Model emits `file_deleted(filename)` signal on successful S3 deletion
**Rationale**: Maintains MVP pattern where Model is responsible for business logic and signals completion. Presenter listens to update View with refreshed list.
**Alternatives**:
- Return boolean from delete method: Less testable and doesn't support async operations

## Risks / Trade-offs

[Risk: Permanent Data Loss] → S3 deletion is irreversible (no versioning enabled). Confirmation dialog mitigates but cannot prevent. Accept as inherent to permanent deletion.

[Risk: S3 Access Errors] → Access denied, bucket not found, network issues. Mitigation: S3FileService already has custom exception handling (S3AccessDeniedError, S3ConnectionError). Reuse for delete operation.

[Risk: Concurrent Deletion] → Object deleted by another process between list and delete. Mitigation: Catch NoSuchKey error and show user-friendly message.
