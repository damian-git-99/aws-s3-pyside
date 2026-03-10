"""S3 file service for interacting with AWS S3 buckets."""

import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import boto3
import boto3.s3.transfer
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError

from src.models.bucket_object import BucketObject
from src.services.s3_errors import (
    S3AccessDeniedError,
    S3BucketNotFoundError,
    S3ConnectionError,
    S3CredentialsError,
    S3UploadError,
)


@dataclass
class S3ListResult:
    """Result of an S3 list operation.
    
    Attributes:
        objects: List of bucket objects (files and folders)
        continuation_token: Token for next page, or None if no more pages
        is_truncated: Whether there are more results available
    """
    objects: List[BucketObject]
    continuation_token: Optional[str]
    is_truncated: bool


class S3FileService:
    """Service for listing and managing files in S3 buckets.
    
    This service abstracts S3 operations and provides a clean interface
    for the presenter layer. It supports pagination and error handling.
    
    Args:
        bucket_name: Name of the S3 bucket to access
        s3_client: Optional boto3 S3 client (for testing)
    """
    
    def __init__(self, bucket_name: str, s3_client=None):
        self.bucket_name = bucket_name
        self._s3 = s3_client or boto3.client('s3')
    
    def list_objects(
        self,
        prefix: Optional[str] = None,
        continuation_token: Optional[str] = None
    ) -> S3ListResult:
        """List objects in the S3 bucket.
        
        Lists objects at root level when prefix is None, or under the
        specified prefix. Supports pagination via continuation tokens.
        
        Args:
            prefix: Optional prefix/path to list under (e.g., "folder/")
            continuation_token: Token from previous call for pagination
            
        Returns:
            S3ListResult containing objects and pagination info
            
        Raises:
            S3AccessDeniedError: If credentials lack bucket access
            S3BucketNotFoundError: If bucket doesn't exist
            S3CredentialsError: If AWS credentials are missing/invalid
            S3ConnectionError: If cannot connect to AWS
        """
        objects = []
        common_prefixes = []
        
        current_token = continuation_token
        first_call = True
        
        while first_call or current_token:
            first_call = False
            
            try:
                params = {
                    'Bucket': self.bucket_name,
                    'MaxKeys': 50,
                }
            
                if prefix:
                    params['Prefix'] = prefix
                    params['Delimiter'] = '/'
                else:
                    params['Delimiter'] = '/'
                
                if current_token:
                    params['ContinuationToken'] = current_token
                
                response = self._s3.list_objects_v2(**params)
                
                # Collect common prefixes (folders) from all pages
                for prefix_data in response.get('CommonPrefixes', []):
                    common_prefixes.append(prefix_data['Prefix'])
                
                # Process actual objects (files)
                for obj in response.get('Contents', []):
                    key = obj['Key']
                    # Skip the prefix itself if it's a "folder object"
                    if key.endswith('/'):
                        continue
                        
                    # Extract just the filename (after last /)
                    display_name = key.split('/')[-1] if '/' in key else key
                    
                    objects.append(BucketObject(
                        name=display_name,
                        size=obj['Size'],
                        last_modified=obj['LastModified'],
                        storage_class=obj.get('StorageClass', 'STANDARD'),
                        is_folder=False
                    ))
                
                current_token = response.get('NextContinuationToken')
                
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                if error_code == '403' or error_code == 'AccessDenied':
                    raise S3AccessDeniedError(self.bucket_name) from e
                elif error_code == '404' or error_code == 'NoSuchBucket':
                    raise S3BucketNotFoundError(self.bucket_name) from e
                else:
                    raise S3ConnectionError() from e
                    
            except NoCredentialsError as e:
                raise S3CredentialsError() from e
                
            except EndpointConnectionError as e:
                raise S3ConnectionError() from e
        
        # Process collected common prefixes (folders)
        for prefix_name in common_prefixes:
            display_name = prefix_name.rstrip('/')
            if prefix and display_name.startswith(prefix):
                relative_name = display_name[len(prefix):]
                if relative_name:
                    display_name = relative_name
            objects.append(BucketObject(
                name=display_name,
                size=0,
                last_modified=datetime.now(),
                storage_class='FOLDER',
                is_folder=True
            ))
        
        # Sort: folders first, then files alphabetically
        objects.sort(key=lambda x: (not x.is_folder, x.name.lower()))
        
        next_token = response.get('NextContinuationToken') if response else None
        is_truncated = response.get('IsTruncated', False) if response else False
        
        return S3ListResult(
            objects=objects,
            continuation_token=next_token,
            is_truncated=is_truncated
        )

    def upload_fileobj_to_prefix(
        self,
        file_obj,
        prefix: Optional[str] = None,
        key: Optional[str] = None
    ) -> None:
        """Upload a file-like object to S3 under the specified prefix.

        NOTE: This method uses upload_fileobj instead of upload_file to enable
        accurate progress tracking. While both methods have identical performance
        (both use boto3's s3transfer engine with multipart support), upload_file's
        Callback parameter behaves inconsistently — for small files boto3 performs
        a single-part upload and the callback may be batched or skipped entirely.
        upload_fileobj avoids this by wrapping the file in a custom ProgressFileReader
        that emits Qt signals on each read() call, ensuring reliable progress updates
        regardless of file size.

        Args:
            file_obj: File-like object to upload (must support read())
            prefix: Optional prefix (folder path) in bucket - if None, uploads to root
            key: Optional S3 key (filename) - if None, extracted from file_obj.name

        Raises:
            S3AccessDeniedError: If credentials lack bucket write permission
            S3ConnectionError: If cannot connect to AWS
            S3CredentialsError: If AWS credentials are missing/invalid
            S3UploadError: If upload fails for other reasons
        """
        if key is None:
            # Try to get name from file object
            key = getattr(file_obj, 'name', 'uploaded_file')
            key = os.path.basename(key)
        
        if prefix:
            key = f"{prefix}{key}"

        try:
            self._s3.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                Config=boto3.s3.transfer.TransferConfig(
                    multipart_threshold=8 * 1024 * 1024,
                    multipart_chunksize=8 * 1024 * 1024
                )
            )

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == '403' or error_code == 'AccessDenied':
                raise S3AccessDeniedError(self.bucket_name) from e
            elif error_code == 'NoSuchBucket':
                raise S3BucketNotFoundError(self.bucket_name) from e
            else:
                raise S3UploadError(key, e.response.get('Error', {}).get('Message', str(e))) from e

        except NoCredentialsError as e:
            raise S3CredentialsError() from e

        except EndpointConnectionError as e:
            raise S3ConnectionError() from e

        except Exception as e:
            raise S3UploadError(key, str(e)) from e
