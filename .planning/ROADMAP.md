# Roadmap: AWS S3 Bucket Browser — Pre-signed URL Feature

**Created:** 2025-01-20  
**Requirements:** 15 v1 requirements mapped  
**Granularity:** Standard (5-8 phases)

---

## Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Foundation | Add context menu and basic URL generation service | URL-01, URL-03, URL-04, UI-01, UI-04 | 5 |
| 2 | Core UX | Complete URL generation UX with copy and expiration | URL-02, URL-05, URL-07, URL-09, UI-03, UI-05 | 6 |
| 3 | Polish | Advanced features and keyboard shortcuts | URL-06, URL-08, UI-02 | 4 |

**Total: 3 phases | 15 requirements | 15 success criteria**

---

## Phase 1: Foundation

**Goal:** Add right-click context menu and basic URL generation capability

**Requirements:**
- URL-01: Context menu with "Generate Link" option
- URL-03: Generate pre-signed URL via boto3
- URL-04: Display URL in modal dialog
- UI-01: Right-click context menu on file rows
- UI-04: Loading state during generation

**Success Criteria:**
1. User can right-click any file and see "Generate Link" option
2. Clicking "Generate Link" opens a modal dialog
3. Modal shows a valid pre-signed URL for the selected file
4. URL expires in 1 hour by default
5. Loading spinner appears while URL is being generated

**UI hint:** yes

**Must-haves:**
- [ ] Context menu infrastructure in view layer
- [ ] S3FileService.generate_presigned_url() method
- [ ] Basic modal dialog for URL display
- [ ] Error handling for S3 API failures

**Verification:**
- Right-click on file → context menu appears with "Generate Link"
- Click → modal opens with valid URL
- URL works when pasted in browser (downloads file)

---

## Phase 2: Core UX

**Goal:** Complete the URL generation experience with expiration options and copy functionality

**Requirements:**
- URL-02: Expiration time presets (1h, 1d, 7d, custom)
- URL-05: Copy to clipboard button
- URL-07: Show expiration time in modal
- URL-09: Error handling for generation failures
- UI-03: Visual feedback when copied (toast)
- UI-05: Resizable dialog showing full URL

**Success Criteria:**
1. User can select expiration from dropdown (1h/1d/7d/custom)
2. "Copy to Clipboard" button copies URL immediately
3. Toast notification confirms "URL copied to clipboard"
4. Modal shows "Expires: [date/time]" and "Time remaining: [duration]"
5. Dialog can be resized to show very long URLs
6. Network errors show user-friendly error message with retry option

**UI hint:** yes

**Must-haves:**
- [ ] Expiration selection UI (dropdown or buttons)
- [ ] Clipboard integration (QClipboard)
- [ ] Toast notification system
- [ ] Error dialog with retry capability

**Verification:**
- Select 7 days expiration → URL valid for 7 days
- Click Copy → clipboard contains URL
- Disconnect network → error dialog appears with retry

---

## Phase 3: Polish

**Goal:** Add advanced features for power users and accessibility

**Requirements:**
- URL-06: Auto-copy to clipboard on generation (configurable)
- URL-08: Regenerate URL with different expiration
- UI-02: Keyboard shortcut Ctrl+Shift+C

**Success Criteria:**
1. Settings option to auto-copy URLs when generated
2. "Regenerate" button in modal to create new URL with different expiration
3. Ctrl+Shift+C opens link dialog for currently selected file
4. All Phase 1-2 features work with keyboard navigation

**UI hint:** yes

**Must-haves:**
- [ ] Settings panel integration for auto-copy preference
- [ ] Regenerate button in URL modal
- [ ] Keyboard shortcut registration
- [ ] Accessibility labels for screen readers

**Verification:**
- Enable auto-copy in settings → generate URL → automatically copied
- Press Ctrl+Shift+C → link dialog opens
- Click Regenerate → new URL with same file, can pick new expiration

---

## Traceability Matrix

| Requirement | Phase | Status |
|-------------|-------|--------|
| URL-01 | 1 | Pending |
| URL-02 | 2 | Pending |
| URL-03 | 1 | Pending |
| URL-04 | 1 | Pending |
| URL-05 | 2 | Pending |
| URL-06 | 3 | Pending |
| URL-07 | 2 | Pending |
| URL-08 | 3 | Pending |
| URL-09 | 2 | Pending |
| URL-10 | 3 | Pending |
| UI-01 | 1 | Pending |
| UI-02 | 3 | Pending |
| UI-03 | 2 | Pending |
| UI-04 | 1 | Pending |
| UI-05 | 2 | Pending |

**Coverage: 15/15 requirements mapped ✓**

---

## Dependencies

**Phase 1 → Phase 2:**
- Context menu must exist before adding expiration UI
- URL generation service must work before copy feature

**Phase 2 → Phase 3:**
- Copy functionality must exist before auto-copy setting
- Modal must exist before regenerate feature

**No external dependencies:** All phases use existing boto3/PySide6 infrastructure.

---

## Risk Assessment

| Risk | Phase | Mitigation |
|------|-------|------------|
| S3 permissions for presigned URLs | 1 | Test with limited IAM roles, document required permissions |
| Clipboard API differences (Linux/Windows/macOS) | 2 | Test on all platforms, use Qt abstraction |
| Very long URLs breaking UI | 2 | Resizable dialog, text wrap, horizontal scroll |
| Keyboard shortcut conflicts | 3 | Check against OS defaults, make configurable |

---

## Definition of Done (Milestone)

All 3 phases complete when:
- [ ] All 15 v1 requirements verified
- [ ] User can generate pre-signed URL with any expiration preset
- [ ] User can copy URL to clipboard in 2 clicks or less
- [ ] Error handling works for network and permission failures
- [ ] Code follows existing MVP patterns
- [ ] Manual testing on target platforms

---

*Roadmap created: 2025-01-20*
