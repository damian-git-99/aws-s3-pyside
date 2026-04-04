# Roadmap: AWS S3 Bucket Browser — Pre-signed URL Feature

**Created:** 2025-01-20  
**Requirements:** 15 v1 requirements mapped  
**Granularity:** Standard (5-8 phases)

---

## Overview

| # | Phase | Goal | Requirements | Status |
|---|-------|------|--------------|--------|
| 1 | Generate Links | Add button to generate pre-signed URLs with configurable expiration | URL-01 to URL-06 | Ready to execute |

**Total: 1 phase | 6 requirements**

---

## Phase 1: Generate Links

**Goal:** Add "Generate Link" button to toolbar for creating pre-signed URLs

**Requirements:**
- URL-01: Button to open link generation dialog
- URL-02: Configurable expiration (1h, 1d, 7d, 30d)
- URL-03: Generate pre-signed URL via boto3
- URL-04: Display URL in dialog
- URL-05: Copy to clipboard button
- URL-06: Error handling

**Success Criteria:**
1. "Generate Link" button visible in toolbar
2. Button enabled only when file (not folder) selected
3. Dialog opens with filename and expiration dropdown
4. URL generates with selected expiration
5. URL can be copied to clipboard
6. Error messages show for failures

**Must-haves:**
- [ ] S3FileService.generate_presigned_url() method
- [ ] GenerateLinkDialog with all UI elements
- [ ] Toolbar button with proper enable/disable logic
- [ ] Presenter to wire everything together
- [ ] Copy to clipboard functionality
- [ ] Error handling

---

## Traceability Matrix

| Requirement | Phase | Status |
|-------------|-------|--------|
| URL-01 | 1 | Pending |
| URL-02 | 1 | Pending |
| URL-03 | 1 | Pending |
| URL-04 | 1 | Pending |
| URL-05 | 1 | Pending |
| URL-06 | 1 | Pending |

**Coverage: 6/6 requirements mapped ✓**

---

## Definition of Done

- [ ] All 6 requirements working
- [ ] User can generate link in 3 clicks: select file → click button → generate
- [ ] URL works when pasted in browser
- [ ] Copy functionality works
- [ ] Errors handled gracefully

---

*Roadmap simplified: 2025-01-20*
