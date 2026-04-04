# Requirements: AWS S3 Bucket Browser

**Defined:** 2025-01-20
**Core Value:** Users can easily browse, upload, download, and share S3 files through an intuitive desktop interface

## v1 Requirements

### Pre-signed URL Generation

- [ ] **URL-01**: User can right-click on any file to open context menu with "Generate Link" option
- [ ] **URL-02**: User can select expiration time from presets: 1 hour, 1 day, 7 days, or custom
- [ ] **URL-03**: System generates valid pre-signed URL using boto3 with selected expiration
- [ ] **URL-04**: Generated URL is displayed in a modal dialog with full URL text
- [ ] **URL-05**: User can click "Copy to Clipboard" button to copy URL immediately
- [ ] **URL-06**: URL automatically copies to clipboard when generated (configurable)
- [ ] **URL-07**: Modal shows expiration time and remaining time until expiration
- [ ] **URL-08**: User can regenerate URL with different expiration without closing modal
- [ ] **URL-09**: Error handling for generation failures (permissions, network)
- [ ] **URL-10**: URL history is not stored (security - no persistence)

### UI/UX

- [ ] **UI-01**: Context menu appears on right-click of file row
- [ ] **UI-02**: Keyboard shortcut (Ctrl+Shift+C) opens link dialog for selected file
- [ ] **UI-03**: Visual feedback when URL is copied (toast notification)
- [ ] **UI-04**: Loading state shown while URL is being generated
- [ ] **UI-05**: Dialog is resizable and shows full URL without truncation

## v2 Requirements

### Advanced URL Features

- **URL-V2-01**: Batch URL generation for multiple selected files
- **URL-V2-02**: QR code generation for mobile sharing
- **URL-V2-03**: URL templates/presets (custom default expiration)
- **URL-V2-04**: Recently generated URLs list (session-only)

### Sharing Features

- **URL-V2-05**: Email link directly from app
- **URL-V2-06**: Share to system share sheet (macOS/iOS)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Permanent public URLs | Security risk - pre-signed only for v1 |
| Custom domain/CNAME support | Requires CloudFront or proxy - complexity out of scope |
| URL analytics/tracking | No infrastructure for analytics |
| Password-protected URLs | Not supported by S3 pre-signed URLs natively |
| Short URL generation | Would require external service integration |
| Multi-file link generation | Complex UX, defer to v2 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| URL-01 | Phase 1 | Pending |
| URL-02 | Phase 1 | Pending |
| URL-03 | Phase 1 | Pending |
| URL-04 | Phase 1 | Pending |
| URL-05 | Phase 1 | Pending |
| URL-06 | Phase 2 | Pending |
| URL-07 | Phase 2 | Pending |
| URL-08 | Phase 2 | Pending |
| URL-09 | Phase 2 | Pending |
| URL-10 | Phase 2 | Pending |
| UI-01 | Phase 1 | Pending |
| UI-02 | Phase 2 | Pending |
| UI-03 | Phase 2 | Pending |
| UI-04 | Phase 1 | Pending |
| UI-05 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2025-01-20*
*Last updated: 2025-01-20 after initial definition*
