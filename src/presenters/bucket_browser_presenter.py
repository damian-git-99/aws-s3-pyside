from typing import List, Optional

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

    def initialize(self) -> None:
        """Initialize the presenter and load initial data."""
        self._load_bucket_contents()

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
            except Exception as e:
                self._view.show_error(str(e))
            finally:
                self._view.show_loading(False)
            return

        self._view.show_loading(True)
        try:
            # Call S3 service at root level (no prefix for now)
            result = self._s3_service.list_objects(
                prefix=None,
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
