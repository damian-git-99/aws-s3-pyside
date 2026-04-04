# Requirements: AWS S3 Bucket Browser

**Defined:** 2025-01-20
**Core Value:** Users can easily browse, upload, download, and share S3 files through an intuitive desktop interface

## v1 Requirements

### Pre-signed URL Generation

- [ ] **URL-01**: User can click "Generate Link" button in toolbar to open link dialog
- [ ] **URL-02**: User can select expiration time: 1 hour, 1 day, 7 days, or 30 days
- [ ] **URL-03**: System generates valid pre-signed URL using boto3 with selected expiration
- [ ] **URL-04**: Generated URL is displayed in the dialog text field
- [ ] **URL-05**: User can click "Copy to Clipboard" button to copy URL immediately
- [ ] **URL-06**: Error handling for generation failures (permissions, network)

### Existing Features (Validated)

- ✓ User can browse S3 bucket contents with folder navigation — existing
- ✓ User can upload files to S3 via drag-and-drop or file picker — existing
- ✓ User can download files from S3 to local machine — existing
- ✓ User can delete files from S3 — existing
- ✓ User can preview images directly in the app — existing
- ✓ User can configure AWS credentials via setup wizard — existing
- ✓ User can search/filter files in the current folder — existing
- ✓ User can navigate with breadcrumbs — existing

## Out of Scope

| Feature | Reason |
|---------|--------|
| Context menu (right-click) | Button in toolbar is simpler |
| Auto-copy to clipboard | Manual copy button is explicit |
| Keyboard shortcuts | Not requested |
| Batch URL generation | Single file at a time |
| URL history | Security - no persistence |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| URL-01 | 1 | Complete |
| URL-02 | 1 | Complete |
| URL-03 | 1 | Complete |
| URL-04 | 1 | Complete |
| URL-05 | 1 | Complete |
| URL-06 | 1 | Complete |

**Coverage:**
- v1 requirements: 6 total
- Mapped to phases: 6
- Unmapped: 0 ✓

---
*Requirements defined: 2025-01-20*
*Last updated: 2026-04-04 after Phase 1 completion*