"""Tests for file icon system."""
import unittest
from datetime import datetime

from src.models.bucket_object import BucketObject
from src.utils.file_icons import FileIconManager


class TestFileIconSystem(unittest.TestCase):
    """Test cases for file icon system."""
    
    def test_folder_icon_type(self):
        """Test that folders return 'folder' icon type."""
        # Arrange
        folder = BucketObject(
            name="test_folder",
            size=0,
            last_modified=datetime.now(),
            storage_class="-",
            is_folder=True
        )
        
        # Act
        icon_type = folder.get_icon_type()
        
        # Assert
        self.assertEqual(icon_type, "folder")
    
    def test_image_file_icons(self):
        """Test that image files return 'image' icon type."""
        # Arrange
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
        
        for ext in image_extensions:
            with self.subTest(ext=ext):
                file = BucketObject(
                    name=f"image{ext}",
                    size=1024,
                    last_modified=datetime.now(),
                    storage_class="STANDARD",
                    is_folder=False
                )
                
                # Act
                icon_type = file.get_icon_type()
                
                # Assert
                self.assertEqual(icon_type, "image")
    
    def test_document_file_icons(self):
        """Test that document files return 'document' icon type."""
        # Arrange
        doc_extensions = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt']
        
        for ext in doc_extensions:
            with self.subTest(ext=ext):
                file = BucketObject(
                    name=f"doc{ext}",
                    size=1024,
                    last_modified=datetime.now(),
                    storage_class="STANDARD",
                    is_folder=False
                )
                
                # Act
                icon_type = file.get_icon_type()
                
                # Assert
                self.assertEqual(icon_type, "document")
    
    def test_code_file_icons(self):
        """Test that code files return 'code' icon type."""
        # Arrange
        code_extensions = ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', 
                          '.h', '.json', '.xml', '.yaml', '.yml']
        
        for ext in code_extensions:
            with self.subTest(ext=ext):
                file = BucketObject(
                    name=f"code{ext}",
                    size=1024,
                    last_modified=datetime.now(),
                    storage_class="STANDARD",
                    is_folder=False
                )
                
                # Act
                icon_type = file.get_icon_type()
                
                # Assert
                self.assertEqual(icon_type, "code")
    
    def test_archive_file_icons(self):
        """Test that archive files return 'archive' icon type."""
        # Arrange
        archive_extensions = ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar']
        
        for ext in archive_extensions:
            with self.subTest(ext=ext):
                file = BucketObject(
                    name=f"archive{ext}",
                    size=1024,
                    last_modified=datetime.now(),
                    storage_class="STANDARD",
                    is_folder=False
                )
                
                # Act
                icon_type = file.get_icon_type()
                
                # Assert
                self.assertEqual(icon_type, "archive")
    
    def test_generic_file_icon(self):
        """Test that unknown file types return 'generic' icon."""
        # Arrange
        file = BucketObject(
            name="unknown.xyz",
            size=1024,
            last_modified=datetime.now(),
            storage_class="STANDARD",
            is_folder=False
        )
        
        # Act
        icon_type = file.get_icon_type()
        
        # Assert
        self.assertEqual(icon_type, "generic")
    
    def test_file_without_extension(self):
        """Test that files without extension return 'generic' icon."""
        # Arrange
        file = BucketObject(
            name="no_extension",
            size=1024,
            last_modified=datetime.now(),
            storage_class="STANDARD",
            is_folder=False
        )
        
        # Act
        icon_type = file.get_icon_type()
        
        # Assert
        self.assertEqual(icon_type, "generic")
    
    def test_icon_manager_get_icon(self):
        """Test that FileIconManager can get icons for all types."""
        # Arrange
        icon_types = ['folder', 'image', 'document', 'code', 'archive', 'generic']
        
        # Act & Assert
        for icon_type in icon_types:
            with self.subTest(icon_type=icon_type):
                icon = FileIconManager.get_icon(icon_type)
                self.assertIsNotNone(icon)
    
    def test_icon_manager_caching(self):
        """Test that icons are cached."""
        # Act
        icon1 = FileIconManager.get_icon('folder')
        icon2 = FileIconManager.get_icon('folder')
        
        # Assert - should be the same object due to caching
        self.assertIs(icon1, icon2)
    
    def test_icon_manager_for_object(self):
        """Test getting icon for a bucket object."""
        # Arrange
        file = BucketObject(
            name="test.py",
            size=1024,
            last_modified=datetime.now(),
            storage_class="STANDARD",
            is_folder=False
        )
        
        # Act
        icon = FileIconManager.get_icon_for_object(file)
        
        # Assert
        self.assertIsNotNone(icon)


if __name__ == '__main__':
    unittest.main()
