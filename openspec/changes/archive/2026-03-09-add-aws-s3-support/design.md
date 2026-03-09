## Context

This change adds foundational AWS S3 infrastructure support to the PySide6 CRUD application. Currently, the application has no cloud storage capabilities. This design establishes the necessary dependencies and configuration patterns before implementing S3 operations.

The project uses `uv` for package management and follows MVP architecture with PySide6.

## Goals / Non-Goals

**Goals:**
- Add `boto3` and related AWS SDK dependencies to the project
- Define required AWS S3 environment variables in `.env.example`
- Establish secure credential handling patterns
- Update project dependencies configuration

**Non-Goals:**
- No actual S3 client code or operations (covered in future changes)
- No bucket creation or management logic
- No file upload/download functionality
- No error handling or retry logic for S3 operations

## Decisions

### Decision: Use boto3 as the AWS SDK
**Rationale**: boto3 is the official AWS SDK for Python, actively maintained, and provides comprehensive S3 API coverage. It handles authentication, request signing, and response parsing automatically.

**Alternatives considered**:
- `aiobotocore` - Async version, but unnecessary since this is a desktop PySide6 app using synchronous patterns
- `minio` - S3-compatible client, but would limit us to S3-compatible APIs only

### Decision: Environment variables for credentials
**Rationale**: Following the 12-factor app methodology and AWS best practices. Environment variables keep credentials out of code and allow different configurations per environment (dev/staging/prod).

**Variables needed**:
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_DEFAULT_REGION` - AWS region (e.g., us-east-1)
- `AWS_S3_BUCKET_NAME` - Target S3 bucket name

### Decision: Use `.env.example` as template
**Rationale**: Provides a clear reference for required variables without committing actual credentials. Developers copy to `.env` and fill in values. The `.env` file is gitignored by convention.

### Decision: Add dependencies to requirements.txt
**Rationale**: The project currently uses `requirements.txt`. We'll add boto3 and its dependencies there, consistent with existing patterns.

## Risks / Trade-offs

**Risk**: Developers may accidentally commit `.env` file with real credentials
→ **Mitigation**: Add `.env` to `.gitignore` if not already present. Document the risk in setup instructions.

**Risk**: AWS credentials exposed in environment may be accessed by other processes
→ **Mitigation**: This is a desktop application, so risk is limited to the user's machine. Future iterations may consider credential caching or AWS SSO integration.

**Risk**: boto3 adds ~50MB of dependencies
→ **Mitigation**: Acceptable for a desktop application. If size becomes an issue, consider `boto3-stubs` for type hints separately.

**Risk**: Hard-coded region in examples may not match user's setup
→ **Mitigation**: Make region configurable via env var with sensible default (us-east-1).
