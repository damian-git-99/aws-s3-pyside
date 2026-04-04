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
    S3DeleteError,
    S3ObjectNotFoundError,
    S3CreateFolderError,
    S3DownloadError,
    S3PresignedUrlError,
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
        self._s3 = s3_client or boto3.client("s3")

    def list_objects(
        self, prefix: Optional[str] = None, continuation_token: Optional[str] = None
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
                    "Bucket": self.bucket_name,
                    "MaxKeys": 50,
                }

                if prefix:
                    params["Prefix"] = prefix
                    params["Delimiter"] = "/"
                else:
                    params["Delimiter"] = "/"

                if current_token:
                    params["ContinuationToken"] = current_token

                response = self._s3.list_objects_v2(**params)

                # Collect common prefixes (folders) from all pages
                for prefix_data in response.get("CommonPrefixes", []):
                    common_prefixes.append(prefix_data["Prefix"])

                # Process actual objects (files)
                for obj in response.get("Contents", []):
                    key = obj["Key"]
                    # Skip the prefix itself if it's a "folder object"
                    if key.endswith("/"):
                        continue

                    # Extract just the filename (after last /)
                    display_name = key.split("/")[-1] if "/" in key else key

                    objects.append(
                        BucketObject(
                            name=display_name,
                            size=obj["Size"],
                            last_modified=obj["LastModified"],
                            storage_class=obj.get("StorageClass", "STANDARD"),
                            is_folder=False,
                        )
                    )

                current_token = response.get("NextContinuationToken")

            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "Unknown")
                if error_code == "403" or error_code == "AccessDenied":
                    raise S3AccessDeniedError(self.bucket_name) from e
                elif error_code == "404" or error_code == "NoSuchBucket":
                    raise S3BucketNotFoundError(self.bucket_name) from e
                else:
                    raise S3ConnectionError() from e

            except NoCredentialsError as e:
                raise S3CredentialsError() from e

            except EndpointConnectionError as e:
                raise S3ConnectionError() from e

        # Process collected common prefixes (folders)
        for prefix_name in common_prefixes:
            display_name = prefix_name.rstrip("/")
            if prefix and display_name.startswith(prefix):
                relative_name = display_name[len(prefix) :]
                if relative_name:
                    display_name = relative_name
            objects.append(
                BucketObject(
                    name=display_name,
                    size=0,
                    last_modified=datetime.now(),
                    storage_class="FOLDER",
                    is_folder=True,
                )
            )

        # Sort: folders first, then files alphabetically
        objects.sort(key=lambda x: (not x.is_folder, x.name.lower()))

        next_token = response.get("NextContinuationToken") if response else None
        is_truncated = response.get("IsTruncated", False) if response else False

        return S3ListResult(
            objects=objects, continuation_token=next_token, is_truncated=is_truncated
        )

    def upload_fileobj_to_prefix(
        self, file_obj, prefix: Optional[str] = None, key: Optional[str] = None
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
            key = getattr(file_obj, "name", "uploaded_file")
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
                    multipart_chunksize=8 * 1024 * 1024,
                ),
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            if error_code == "403" or error_code == "AccessDenied":
                raise S3AccessDeniedError(self.bucket_name) from e
            elif error_code == "NoSuchBucket":
                raise S3BucketNotFoundError(self.bucket_name) from e
            else:
                raise S3UploadError(
                    key, e.response.get("Error", {}).get("Message", str(e))
                ) from e

        except NoCredentialsError as e:
            raise S3CredentialsError() from e

        except EndpointConnectionError as e:
            raise S3ConnectionError() from e

        except Exception as e:
            raise S3UploadError(key, str(e)) from e

    def delete_object(self, key: str) -> None:
        """Delete an object from S3 bucket.

        Args:
            key: The S3 key (path) of the object to delete

        Raises:
            S3AccessDeniedError: If credentials lack bucket delete permission
            S3BucketNotFoundError: If bucket doesn't exist
            S3ObjectNotFoundError: If object doesn't exist in bucket
            S3CredentialsError: If AWS credentials are missing/invalid
            S3ConnectionError: If cannot connect to AWS
            S3DeleteError: If deletion fails for other reasons
        """
        try:
            self._s3.delete_object(Bucket=self.bucket_name, Key=key)

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            if error_code == "403" or error_code == "AccessDenied":
                raise S3AccessDeniedError(self.bucket_name) from e
            elif error_code == "404" or error_code == "NoSuchBucket":
                raise S3BucketNotFoundError(self.bucket_name) from e
            elif error_code == "NoSuchKey":
                raise S3ObjectNotFoundError(key) from e
            else:
                raise S3DeleteError(
                    key, e.response.get("Error", {}).get("Message", str(e))
                ) from e

        except NoCredentialsError as e:
            raise S3CredentialsError() from e

        except EndpointConnectionError as e:
            raise S3ConnectionError() from e

        except Exception as e:
            raise S3DeleteError(key, str(e)) from e

    def create_folder(self, prefix: Optional[str], folder_name: str) -> str:
        """Create a folder (prefix) in S3 bucket.

        In S3, folders are represented as empty objects with keys ending in /.
        This method creates such an object to represent a folder.

        Args:
            prefix: Optional prefix (folder path) where folder should be created
            folder_name: Name of the folder to create

        Returns:
            The full S3 key of the created folder (e.g., "folder_name/" or "prefix/folder_name/")

        Raises:
            S3AccessDeniedError: If credentials lack bucket write permission
            S3BucketNotFoundError: If bucket doesn't exist
            S3CredentialsError: If AWS credentials are missing/invalid
            S3ConnectionError: If cannot connect to AWS
            S3CreateFolderError: If folder creation fails for other reasons
        """
        # Construct full key: prefix + folder_name + "/"
        if prefix:
            # Ensure prefix ends with /
            prefix_normalized = prefix if prefix.endswith("/") else prefix + "/"
            key = f"{prefix_normalized}{folder_name}/"
        else:
            key = f"{folder_name}/"

        try:
            # Create empty object with trailing / to represent folder
            self._s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=b"",  # Empty body
            )
            return key

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            if error_code == "403" or error_code == "AccessDenied":
                raise S3AccessDeniedError(self.bucket_name) from e
            elif error_code == "404" or error_code == "NoSuchBucket":
                raise S3BucketNotFoundError(self.bucket_name) from e
            else:
                raise S3CreateFolderError(
                    folder_name, e.response.get("Error", {}).get("Message", str(e))
                ) from e

        except NoCredentialsError as e:
            raise S3CredentialsError() from e

        except EndpointConnectionError as e:
            raise S3ConnectionError() from e

        except Exception as e:
            raise S3CreateFolderError(folder_name, str(e)) from e

    def download_fileobj(
        self, key: str, file_obj, progress_callback: Optional[callable] = None
    ) -> None:
        """Download an object from S3 to a file-like object.

        Downloads the S3 object specified by key to the provided file-like object.
        Optionally calls a progress callback with the number of bytes transferred.

        Args:
            key: The S3 key (path) of the object to download
            file_obj: File-like object to write to (must support write())
            progress_callback: Optional callback function(bytes_transferred) called during download

        Raises:
            S3AccessDeniedError: If credentials lack bucket read permission
            S3BucketNotFoundError: If bucket doesn't exist
            S3ObjectNotFoundError: If object doesn't exist in bucket
            S3CredentialsError: If AWS credentials are missing/invalid
            S3ConnectionError: If cannot connect to AWS
            S3DownloadError: If download fails for other reasons
        """
        try:
            # Create a wrapper callback that tracks total bytes transferred
            total_transferred = [0]

            def callback(bytes_amount):
                total_transferred[0] += bytes_amount
                if progress_callback:
                    progress_callback(total_transferred[0])

            self._s3.download_fileobj(
                self.bucket_name, key, file_obj, Callback=callback
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            if error_code == "403" or error_code == "AccessDenied":
                raise S3AccessDeniedError(self.bucket_name) from e
            elif error_code == "404" or error_code == "NoSuchBucket":
                raise S3BucketNotFoundError(self.bucket_name) from e
            elif error_code == "NoSuchKey":
                raise S3ObjectNotFoundError(key) from e
            else:
                raise S3DownloadError(
                    key, e.response.get("Error", {}).get("Message", str(e))
                ) from e

        except NoCredentialsError as e:
            raise S3CredentialsError() from e

        except EndpointConnectionError as e:
            raise S3ConnectionError() from e

        except Exception as e:
            raise S3DownloadError(key, str(e)) from e

    def generate_presigned_url(self, key: str, expiration_hours: int = 1) -> str:
        """Generate a pre-signed URL for downloading an S3 object.

        Creates a temporary URL that allows access to the object without
        AWS credentials. The URL expires after the specified duration.

        Args:
            key: The S3 key (path) of the object
            expiration_hours: URL validity duration in hours (default: 1, max: 168)

        Returns:
            Pre-signed URL string

        Raises:
            S3AccessDeniedError: If credentials lack bucket read permission
            S3BucketNotFoundError: If bucket doesn't exist
            S3ObjectNotFoundError: If object doesn't exist in bucket
            S3CredentialsError: If AWS credentials are missing/invalid
            S3ConnectionError: If cannot connect to AWS
            S3PresignedUrlError: If URL generation fails for other reasons
        """
        try:
            url = self._s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expiration_hours * 3600,
            )
            return url
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            if error_code in ("403", "AccessDenied"):
                raise S3AccessDeniedError(self.bucket_name) from e
            elif error_code in ("404", "NoSuchBucket"):
                raise S3BucketNotFoundError(self.bucket_name) from e
            elif error_code == "NoSuchKey":
                raise S3ObjectNotFoundError(key) from e
            else:
                raise S3PresignedUrlError(
                    key, e.response.get("Error", {}).get("Message", str(e))
                ) from e
        except NoCredentialsError as e:
            raise S3CredentialsError() from e
        except EndpointConnectionError as e:
            raise S3ConnectionError() from e
        except Exception as e:
            raise S3PresignedUrlError(key, str(e)) from e
