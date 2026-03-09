## Context

The project already has:
- AWS S3 infrastructure configured (`boto3`, environment variables)
- Bucket browser UI implemented with mock data
- MVP architecture with Model-View-Presenter pattern

Currently, the bucket browser displays mocked file data. This change connects the UI to real AWS S3 to enable production use.

## Goals / Non-Goals

**Goals:**
- Replace mock file data with real S3 bucket listings
- Maintain MVP architecture (no logic in Views)
- Support pagination for large buckets (1000+ objects)
- Handle S3 errors gracefully (access denied, bucket not found)
- Keep existing UI behavior (icons, sorting, columns)

**Non-Goals:**
- Folder browsing/navigation (root level only for now, but service designed to support prefixes)
- Upload/download functionality (separate change)
- Multiple bucket support (separate change)
- Caching layer (can be added later)
- Folder creation/deletion operations

## Decisions

### 1. S3 Service Layer
**Decision**: Create `S3FileService` class in `src/services/s3_service.py`

**Rationale**: 
- Abstracts S3 operations from presenters
- Allows easy mocking for tests
- Follows Single Responsibility Principle
- Designed with optional prefix parameter for future browsing support

**API Design**:
```python
def list_objects(self, prefix: str | None = None, continuation_token: str | None = None) -> S3ListResult:
    # Returns files at root level when prefix is None
    # Returns files under prefix when prefix is provided
```

**Alternatives considered**:
- Direct boto3 calls in presenter (rejected: too coupled, hard to test)
- Repository pattern (overkill for MVP)

### 2. Configuration Management
**Decision**: Load credentials from environment variables via `src/config.py`

**Rationale**:
- AWS SDK automatically reads standard env vars
- No need for custom config files
- 12-factor app principles

**Alternatives considered**:
- Config file with credentials (security risk)
- AWS credential files (adds complexity)

### 3. Pagination Strategy
**Decision**: Use S3's native `ListObjectsV2` with `ContinuationToken`

**Rationale**:
- Standard S3 pagination mechanism
- Supports up to 1000 keys per request
- Efficient for large buckets

**Implementation**:
- First request without token
- Display first page immediately
- Load more on demand ("Load More" button)
- Store continuation token in presenter state

### 4. Error Handling
**Decision**: S3-specific exceptions mapped to user-friendly messages

**Mapping**:
- `ClientError` (403) → "Access denied to bucket"
- `ClientError` (404) → "Bucket not found"
- `EndpointConnectionError` → "Cannot connect to AWS"
- `NoCredentialsError` → "AWS credentials not configured"

**Rationale**: Users shouldn't see raw boto3 exceptions

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| S3 latency affects UI responsiveness | Show loading spinner, async operations |
| Large buckets (>10k objects) slow to load | Implement pagination, lazy loading |
| Credentials exposed in logs | Never log credentials, use env vars only |
| AWS costs for API calls | Document cost implications, use pagination |
| Testing requires AWS access | Mock S3 client in tests using moto |

## Migration Plan

1. **Phase 1**: Add S3FileService with basic list operation
2. **Phase 2**: Update BucketBrowserPresenter to use S3FileService
3. **Phase 3**: Remove mock data, update tests
4. **Phase 4**: Add pagination UI controls

**Rollback**: Revert to mock data by restoring presenter to use mock service

## Open Questions

- Should we cache S3 responses to reduce API calls?
- Do we need a "refresh" interval or manual only?
- Should empty folders be shown (S3 doesn't have real folders)?
