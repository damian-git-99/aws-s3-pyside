## 1. Add AWS Dependencies

- [x] 1.1 Add `boto3>=1.34.0` to `requirements.txt`
- [x] 1.2 Run `uv pip install -r requirements.txt` to verify installation
- [x] 1.3 Verify boto3 imports successfully with `python -c "import boto3; print(boto3.__version__)"`

## 2. Create Environment Configuration

- [x] 2.1 Create `.env.example` file with AWS S3 variables:
  - AWS_ACCESS_KEY_ID=your-access-key-id
  - AWS_SECRET_ACCESS_KEY=your-secret-access-key
  - AWS_DEFAULT_REGION=us-east-1
  - AWS_S3_BUCKET_NAME=your-bucket-name
- [x] 2.2 Verify `.env` is in `.gitignore` (add if missing)

## 3. Documentation

- [x] 3.1 Update README.md with AWS setup section explaining:
  - Copy `.env.example` to `.env`
  - Where to obtain AWS credentials
  - Security warning about never committing credentials
