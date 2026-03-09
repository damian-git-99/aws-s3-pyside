"""S3-specific error types for the application."""


class S3Error(Exception):
    """Base class for all S3-related errors."""
    pass


class S3AccessDeniedError(S3Error):
    """Raised when AWS credentials lack permission to access the bucket."""
    
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        super().__init__(f"Access denied to bucket '{bucket_name}'. Check your AWS permissions.")


class S3BucketNotFoundError(S3Error):
    """Raised when the specified S3 bucket does not exist."""
    
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        super().__init__(f"Bucket '{bucket_name}' not found. Check the bucket name.")


class S3CredentialsError(S3Error):
    """Raised when AWS credentials are missing or invalid."""
    
    def __init__(self):
        super().__init__("AWS credentials not configured. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")


class S3ConnectionError(S3Error):
    """Raised when the application cannot connect to AWS endpoints."""
    
    def __init__(self):
        super().__init__("Cannot connect to AWS. Please check your network configuration.")
