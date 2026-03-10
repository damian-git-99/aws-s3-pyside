"""Tests for S3FileService."""

import io
import unittest
from datetime import datetime
from unittest.mock import MagicMock

from src.models.bucket_object import BucketObject
from src.services.s3_errors import (
    S3AccessDeniedError,
    S3BucketNotFoundError,
    S3ConnectionError,
    S3CredentialsError,
    S3UploadError,
    S3DeleteError,
    S3ObjectNotFoundError,
)
from src.services.s3_service import S3FileService, S3ListResult


class TestS3FileService(unittest.TestCase):
    """Test cases for S3FileService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_s3_client = MagicMock()
        self.service = S3FileService(
            bucket_name="test-bucket",
            s3_client=self.mock_s3_client
        )

    def test_initialization(self):
        """Service should store bucket name and S3 client."""
        self.assertEqual(self.service.bucket_name, "test-bucket")
        self.assertEqual(self.service._s3, self.mock_s3_client)

    def test_list_objects_root_level(self):
        """Should list objects at root level when no prefix given."""
        # Mock response with files and folders at root
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {
                    'Key': 'file1.txt',
                    'Size': 1024,
                    'LastModified': datetime(2024, 1, 1, 12, 0, 0),
                    'StorageClass': 'STANDARD'
                },
                {
                    'Key': 'file2.pdf',
                    'Size': 2048,
                    'LastModified': datetime(2024, 1, 2, 12, 0, 0),
                    'StorageClass': 'STANDARD'
                }
            ],
            'CommonPrefixes': [
                {'Prefix': 'folder1/'},
                {'Prefix': 'folder2/'}
            ],
            'IsTruncated': False
        }

        result = self.service.list_objects()

        # Verify API was called correctly
        self.mock_s3_client.list_objects_v2.assert_called_once_with(
            Bucket='test-bucket',
            MaxKeys=50,
            Delimiter='/'
        )

        # Verify result structure
        self.assertIsInstance(result, S3ListResult)
        self.assertEqual(len(result.objects), 4)  # 2 folders + 2 files
        self.assertFalse(result.is_truncated)
        self.assertIsNone(result.continuation_token)

        # Verify folders come first and have correct properties
        self.assertTrue(result.objects[0].is_folder)
        self.assertEqual(result.objects[0].name, 'folder1')
        self.assertEqual(result.objects[0].storage_class, 'FOLDER')

        # Verify files have correct properties
        file_objects = [obj for obj in result.objects if not obj.is_folder]
        self.assertEqual(len(file_objects), 2)
        self.assertEqual(file_objects[0].name, 'file1.txt')
        self.assertEqual(file_objects[0].size, 1024)

    def test_list_objects_with_prefix(self):
        """Should list objects under specified prefix."""
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {
                    'Key': 'folder1/nested_file.txt',
                    'Size': 512,
                    'LastModified': datetime(2024, 1, 1, 12, 0, 0),
                    'StorageClass': 'STANDARD'
                }
            ],
            'CommonPrefixes': [],
            'IsTruncated': False
        }

        result = self.service.list_objects(prefix='folder1/')

        # Verify API was called with prefix
        self.mock_s3_client.list_objects_v2.assert_called_once_with(
            Bucket='test-bucket',
            MaxKeys=50,
            Prefix='folder1/',
            Delimiter='/'
        )

        # Verify only the filename (not full path) is returned
        self.assertEqual(len(result.objects), 1)
        self.assertEqual(result.objects[0].name, 'nested_file.txt')

    def test_list_objects_with_pagination(self):
        """Should handle pagination with continuation tokens."""
        # First page
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1.txt', 'Size': 100, 'LastModified': datetime.now(), 'StorageClass': 'STANDARD'}],
            'CommonPrefixes': [],
            'IsTruncated': True,
            'NextContinuationToken': 'token123'
        }

        result = self.service.list_objects()

        self.assertTrue(result.is_truncated)
        self.assertEqual(result.continuation_token, 'token123')

        # Second page with token
        self.mock_s3_client.list_objects_v2.reset_mock()
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file2.txt', 'Size': 200, 'LastModified': datetime.now(), 'StorageClass': 'STANDARD'}],
            'CommonPrefixes': [],
            'IsTruncated': False
        }

        result2 = self.service.list_objects(continuation_token='token123')

        # Verify continuation token was passed
        self.mock_s3_client.list_objects_v2.assert_called_once_with(
            Bucket='test-bucket',
            MaxKeys=50,
            ContinuationToken='token123',
            Delimiter='/'
        )
        self.assertFalse(result2.is_truncated)

    def test_list_objects_empty_bucket(self):
        """Should return empty list for empty bucket."""
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [],
            'CommonPrefixes': [],
            'IsTruncated': False
        }

        result = self.service.list_objects()

        self.assertEqual(len(result.objects), 0)
        self.assertFalse(result.is_truncated)

    def test_list_objects_skips_folder_objects(self):
        """Should skip S3 folder objects (keys ending with /)."""
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {
                    'Key': 'folder1/',  # This is a "folder object" placeholder
                    'Size': 0,
                    'LastModified': datetime.now(),
                    'StorageClass': 'STANDARD'
                },
                {
                    'Key': 'folder1/file.txt',
                    'Size': 100,
                    'LastModified': datetime.now(),
                    'StorageClass': 'STANDARD'
                }
            ],
            'CommonPrefixes': [{'Prefix': 'folder1/subfolder/'}],
            'IsTruncated': False
        }

        result = self.service.list_objects(prefix='folder1/')

        # Should have file and subfolder, but not the folder object placeholder
        self.assertEqual(len(result.objects), 2)
        names = [obj.name for obj in result.objects]
        self.assertIn('file.txt', names)
        self.assertIn('subfolder', names)
        # The placeholder folder1/ should be skipped (it represents current directory)
        self.assertNotIn('folder1', names)

    def test_access_denied_error(self):
        """Should raise S3AccessDeniedError on 403."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': '403', 'Message': 'Access Denied'}
        }
        self.mock_s3_client.list_objects_v2.side_effect = ClientError(
            error_response, 'ListObjectsV2'
        )

        with self.assertRaises(S3AccessDeniedError) as context:
            self.service.list_objects()

        self.assertIn('test-bucket', str(context.exception))

    def test_bucket_not_found_error(self):
        """Should raise S3BucketNotFoundError on 404."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': 'NoSuchBucket', 'Message': 'Bucket not found'}
        }
        self.mock_s3_client.list_objects_v2.side_effect = ClientError(
            error_response, 'ListObjectsV2'
        )

        with self.assertRaises(S3BucketNotFoundError) as context:
            self.service.list_objects()

        self.assertIn('test-bucket', str(context.exception))

    def test_credentials_error(self):
        """Should raise S3CredentialsError when no credentials."""
        from botocore.exceptions import NoCredentialsError

        self.mock_s3_client.list_objects_v2.side_effect = NoCredentialsError()

        with self.assertRaises(S3CredentialsError):
            self.service.list_objects()

    def test_connection_error(self):
        """Should raise S3ConnectionError on connection issues."""
        from botocore.exceptions import EndpointConnectionError

        self.mock_s3_client.list_objects_v2.side_effect = EndpointConnectionError(
            endpoint_url='https://s3.amazonaws.com'
        )

        with self.assertRaises(S3ConnectionError):
            self.service.list_objects()

    def test_upload_fileobj_to_root(self):
        """Should upload file-like object to root of bucket."""
        fake_file = io.BytesIO(b'test content')
        setattr(fake_file, 'name', '/path/to/file.txt')

        self.service.upload_fileobj_to_prefix(fake_file)

        self.mock_s3_client.upload_fileobj.assert_called_once()
        call_args = self.mock_s3_client.upload_fileobj.call_args
        self.assertEqual(call_args[0][0], fake_file)
        self.assertEqual(call_args[0][1], 'test-bucket')
        self.assertEqual(call_args[0][2], 'file.txt')

    def test_upload_fileobj_with_prefix(self):
        """Should upload file-like object to specified prefix."""
        fake_file = io.BytesIO(b'test content')
        
        self.service.upload_fileobj_to_prefix(fake_file, prefix='uploads/', key='test.txt')

        call_args = self.mock_s3_client.upload_fileobj.call_args
        self.assertEqual(call_args[0][2], 'uploads/test.txt')

    def test_upload_fileobj_to_prefix_with_name_attr(self):
        """Should extract filename from file_obj.name attribute."""
        fake_file = io.BytesIO(b'test content')
        setattr(fake_file, 'name', '/path/to/important.doc')

        self.service.upload_fileobj_to_prefix(fake_file, prefix='docs/')

        call_args = self.mock_s3_client.upload_fileobj.call_args
        self.assertEqual(call_args[0][2], 'docs/important.doc')

    def test_upload_fileobj_no_name_attr_uses_default(self):
        """Should use default filename when file_obj has no name attribute."""
        fake_file = io.BytesIO(b'test content')
        # No name attribute set

        self.service.upload_fileobj_to_prefix(fake_file)

        call_args = self.mock_s3_client.upload_fileobj.call_args
        self.assertEqual(call_args[0][2], 'uploaded_file')

    def test_upload_fileobj_access_denied_error(self):
        """Should raise S3AccessDeniedError on 403 during upload."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': '403', 'Message': 'Access Denied'}
        }
        self.mock_s3_client.upload_fileobj.side_effect = ClientError(
            error_response, 'PutObject'
        )

        fake_file = io.BytesIO(b'test content')
        
        with self.assertRaises(S3AccessDeniedError):
            self.service.upload_fileobj_to_prefix(fake_file, key='file.txt')

    def test_upload_fileobj_bucket_not_found_error(self):
        """Should raise S3BucketNotFoundError when bucket doesn't exist."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': 'NoSuchBucket', 'Message': 'Bucket not found'}
        }
        self.mock_s3_client.upload_fileobj.side_effect = ClientError(
            error_response, 'PutObject'
        )

        fake_file = io.BytesIO(b'test content')

        with self.assertRaises(S3BucketNotFoundError):
            self.service.upload_fileobj_to_prefix(fake_file, key='file.txt')

    def test_upload_fileobj_connection_error(self):
        """Should raise S3ConnectionError on connection issues during upload."""
        from botocore.exceptions import EndpointConnectionError

        self.mock_s3_client.upload_fileobj.side_effect = EndpointConnectionError(
            endpoint_url='https://s3.amazonaws.com'
        )

        fake_file = io.BytesIO(b'test content')

        with self.assertRaises(S3ConnectionError):
            self.service.upload_fileobj_to_prefix(fake_file, key='file.txt')

    def test_upload_fileobj_credentials_error(self):
        """Should raise S3CredentialsError when no credentials during upload."""
        from botocore.exceptions import NoCredentialsError

        self.mock_s3_client.upload_fileobj.side_effect = NoCredentialsError()

        fake_file = io.BytesIO(b'test content')

        with self.assertRaises(S3CredentialsError):
            self.service.upload_fileobj_to_prefix(fake_file, key='file.txt')

    def test_delete_object_success(self):
        """Should successfully delete an object from S3."""
        self.service.delete_object('test-file.txt')

        self.mock_s3_client.delete_object.assert_called_once_with(
            Bucket='test-bucket',
            Key='test-file.txt'
        )

    def test_delete_object_with_prefix(self):
        """Should delete object with prefix (nested path)."""
        self.service.delete_object('folder/subfolder/file.txt')

        self.mock_s3_client.delete_object.assert_called_once_with(
            Bucket='test-bucket',
            Key='folder/subfolder/file.txt'
        )

    def test_delete_object_access_denied_error(self):
        """Should raise S3AccessDeniedError on 403 during delete."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': '403', 'Message': 'Access Denied'}
        }
        self.mock_s3_client.delete_object.side_effect = ClientError(
            error_response, 'DeleteObject'
        )

        with self.assertRaises(S3AccessDeniedError) as context:
            self.service.delete_object('file.txt')

        self.assertIn('test-bucket', str(context.exception))

    def test_delete_object_bucket_not_found_error(self):
        """Should raise S3BucketNotFoundError when bucket doesn't exist."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': 'NoSuchBucket', 'Message': 'Bucket not found'}
        }
        self.mock_s3_client.delete_object.side_effect = ClientError(
            error_response, 'DeleteObject'
        )

        with self.assertRaises(S3BucketNotFoundError):
            self.service.delete_object('file.txt')

    def test_delete_object_not_found_error(self):
        """Should raise S3ObjectNotFoundError when object doesn't exist."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': 'NoSuchKey', 'Message': 'Object not found'}
        }
        self.mock_s3_client.delete_object.side_effect = ClientError(
            error_response, 'DeleteObject'
        )

        with self.assertRaises(S3ObjectNotFoundError) as context:
            self.service.delete_object('missing-file.txt')

        self.assertIn('missing-file.txt', str(context.exception))

    def test_delete_object_connection_error(self):
        """Should raise S3ConnectionError on connection issues during delete."""
        from botocore.exceptions import EndpointConnectionError

        self.mock_s3_client.delete_object.side_effect = EndpointConnectionError(
            endpoint_url='https://s3.amazonaws.com'
        )

        with self.assertRaises(S3ConnectionError):
            self.service.delete_object('file.txt')

    def test_delete_object_credentials_error(self):
        """Should raise S3CredentialsError when no credentials during delete."""
        from botocore.exceptions import NoCredentialsError

        self.mock_s3_client.delete_object.side_effect = NoCredentialsError()

        with self.assertRaises(S3CredentialsError):
            self.service.delete_object('file.txt')

    def test_delete_object_generic_error(self):
        """Should raise S3DeleteError for other errors during delete."""
        from botocore.exceptions import ClientError

        error_response = {
            'Error': {'Code': 'InternalError', 'Message': 'Internal server error'}
        }
        self.mock_s3_client.delete_object.side_effect = ClientError(
            error_response, 'DeleteObject'
        )

        with self.assertRaises(S3DeleteError) as context:
            self.service.delete_object('file.txt')

        self.assertIn('file.txt', str(context.exception))


if __name__ == '__main__':
    unittest.main()
