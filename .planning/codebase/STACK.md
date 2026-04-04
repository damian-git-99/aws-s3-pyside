# Technology Stack

**Analysis Date:** 2026-04-04

## Languages

**Primary:**
- **Python 3.12+** - All application code and business logic

**Secondary:**
- **Bash** - Build scripts and CI/CD workflows

## Runtime

**Environment:**
- **CPython** 3.12+ (specified in `pyproject.toml`)

**Package Manager:**
- **uv** - Modern Python package manager and runner
- Lockfile: `uv.lock` (present)
- Alternative: `requirements.txt` for compatibility

## Frameworks

**Core:**
- **PySide6 >=6.6.0** - Qt-based GUI framework for cross-platform desktop application

**Testing:**
- **unittest** - Standard Python testing library (no external test framework)

**Build/Bundle:**
- **PyInstaller >=6.0.0** - Creates standalone executable from Python scripts
- **UPX** - Compression for executables (enabled in `s3-bucket-browser.spec`)

## Key Dependencies

**Critical:**
- **boto3 >=1.34.0** - AWS SDK for Python - S3 operations
- **botocore >=1.42.0** - Core library for boto3
- **PySide6 >=6.6.0** - GUI framework

**Infrastructure:**
- **python-dotenv >=1.0.0** - Environment variable loading from `.env` files
- **s3transfer** - S3 transfer operations (boto3 dependency)
- **jmespath** - JSON matching for AWS responses
- **python-dateutil** - Date parsing for S3 object metadata
- **urllib3** - HTTP client for AWS API calls

**Build:**
- **altgraph** - Graph utilities for PyInstaller
- **setuptools >=61.0** - Build backend

## Configuration

**Environment:**
- `.env` file for local development (copy from `.env.example`)
- SQLite database for persistent configuration storage:
  - **Linux/macOS**: `~/.config/BucketBrowser/config.db`
  - **Windows**: `%APPDATA%/BucketBrowser/config.db`

**Required Environment Variables:**
- `AWS_ACCESS_KEY_ID` - AWS credential
- `AWS_SECRET_ACCESS_KEY` - AWS credential
- `AWS_DEFAULT_REGION` - AWS region (e.g., `us-east-1`)
- `AWS_S3_BUCKET_NAME` - Target S3 bucket

**Build:**
- `pyproject.toml` - Project metadata and dependencies
- `s3-bucket-browser.spec` - PyInstaller configuration
- `build.py` - Custom build script wrapper

**Code Quality:**
- `ruff` cache directory present (`.ruff_cache/`)
- No explicit linter configuration files detected

## Platform Requirements

**Development:**
- Python 3.12+
- uv package manager (recommended)
- Git

**Production:**
- Target platforms: Windows, Linux (built via CI/CD)
- Single executable distribution (~91MB)
- No Python runtime required on target machine

**CI/CD:**
- GitHub Actions
- Ubuntu 22.04 and Windows runners
- Node.js 20 (for semantic-release)

---

*Stack analysis: 2026-04-04*
