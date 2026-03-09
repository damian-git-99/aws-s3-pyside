"""Tests for S3 error classes."""

import unittest
from src.services.s3_errors import (
    S3Error,
    S3AccessDeniedError,
    S3BucketNotFoundError,
    S3CredentialsError,
    S3ConnectionError,
)


class TestS3Errors(unittest.TestCase):
    """Test cases for S3 error classes."""

    def test_s3_error_is_base_class(self):
        """S3Error should be the base class for all S3 errors."""
        error = S3Error("base error")
        self.assertEqual(str(error), "base error")
        self.assertIsInstance(error, Exception)

    def test_s3_access_denied_error(self):
        """S3AccessDeniedError should include bucket name in message."""
        error = S3AccessDeniedError("my-bucket")
        self.assertEqual(error.bucket_name, "my-bucket")
        self.assertIn("my-bucket", str(error))
        self.assertIn("Access denied", str(error))
        self.assertIsInstance(error, S3Error)

    def test_s3_bucket_not_found_error(self):
        """S3BucketNotFoundError should include bucket name in message."""
        error = S3BucketNotFoundError("nonexistent-bucket")
        self.assertEqual(error.bucket_name, "nonexistent-bucket")
        self.assertIn("nonexistent-bucket", str(error))
        self.assertIn("not found", str(error))
        self.assertIsInstance(error, S3Error)

    def test_s3_credentials_error(self):
        """S3CredentialsError should indicate credentials issue."""
        error = S3CredentialsError()
        self.assertIn("credentials", str(error).lower())
        self.assertIn("AWS_ACCESS_KEY_ID", str(error))
        self.assertIsInstance(error, S3Error)

    def test_s3_connection_error(self):
        """S3ConnectionError should indicate connection issue."""
        error = S3ConnectionError()
        self.assertIn("connect", str(error).lower())
        self.assertIn("network", str(error).lower())
        self.assertIsInstance(error, S3Error)

    def test_error_inheritance(self):
        """All S3 errors should inherit from S3Error."""
        self.assertTrue(issubclass(S3AccessDeniedError, S3Error))
        self.assertTrue(issubclass(S3BucketNotFoundError, S3Error))
        self.assertTrue(issubclass(S3CredentialsError, S3Error))
        self.assertTrue(issubclass(S3ConnectionError, S3Error))


if __name__ == "__main__":
    unittest.main()
