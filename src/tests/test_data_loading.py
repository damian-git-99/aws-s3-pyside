"""Integration tests for bucket browser data loading."""
import unittest
from datetime import datetime

from src.models.bucket_browser_model import BucketBrowserModel
from src.models.bucket_object import BucketObject


class TestDataLoadingIntegration(unittest.TestCase):
    """Integration tests for data loading functionality."""
    
    def test_model_loads_mock_data(self):
        """Test that model loads mock data on initialization."""
        # Act
        model = BucketBrowserModel()
        
        # Assert
        data = model.get_data()
        self.assertGreater(len(data), 0)
    
    def test_mock_data_contains_folders_and_files(self):
        """Test that mock data contains both folders and files."""
        # Arrange
        model = BucketBrowserModel()
        
        # Act
        data = model.get_data()
        
        # Assert
        folders = [obj for obj in data if obj.is_folder]
        files = [obj for obj in data if not obj.is_folder]
        
        self.assertGreater(len(folders), 0, "Should have folders")
        self.assertGreater(len(files), 0, "Should have files")
    
    def test_folders_come_before_files(self):
        """Test that folders are listed before files."""
        # Arrange
        model = BucketBrowserModel()
        
        # Act
        data = model.get_data()
        
        # Assert
        folder_indices = [i for i, obj in enumerate(data) if obj.is_folder]
        file_indices = [i for i, obj in enumerate(data) if not obj.is_folder]
        
        if folder_indices and file_indices:
            max_folder_idx = max(folder_indices)
            min_file_idx = min(file_indices)
            self.assertLess(max_folder_idx, min_file_idx,
                          "All folders should come before files")
    
    def test_data_contains_expected_file_types(self):
        """Test that data contains various file types."""
        # Arrange
        model = BucketBrowserModel()
        
        # Act
        data = model.get_data()
        files = [obj for obj in data if not obj.is_folder]
        
        # Assert
        icon_types = set(obj.get_icon_type() for obj in files)
        expected_types = {'image', 'document', 'code', 'archive', 'generic'}
        
        for expected in expected_types:
            self.assertIn(expected, icon_types,
                         f"Should have at least one {expected} file")
    
    def test_bucket_object_has_required_attributes(self):
        """Test that bucket objects have all required attributes."""
        # Arrange
        model = BucketBrowserModel()
        
        # Act
        data = model.get_data()
        
        # Assert
        for obj in data:
            self.assertIsNotNone(obj.name)
            self.assertIsNotNone(obj.size)
            self.assertIsNotNone(obj.last_modified)
            self.assertIsNotNone(obj.storage_class)
            self.assertIsInstance(obj.is_folder, bool)
    
    def test_file_size_formatting(self):
        """Test that file sizes are formatted correctly."""
        # Arrange
        model = BucketBrowserModel()
        
        # Act
        data = model.get_data()
        files = [obj for obj in data if not obj.is_folder]
        
        # Assert
        for file in files:
            formatted = file.get_formatted_size()
            self.assertNotEqual(formatted, "--",
                              "Files should have formatted size")
            self.assertTrue(any(unit in formatted 
                              for unit in ['B', 'KB', 'MB', 'GB', 'TB']),
                          "Size should include unit")
    
    def test_folder_size_is_dash(self):
        """Test that folders show '--' for size."""
        # Arrange
        model = BucketBrowserModel()
        
        # Act
        data = model.get_data()
        folders = [obj for obj in data if obj.is_folder]
        
        # Assert
        for folder in folders:
            self.assertEqual(folder.get_formatted_size(), "--",
                           "Folders should show '--' for size")
    
    def test_refresh_data_changes_data(self):
        """Test that refresh can change data (due to randomness in mock)."""
        # Arrange
        model = BucketBrowserModel()
        original_data = model.get_data()
        
        # Act
        model.refresh_data()
        new_data = model.get_data()
        
        # Assert
        self.assertEqual(len(original_data), len(new_data),
                        "Should have same number of items after refresh")


if __name__ == '__main__':
    unittest.main()
