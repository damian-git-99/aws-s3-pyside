"""Tests for BucketBrowserPresenter."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.presenters.bucket_browser_presenter import BucketBrowserPresenter
from src.models.bucket_browser_model import BucketBrowserModel
from src.models.bucket_object import BucketObject
from src.services.s3_service import S3FileService, S3ListResult
from src.services.s3_errors import S3AccessDeniedError, S3BucketNotFoundError
from src.tests.mock_view import MockView


class TestBucketBrowserPresenter(unittest.TestCase):
    """Test cases for BucketBrowserPresenter."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = BucketBrowserModel()
        self.view = MockView()
        self.mock_s3_service = MagicMock(spec=S3FileService)
        self.presenter = BucketBrowserPresenter(
            self.model, self.view, s3_service=self.mock_s3_service
        )

    def test_presenter_creation_without_s3_service(self):
        """Test that presenter can be created without S3 service (uses model fallback)."""
        presenter = BucketBrowserPresenter(self.model, self.view)
        self.assertEqual(presenter.get_model(), self.model)
        self.assertEqual(presenter.get_view(), self.view)
        # Should not have S3 service initially
        self.assertIsNone(presenter._s3_service)

    def test_presenter_creation_with_s3_service(self):
        """Test that presenter accepts S3 service in constructor."""
        self.assertEqual(self.presenter.get_model(), self.model)
        self.assertEqual(self.presenter.get_view(), self.view)
        self.assertEqual(self.presenter._s3_service, self.mock_s3_service)

    def test_initialize_loads_data_from_s3(self):
        """Test that initialize loads data from S3 service."""
        # Arrange
        mock_objects = [
            BucketObject(name='file1.txt', size=1024, last_modified=datetime.now(), storage_class='STANDARD'),
            BucketObject(name='folder1', size=0, last_modified=datetime.now(), storage_class='FOLDER', is_folder=True),
        ]
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=mock_objects,
            continuation_token=None,
            is_truncated=False
        )

        # Act
        self.presenter.initialize()

        # Assert
        self.mock_s3_service.list_objects.assert_called_once_with(
            prefix=None,
            continuation_token=None
        )
        displayed_data = self.view.get_displayed_data()
        self.assertEqual(len(displayed_data), 2)
        self.assertFalse(self.view.was_loading_shown())

    def test_initialize_shows_load_more_button_when_truncated(self):
        """Test that Load More button is shown when there are more pages."""
        # Arrange
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=[BucketObject(name='file1.txt', size=1024, last_modified=datetime.now(), storage_class='STANDARD')],
            continuation_token='next_token',
            is_truncated=True
        )

        # Act
        self.presenter.initialize()

        # Assert
        self.assertTrue(self.view.was_load_more_button_shown())
        self.assertEqual(self.presenter._continuation_token, 'next_token')
        self.assertTrue(self.presenter._is_truncated)

    def test_load_more_loads_next_page(self):
        """Test that load_more fetches the next page using continuation token."""
        # Arrange - First page
        first_page_objects = [
            BucketObject(name='file1.txt', size=1024, last_modified=datetime.now(), storage_class='STANDARD'),
        ]
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=first_page_objects,
            continuation_token='token123',
            is_truncated=True
        )
        self.presenter.initialize()

        # Arrange - Second page
        second_page_objects = [
            BucketObject(name='file2.txt', size=2048, last_modified=datetime.now(), storage_class='STANDARD'),
        ]
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=second_page_objects,
            continuation_token=None,
            is_truncated=False
        )

        # Act
        self.presenter.load_more()

        # Assert
        self.mock_s3_service.list_objects.assert_called_with(
            prefix=None,
            continuation_token='token123'
        )
        displayed_data = self.view.get_displayed_data()
        self.assertEqual(len(displayed_data), 2)  # Both pages combined

    def test_update_view_displays_current_data(self):
        """Test that update_view displays the current data."""
        # Arrange - Load some data first
        mock_objects = [BucketObject(name='test.txt', size=100, last_modified=datetime.now(), storage_class='STANDARD')]
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=mock_objects,
            continuation_token=None,
            is_truncated=False
        )
        self.presenter.initialize()

        # Act
        self.view._displayed_data = []  # Clear displayed data
        self.presenter.update_view()

        # Assert
        displayed_data = self.view.get_displayed_data()
        self.assertEqual(len(displayed_data), 1)

    def test_on_refresh_clicked_resets_and_reloads(self):
        """Test that refresh resets pagination and reloads data."""
        # Arrange - Load with pagination
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=[BucketObject(name='file1.txt', size=1024, last_modified=datetime.now(), storage_class='STANDARD')],
            continuation_token='token123',
            is_truncated=True
        )
        self.presenter.initialize()
        self.assertEqual(self.presenter._continuation_token, 'token123')

        # Act - Refresh
        self.mock_s3_service.list_objects.reset_mock()
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=[BucketObject(name='file1.txt', size=1024, last_modified=datetime.now(), storage_class='STANDARD')],
            continuation_token=None,
            is_truncated=False
        )
        self.presenter.on_refresh_clicked()

        # Assert
        self.assertIsNone(self.presenter._continuation_token)
        self.assertFalse(self.presenter._is_truncated)
        self.mock_s3_service.list_objects.assert_called_once_with(
            prefix=None,
            continuation_token=None
        )

    def test_s3_access_denied_error(self):
        """Test handling of S3AccessDeniedError."""
        # Arrange
        self.mock_s3_service.list_objects.side_effect = S3AccessDeniedError('test-bucket')

        # Act
        self.presenter.initialize()

        # Assert
        self.assertIsNotNone(self.view.get_error_message())
        self.assertIn('Access Denied', self.view.get_error_message())
        retry_callback = self.view.get_retry_callback()
        self.assertIsNotNone(retry_callback)

    def test_s3_bucket_not_found_error(self):
        """Test handling of S3BucketNotFoundError."""
        # Arrange
        self.mock_s3_service.list_objects.side_effect = S3BucketNotFoundError('test-bucket')

        # Act
        self.presenter.initialize()

        # Assert
        self.assertIsNotNone(self.view.get_error_message())
        self.assertIn('Bucket Not Found', self.view.get_error_message())

    def test_on_upload_clicked_does_nothing(self):
        """Test that upload click does nothing (placeholder)."""
        # Act - should not raise any exceptions
        self.presenter.on_upload_clicked()

        # Assert - view state should be unchanged
        self.assertIsNone(self.view.get_error_message())

    def test_empty_bucket_shows_empty_state(self):
        """Test that empty bucket shows empty state message."""
        # Arrange
        self.mock_s3_service.list_objects.return_value = S3ListResult(
            objects=[],
            continuation_token=None,
            is_truncated=False
        )

        # Act
        self.presenter.initialize()

        # Assert
        displayed_data = self.view.get_displayed_data()
        self.assertEqual(len(displayed_data), 0)
        # Empty state should be shown (via _show_empty_state call in display_data)


class TestBucketBrowserPresenterFallback(unittest.TestCase):
    """Test cases for presenter fallback to model when S3 service not available."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = BucketBrowserModel()
        self.view = MockView()
        # Create presenter without S3 service
        self.presenter = BucketBrowserPresenter(self.model, self.view)

    def test_initialize_uses_model_when_no_s3_service(self):
        """Test that initialize falls back to model when S3 service not available."""
        # Act
        self.presenter.initialize()

        # Assert - Should display model's mock data
        displayed_data = self.view.get_displayed_data()
        self.assertGreater(len(displayed_data), 0)
        self.assertFalse(self.view.was_loading_shown())


if __name__ == '__main__':
    unittest.main()
