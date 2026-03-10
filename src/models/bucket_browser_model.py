from datetime import datetime, timedelta
from typing import List, Optional
from random import choice, randint

from src.mvp.base_model import BaseModel
from src.models.bucket_object import BucketObject
from src.services.s3_service import S3FileService
from src.services.s3_errors import S3Error


class BucketBrowserModel(BaseModel):
    """Model for the bucket browser. Manages bucket objects data."""
    
    def __init__(self):
        super().__init__()
        self._data: List[BucketObject] = []
        self._s3_service: Optional[S3FileService] = None
        self._load_mock_data()
    
    def set_s3_service(self, s3_service: S3FileService) -> None:
        """Set the S3 service for deletion operations.
        
        Args:
            s3_service: The S3 file service instance
        """
        self._s3_service = s3_service
    
    def load_data(self) -> None:
        """Load data - for mock version, just refresh the mock data."""
        self._load_mock_data()
        self.notify_data_loaded()
    
    def get_data(self) -> List[BucketObject]:
        """Return current bucket objects."""
        return self._data.copy()
    
    def refresh_data(self) -> None:
        """Refresh data from source (mock: reload with variations)."""
        self._load_mock_data()
        self.notify_data_changed()

    def _load_mock_data(self) -> None:
        """Load mock data for development and testing."""
        base_date = datetime.now()
        
        mock_files = [
            # Documents
            ('documento1.pdf', 2457600, 'STANDARD'),
            ('documento2.docx', 512000, 'STANDARD'),
            ('readme.txt', 2048, 'STANDARD'),
            ('notas.rtf', 15360, 'STANDARD'),
            
            # Images
            ('foto1.jpg', 3145728, 'STANDARD'),
            ('foto2.png', 2097152, 'STANDARD'),
            ('logo.svg', 15360, 'STANDARD'),
            ('banner.webp', 1048576, 'STANDARD'),
            
            # Code
            ('script.py', 5120, 'STANDARD'),
            ('app.js', 25600, 'STANDARD'),
            ('index.html', 8192, 'STANDARD'),
            ('styles.css', 12288, 'STANDARD'),
            ('config.json', 2048, 'STANDARD'),
            
            # Archives
            ('backup.zip', 52428800, 'IA'),
            ('data.tar.gz', 104857600, 'IA'),
            ('old_files.7z', 20971520, 'GLACIER'),
            
            # Generic files
            ('database.db', 104857600, 'STANDARD'),
            ('log.txt', 1048576, 'STANDARD'),
            ('binary_file', 51200, 'STANDARD'),
            
            # Large files
            ('video.mp4', 1073741824, 'STANDARD'),
            ('dataset.csv', 536870912, 'IA'),
        ]
        
        storage_classes = ['STANDARD', 'IA', 'GLACIER', 'DEEP_ARCHIVE']
        
        self._data = []
        
        # Add folders first
        folders = [
            BucketObject(
                name='Documents',
                size=0,
                last_modified=base_date - timedelta(days=30),
                storage_class='-',
                is_folder=True
            ),
            BucketObject(
                name='Images',
                size=0,
                last_modified=base_date - timedelta(days=25),
                storage_class='-',
                is_folder=True
            ),
            BucketObject(
                name='Scripts',
                size=0,
                last_modified=base_date - timedelta(days=20),
                storage_class='-',
                is_folder=True
            ),
            BucketObject(
                name='Backups',
                size=0,
                last_modified=base_date - timedelta(days=60),
                storage_class='-',
                is_folder=True
            ),
            BucketObject(
                name='Archive',
                size=0,
                last_modified=base_date - timedelta(days=90),
                storage_class='-',
                is_folder=True
            ),
        ]
        
        self._data.extend(folders)
        
        # Add files
        for i, (filename, size, storage_class) in enumerate(mock_files):
            # Add some randomness to dates and sizes
            days_ago = randint(1, 365)
            modified_date = base_date - timedelta(days=days_ago)
            
            obj = BucketObject(
                name=filename,
                size=size + randint(-size//10, size//10),  # +/- 10% variation
                last_modified=modified_date,
                storage_class=choice(storage_classes) if randint(0, 10) > 7 else storage_class,
                is_folder=False
            )
            self._data.append(obj)
        
        # Sort: folders first, then by name
        self._data.sort(key=lambda x: (not x.is_folder, x.name.lower()))
    
    def delete_file(self, key: str) -> None:
        """Delete a file from S3 bucket.

        Args:
            key: The S3 key (path) of the file to delete (e.g., "folder/file.txt")

        Raises:
            Various S3Error subclasses on failure
        """
        if not self._s3_service:
            raise RuntimeError("S3 service not configured. Cannot delete file.")

        try:
            # Delete from S3
            self._s3_service.delete_object(key)
            # Emit success signal
            filename = key.split('/')[-1]
            self.notify_file_deleted(filename)
        except S3Error as e:
            # Emit error signal with detailed message
            self.notify_error(str(e))

    def create_folder(self, prefix: Optional[str], folder_name: str) -> None:
        """Create a folder in the S3 bucket.

        Args:
            prefix: Optional prefix (current location) where folder should be created
            folder_name: Name of the folder to create

        Raises:
            RuntimeError: If S3 service not configured
            Various S3Error subclasses on failure
        """
        if not self._s3_service:
            raise RuntimeError("S3 service not configured. Cannot create folder.")

        try:
            # Create folder in S3
            created_key = self._s3_service.create_folder(prefix, folder_name)
            # Emit success signal with folder name
            self.notify_folder_created(folder_name)
        except S3Error as e:
            # Emit error signal with detailed message
            self.notify_folder_creation_error(str(e))
