## Context

This is an S3 bucket browser application using MVP architecture. The S3FileService currently supports listing, uploading, and deleting objects. In S3, "folders" are represented as prefixes (keys ending with `/`). The bucket browser tree shows folders and files.

## Goals / Non-Goals

**Goals:**
- Users can create S3 folder prefixes via UI button + dialog
- New folder created as empty prefix (key ending with /)
- Folder created in current prefix location (nested support)
- Tree updates immediately to show new folder
- Works with boto3/botocore S3 client

**Non-Goals:**
- Folder renaming or moving
- Bulk folder operations
- Local filesystem operations

## Decisions

**Decision 1: S3 Prefix Creation Method**
- **Choice**: Use `put_object()` with empty body to create prefix object (key ending with `/`)
- **Rationale**: S3 doesn't have native folders; empty objects are the standard convention
- **Alternative**: Use `head_object()` to verify (adds complexity, unnecessary for creation)

**Decision 2: Button Location**
- **Choice**: Toolbar button near file tree
- **Rationale**: Visible, quick access, consistent with upload/delete

**Decision 3: Error Handling**
- **Choice**: Catch S3 errors (permission, connection, already exists) and emit signals
- **Rationale**: Follows existing S3FileService pattern

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Permission errors** | S3FileService error handling catches AccessDenied, emit error signal |
| **Duplicate folder names** | S3 allows duplicate prefixes; overwrite is harmless (empty object) |
| **Connection issues** | boto3 connection errors caught and wrapped in S3ConnectionError |
| **Tree not updating** | Presenter listens to folder_created signal, refreshes tree |
