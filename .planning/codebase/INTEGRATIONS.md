# External Integrations

**Analysis Date:** 2026-04-04

## APIs & External Services

**AWS S3:**
- **Purpose:** Primary data storage and file management
- **SDK/Client:** `boto3` (`src/services/s3_service.py`)
- **Auth:** Environment variables (see below)
- **Operations:**
  - List objects with pagination
  - Upload files (multipart supported)
  - Download files with progress tracking
  - Delete objects
  - Create folders (empty objects with `/` suffix)

**AWS SDK Dependencies:**
- `boto3` - Main AWS SDK
- `botocore` - Core HTTP handling and authentication
- `s3transfer` - Optimized S3 transfers

## Data Storage

**Local Configuration:**
- **Type:** SQLite database
- **Purpose:** Persistent storage of AWS credentials and settings
- **Location:** Platform-specific user data directory
- **Access:** `src/config/config_manager.py`

**File Storage:**
- **Service:** AWS S3 bucket (configured via `AWS_S3_BUCKET_NAME`)
- **Local cache:** None (direct streaming to/from S3)

**Caching:**
- None detected - direct S3 API calls with real-time data

## Authentication & Identity

**AWS Credentials:**
- **Type:** IAM User Access Keys
- **Implementation:** Environment variables passed to boto3
- **Storage:** SQLite database (encrypted at rest by OS)
- **Required vars:**
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`

**Security Considerations:**
- Credentials stored locally in SQLite
- No encryption at application level
- Relies on OS-level file permissions
- Setup wizard for first-time configuration (`src/views/setup_wizard_view.py`)

## Monitoring & Observability

**Error Tracking:**
- None - local logging only

**Logs:**
- **Framework:** Python `logging` module
- **Output:** Console (stdout)
- **Level:** INFO for application, WARNING for boto3/botocore/urllib3
- **Config:** `src/main.py` lines 11-22

**Custom Error Types:**
- `S3AccessDeniedError`
- `S3BucketNotFoundError`
- `S3CredentialsError`
- `S3ConnectionError`
- `S3UploadError`
- `S3DownloadError`
- `S3DeleteError`
- `S3ObjectNotFoundError`
- `S3CreateFolderError`

## CI/CD & Deployment

**Hosting:**
- GitHub Releases for executable distribution

**CI Pipeline:**
- **Service:** GitHub Actions (`.github/workflows/release.yml`)
- **Trigger:** Manual (`workflow_dispatch`)
- **Jobs:**
  1. **release:** semantic-release for versioning
  2. **build:** Cross-platform executable builds

**Build Matrix:**
- Ubuntu 22.04 → Linux binary
- Windows Latest → Windows .exe

**Release Tooling:**
- **semantic-release** (^23.0.0) - Automated versioning from commits
- **Conventional Commits** format required

## Environment Configuration

**Required env vars for development:**
```bash
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket-name
```

**Secrets location:**
- Development: `.env` file (gitignored)
- Production: SQLite database in user data directory

## Webhooks & Callbacks

**Incoming:**
- None - desktop application

**Outgoing:**
- None - no external webhooks configured

## Network Requirements

**Outbound:**
- HTTPS to AWS S3 endpoints (region-specific)
- Port 443 required

**No Inbound:**
- No server component

---

*Integration audit: 2026-04-04*
