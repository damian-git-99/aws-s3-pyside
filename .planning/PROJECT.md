# AWS S3 Bucket Browser

## What This Is

A desktop application for browsing and managing AWS S3 buckets with a clean PySide6 interface. Users can navigate folders, upload/download files, preview images, and manage S3 objects without using the AWS CLI or web console.

## Core Value

Users can easily browse, upload, download, and share S3 files through an intuitive desktop interface.

## Requirements

### Validated

- ✓ User can browse S3 bucket contents with folder navigation — existing
- ✓ User can upload files to S3 via drag-and-drop or file picker — existing
- ✓ User can download files from S3 to local machine — existing
- ✓ User can delete files from S3 — existing
- ✓ User can preview images directly in the app — existing
- ✓ User can configure AWS credentials via setup wizard — existing
- ✓ User can search/filter files in the current folder — existing
- ✓ User can navigate with breadcrumbs — existing

### Active

- [ ] User can generate pre-signed URLs for S3 objects with configurable expiration
- [ ] User can copy pre-signed URLs to clipboard with one click
- [ ] User can select expiration time for pre-signed URLs (1h, 1d, 7d, custom)

### Out of Scope

- Multi-bucket support — Single bucket per session is sufficient
- File editing in-place — Download, edit locally, upload is the workflow
- Batch operations on multiple files — v1 focuses on single-file operations
- CloudFront integration — Pre-signed URLs use S3 directly
- Permanent public URLs — Security risk, pre-signed only

## Context

Existing MVP architecture with Model-View-Presenter pattern. S3 operations abstracted through S3FileService. Qt signals used for async communication. Configuration persisted in SQLite. Built with PySide6, boto3 for AWS operations.

## Constraints

- **Tech Stack**: Python 3.12+, PySide6, boto3 — existing codebase
- **Architecture**: Must follow existing MVP pattern — established pattern
- **Security**: Pre-signed URLs only, no permanent public access — security best practice
- **UX**: One-click copy, minimal friction — user experience priority

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use boto3 generate_presigned_url | Native AWS SDK support | — Pending |
| Add context menu for quick actions | Desktop app convention | — Pending |
| Support 4 expiration presets | Balance flexibility vs simplicity | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2025-01-20 after initialization*