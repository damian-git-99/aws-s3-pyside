from typing import List, Optional, Tuple

from src.mvp.base_presenter import BasePresenter
from src.models.bucket_browser_model import BucketBrowserModel
from src.models.bucket_object import BucketObject
from src.views.bucket_browser_view import BucketBrowserView
from src.services.s3_service import S3FileService, S3ListResult
from src.services.s3_errors import (
    S3AccessDeniedError,
    S3BucketNotFoundError,
    S3ConnectionError,
    S3CredentialsError,
)


class BucketBrowserPresenter(BasePresenter):
    """Presenter for the bucket browser.

    Manages the interaction between the S3 service, model, and view.
    Handles pagination, error handling, and user actions.

    Args:
        model: The bucket browser model
        view: The bucket browser view
        s3_service: Optional S3 file service (for testing/dependency injection)
    """

    def __init__(
        self,
        model: BucketBrowserModel,
        view: BucketBrowserView,
        s3_service: Optional[S3FileService] = None
    ):
        super().__init__(model, view)
        self._model: BucketBrowserModel = model
        self._view: BucketBrowserView = view
        self._s3_service: Optional[S3FileService] = s3_service
        self._continuation_token: Optional[str] = None
        self._is_truncated: bool = False
        self._all_objects: List[BucketObject] = []
        self._current_prefix: Optional[str] = None
        self._bucket_name: str = ""

    def initialize(self) -> None:
        """Initialize the presenter and load initial data."""
        if self._s3_service:
            self._bucket_name = self._s3_service.bucket_name
        else:
            self._bucket_name = "Bucket"
        self._load_bucket_contents()

    def navigate_to_folder(self, folder_name: str) -> None:
        """Navigate into a folder.
        
        Args:
            folder_name: Name of the folder to navigate into
        """
        if self._current_prefix:
            new_prefix = self._current_prefix + folder_name + "/"
        else:
            new_prefix = folder_name + "/"
        self.navigate_to_prefix(new_prefix)

    def navigate_to_prefix(self, prefix: Optional[str]) -> None:
        """Navigate to a specific prefix (folder path).
        
        Args:
            prefix: The prefix to navigate to (None for root)
        """
        self._current_prefix = prefix
        self._continuation_token = None
        self._is_truncated = False
        self._all_objects = []
        self._load_bucket_contents()

    def navigate_up(self) -> None:
        """Navigate to the parent directory."""
        if not self._current_prefix:
            return
        
        prefix_without_trailing = self._current_prefix.rstrip('/')
        if '/' not in prefix_without_trailing:
            if self._current_prefix:
                self.navigate_to_prefix(None)
        else:
            parent_prefix = prefix_without_trailing.rsplit('/', 1)[0] + "/"
            self.navigate_to_prefix(parent_prefix)

    def navigate_to_root(self) -> None:
        """Navigate to the root of the bucket."""
        self.navigate_to_prefix(None)

    def get_breadcrumb(self) -> List[Tuple[str, Optional[str]]]:
        """Get the breadcrumb path segments.
        
        Returns:
            List of tuples (display_name, prefix) for each segment
        """
        segments: List[Tuple[str, Optional[str]]] = []
        
        segments.append((self._bucket_name, None))
        
        if self._current_prefix:
            prefix_without_trailing = self._current_prefix.rstrip('/')
            parts = prefix_without_trailing.split('/')
            
            current_path = ""
            for part in parts:
                current_path += part + "/"
                segments.append((part, current_path))
        
        return segments

    def on_item_double_clicked(self, object_name: str, is_folder: bool) -> None:
        """Handle double-click on a table item.
        
        Args:
            object_name: Name of the clicked object
            is_folder: Whether the object is a folder
        """
        if is_folder:
            self.navigate_to_folder(object_name)

    def _update_navigation_ui(self) -> None:
        """Update the view with navigation UI elements."""
        breadcrumb = self.get_breadcrumb()
        self._view.update_breadcrumb(breadcrumb)
        
        can_go_up = self._current_prefix is not None
        self._view.enable_navigation_buttons(can_go_up=can_go_up)
        
        if self._current_prefix:
            path = "/" + self._current_prefix
            self._view.setWindowTitle(f"Bucket Browser - {self._bucket_name}{path}")
        else:
            self._view.setWindowTitle(f"Bucket Browser - {self._bucket_name}")

    def _load_bucket_contents(self, append: bool = False) -> None:
        """Load bucket contents from S3 service.

        Args:
            append: If True, append to existing data (for pagination).
                   If False, replace existing data.
        """
        if not self._s3_service:
            # Fallback to model data if no S3 service
            self._view.show_loading(True)
            try:
                data = self._model.get_data()
                self._view.display_data(data)
                self._update_navigation_ui()
            except Exception as e:
                self._view.show_error(str(e))
            finally:
                self._view.show_loading(False)
            return

        self._view.show_loading(True)
        try:
            result = self._s3_service.list_objects(
                prefix=self._current_prefix,
                continuation_token=self._continuation_token if append else None
            )

            if append:
                self._all_objects.extend(result.objects)
            else:
                self._all_objects = result.objects

            self._continuation_token = result.continuation_token
            self._is_truncated = result.is_truncated

            self._view.display_data(self._all_objects)
            self._view.show_load_more_button(result.is_truncated)
            self._update_navigation_ui()

        except S3AccessDeniedError as e:
            self._view.show_error_with_retry(
                f"Access Denied: {e}",
                on_retry=self._load_bucket_contents
            )
        except S3BucketNotFoundError as e:
            self._view.show_error_with_retry(
                f"Bucket Not Found: {e}",
                on_retry=self._load_bucket_contents
            )
        except S3CredentialsError as e:
            self._view.show_error_with_retry(
                f"Invalid Credentials: {e}",
                on_retry=self._load_bucket_contents
            )
        except S3ConnectionError as e:
            self._view.show_error_with_retry(
                f"Connection Error: {e}",
                on_retry=self._load_bucket_contents
            )
        except Exception as e:
            self._view.show_error_with_retry(
                f"Unexpected Error: {e}",
                on_retry=self._load_bucket_contents
            )
        finally:
            self._view.show_loading(False)

    def load_more(self) -> None:
        """Load next page of bucket contents."""
        if self._is_truncated and self._continuation_token:
            self._load_bucket_contents(append=True)

    def update_view(self) -> None:
        """Update the view with current model data."""
        self._view.display_data(self._all_objects)

    def on_refresh_clicked(self) -> None:
        """Handle refresh button click."""
        # Reset pagination and reload
        self._continuation_token = None
        self._is_truncated = False
        self._all_objects = []
        self._load_bucket_contents(append=False)

    def on_upload_clicked(self) -> None:
        """Handle upload button click."""
        # Placeholder - no functionality for now
        # This will be implemented when upload feature is added
        pass
