"""Configuration management for the application.

Loads configuration from environment variables and provides validation.
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class AWSConfig:
    """AWS configuration settings.
    
    Attributes:
        access_key_id: AWS access key ID
        secret_access_key: AWS secret access key
        region: AWS region (e.g., 'us-east-1')
        bucket_name: S3 bucket name to browse
    """
    access_key_id: str
    secret_access_key: str
    region: str
    bucket_name: str


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, missing_vars: list[str]):
        self.missing_vars = missing_vars
        var_list = ', '.join(missing_vars)
        super().__init__(
            f"Missing required environment variables: {var_list}\n\n"
            "Please set these variables in your environment or .env file:\n"
            "1. Copy .env.example to .env\n"
            "2. Fill in your actual AWS credentials in .env\n"
            "3. Ensure .env is not committed to version control"
        )


def load_config() -> AWSConfig:
    """Load AWS configuration from environment variables.
    
    Loads variables from .env file if present, then validates
    that all required variables are set.
    
    Returns:
        AWSConfig object with all settings
        
    Raises:
        ConfigurationError: If any required variables are missing
    """
    # Load from .env file if it exists
    load_dotenv()
    
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_DEFAULT_REGION',
        'AWS_S3_BUCKET_NAME'
    ]
    
    # Check for missing variables
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ConfigurationError(missing)
    
    return AWSConfig(
        access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region=os.getenv('AWS_DEFAULT_REGION'),
        bucket_name=os.getenv('AWS_S3_BUCKET_NAME')
    )


def get_bucket_name() -> Optional[str]:
    """Get just the bucket name from environment.
    
    Returns None if not set (for use in contexts where
    we don't want to fail immediately).
    """
    load_dotenv()
    return os.getenv('AWS_S3_BUCKET_NAME')


def validate_config() -> tuple[bool, Optional[list[str]]]:
    """Validate configuration without raising.
    
    Returns:
        Tuple of (is_valid, missing_vars)
        If valid, missing_vars is None
    """
    load_dotenv()
    
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_DEFAULT_REGION',
        'AWS_S3_BUCKET_NAME'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        return False, missing
    
    return True, None
