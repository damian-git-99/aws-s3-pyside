from datetime import datetime, timedelta
from typing import List
from random import choice, randint

from src.mvp.base_model import BaseModel
from src.models.bucket_object import BucketObject


class BucketBrowserModel(BaseModel):
    """Model for the bucket browser. Manages bucket objects data."""
    
    def __init__(self):
        super().__init__()
        self._data: List[BucketObject] = []
        self._load_mock_data()
    
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
