from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BucketObject:
    """Represents a file or folder in a bucket.
    
    Attributes:
        name: Name of the object
        size: Size in bytes (0 for folders)
        last_modified: Last modification datetime
        storage_class: Storage class (e.g., 'STANDARD', 'IA', 'GLACIER')
        is_folder: Whether this is a folder
    """
    name: str
    size: int
    last_modified: datetime
    storage_class: str
    is_folder: bool = False
    
    def get_formatted_size(self) -> str:
        """Return human-readable size string.
        
        Returns:
            Formatted size like '1.5 MB', '2 GB', etc.
            Returns '--' for folders.
        """
        if self.is_folder:
            return "--"
        
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def get_icon_type(self) -> str:
        """Get the icon type based on file extension.
        
        Returns:
            Icon type: 'folder', 'image', 'document', 'code', 'archive', or 'generic'
        """
        if self.is_folder:
            return 'folder'
        
        extension = self.name.lower().split('.')[-1] if '.' in self.name else ''
        
        # Image files
        if extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']:
            return 'image'
        
        # Document files
        if extension in ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']:
            return 'document'
        
        # Code files
        if extension in ['py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'h', 'json', 'xml', 'yaml', 'yml']:
            return 'code'
        
        # Archive files
        if extension in ['zip', 'tar', 'gz', 'bz2', '7z', 'rar']:
            return 'archive'
        
        return 'generic'
