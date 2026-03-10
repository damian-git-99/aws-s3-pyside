"""Tests for BucketBrowserModel."""

import unittest
from unittest.mock import MagicMock

from src.models.bucket_browser_model import BucketBrowserModel
from src.services.s3_service import S3FileService
from src.services.s3_errors import (
    S3AccessDeniedError,
    S3BucketNotFoundError,
    S3ConnectionError,
    S3ObjectNotFoundError,
)


class TestBucketBrowserModel(unittest.TestCase):
    """Test cases for BucketBrowserModel."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = BucketBrowserModel()
        self.mock_s3_service = MagicMock(spec=S3FileService)
        self.model.set_s3_service(self.mock_s3_service)

    def test_initialization(self):
        """Model should initialize with mock data."""
        data = self.model.get_data()
        self.assertGreater(len(data), 0)
        # Should have both folders and files
        has_folders = any(obj.is_folder for obj in data)
        has_files = any(not obj.is_folder for obj in data)
        self.assertTrue(has_folders)
        self.assertTrue(has_files)

    def test_delete_file_success(self):
        """Model should successfully delete a file."""
        file_deleted_signal_received = []
        self.model.signals.file_deleted.connect(
            lambda filename: file_deleted_signal_received.append(filename)
        )

        self.model.delete_file('test-file.txt')

        # Verify S3 service was called
        self.mock_s3_service.delete_object.assert_called_once_with('test-file.txt')
        
        # Verify signal was emitted
        self.assertEqual(len(file_deleted_signal_received), 1)
        self.assertEqual(file_deleted_signal_received[0], 'test-file.txt')

    def test_delete_file_with_prefix(self):
        """Model should delete file with prefix (nested path)."""
        file_deleted_signal_received = []
        self.model.signals.file_deleted.connect(
            lambda filename: file_deleted_signal_received.append(filename)
        )

        self.model.delete_file('folder/subfolder/file.txt')

        # Verify S3 service was called with full key
        self.mock_s3_service.delete_object.assert_called_once_with('folder/subfolder/file.txt')
        
        # Verify only filename (not path) is emitted in signal
        self.assertEqual(file_deleted_signal_received[0], 'file.txt')

    def test_delete_file_access_denied(self):
        """Model should emit error signal on access denied."""
        error_signal_received = []
        self.model.signals.error_occurred.connect(
            lambda msg: error_signal_received.append(msg)
        )
        
        self.mock_s3_service.delete_object.side_effect = S3AccessDeniedError('test-bucket')

        self.model.delete_file('file.txt')

        # Verify error signal was emitted
        self.assertEqual(len(error_signal_received), 1)
        self.assertIn('Access denied', error_signal_received[0])

    def test_delete_file_bucket_not_found(self):
        """Model should emit error signal when bucket not found."""
        error_signal_received = []
        self.model.signals.error_occurred.connect(
            lambda msg: error_signal_received.append(msg)
        )
        
        self.mock_s3_service.delete_object.side_effect = S3BucketNotFoundError('test-bucket')

        self.model.delete_file('file.txt')

        self.assertEqual(len(error_signal_received), 1)
        self.assertIn('Bucket', error_signal_received[0])

    def test_delete_file_not_found(self):
        """Model should emit error signal when file not found."""
        error_signal_received = []
        self.model.signals.error_occurred.connect(
            lambda msg: error_signal_received.append(msg)
        )
        
        self.mock_s3_service.delete_object.side_effect = S3ObjectNotFoundError('missing.txt')

        self.model.delete_file('missing.txt')

        self.assertEqual(len(error_signal_received), 1)
        self.assertIn('missing.txt', error_signal_received[0])

    def test_delete_file_connection_error(self):
        """Model should emit error signal on connection failure."""
        error_signal_received = []
        self.model.signals.error_occurred.connect(
            lambda msg: error_signal_received.append(msg)
        )
        
        self.mock_s3_service.delete_object.side_effect = S3ConnectionError()

        self.model.delete_file('file.txt')

        self.assertEqual(len(error_signal_received), 1)
        self.assertIn('Cannot connect', error_signal_received[0])

    def test_delete_file_without_s3_service(self):
        """Model should raise error when S3 service not configured."""
        model_no_service = BucketBrowserModel()

        with self.assertRaises(RuntimeError) as context:
            model_no_service.delete_file('file.txt')

        self.assertIn('S3 service not configured', str(context.exception))


if __name__ == '__main__':
    unittest.main()
