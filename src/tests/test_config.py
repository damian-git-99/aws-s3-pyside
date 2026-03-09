"""Tests for configuration module."""

import os
import unittest
from unittest.mock import patch, MagicMock

from src.config import (
    AWSConfig,
    ConfigurationError,
    load_config,
    validate_config,
    get_bucket_name,
)


class TestConfig(unittest.TestCase):
    """Test cases for configuration management."""

    def setUp(self):
        """Clear environment before each test."""
        # Store original env vars
        self.original_env = {
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION'),
            'AWS_S3_BUCKET_NAME': os.getenv('AWS_S3_BUCKET_NAME'),
        }
        
        # Clear all AWS env vars
        for key in self.original_env:
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        """Restore original environment after each test."""
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]

    @patch('src.config.load_dotenv')
    def test_load_config_success(self, mock_load_dotenv):
        """Should load config when all variables are set."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
        os.environ['AWS_S3_BUCKET_NAME'] = 'test-bucket'

        config = load_config()

        self.assertIsInstance(config, AWSConfig)
        self.assertEqual(config.access_key_id, 'test-key')
        self.assertEqual(config.secret_access_key, 'test-secret')
        self.assertEqual(config.region, 'us-west-2')
        self.assertEqual(config.bucket_name, 'test-bucket')

    @patch('src.config.load_dotenv')
    def test_load_config_missing_access_key(self, mock_load_dotenv):
        """Should raise ConfigurationError when ACCESS_KEY_ID is missing."""
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        os.environ['AWS_S3_BUCKET_NAME'] = 'test-bucket'
        # AWS_ACCESS_KEY_ID is missing

        with self.assertRaises(ConfigurationError) as context:
            load_config()

        self.assertIn('AWS_ACCESS_KEY_ID', str(context.exception))
        self.assertEqual(context.exception.missing_vars, ['AWS_ACCESS_KEY_ID'])

    @patch('src.config.load_dotenv')
    def test_load_config_multiple_missing(self, mock_load_dotenv):
        """Should list all missing variables in error."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        # Missing: AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_S3_BUCKET_NAME

        with self.assertRaises(ConfigurationError) as context:
            load_config()

        error_msg = str(context.exception)
        self.assertIn('AWS_SECRET_ACCESS_KEY', error_msg)
        self.assertIn('AWS_DEFAULT_REGION', error_msg)
        self.assertIn('AWS_S3_BUCKET_NAME', error_msg)

    @patch('src.config.load_dotenv')
    def test_validate_config_success(self, mock_load_dotenv):
        """Should return valid when all variables present."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        os.environ['AWS_S3_BUCKET_NAME'] = 'test-bucket'

        is_valid, missing = validate_config()

        self.assertTrue(is_valid)
        self.assertIsNone(missing)

    @patch('src.config.load_dotenv')
    def test_validate_config_failure(self, mock_load_dotenv):
        """Should return invalid with missing vars list."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        # Missing other vars

        is_valid, missing = validate_config()

        self.assertFalse(is_valid)
        self.assertIsNotNone(missing)
        self.assertIn('AWS_SECRET_ACCESS_KEY', missing)
        self.assertIn('AWS_DEFAULT_REGION', missing)
        self.assertIn('AWS_S3_BUCKET_NAME', missing)

    @patch('src.config.load_dotenv')
    def test_get_bucket_name_success(self, mock_load_dotenv):
        """Should return bucket name when set."""
        os.environ['AWS_S3_BUCKET_NAME'] = 'my-bucket'

        bucket = get_bucket_name()

        self.assertEqual(bucket, 'my-bucket')

    @patch('src.config.load_dotenv')
    def test_get_bucket_name_missing(self, mock_load_dotenv):
        """Should return None when bucket not set."""
        bucket = get_bucket_name()

        self.assertIsNone(bucket)

    def test_configuration_error_message(self):
        """ConfigurationError should have helpful message."""
        error = ConfigurationError(['VAR1', 'VAR2'])

        self.assertIn('VAR1', str(error))
        self.assertIn('VAR2', str(error))
        self.assertIn('.env.example', str(error))
        self.assertIn('.env', str(error))


if __name__ == '__main__':
    unittest.main()
