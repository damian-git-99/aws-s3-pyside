from typing import List, Optional, Tuple
import os
import logging

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

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

logger = logging.getLogger(__name__)


class ProgressFileReader:
    """File wrapper that tracks read progress and emits updates via Qt signal."""
    
    def __init__(self, file_path: str, progress_signal):
        self._file = open(file_path, 'rb')
        self._size = os.path.getsize(file_path)
        self._read = 0
        self._progress_signal = progress_signal
        self._last_percentage = -1
        self.name = os.path.basename(file_path)
    
    def read(self, size=-1):
        data = self._file.read(size)
        self._read += len(data)
        percentage = int((self._read / self._size) * 100)
        if percentage != self._last_percentage:
            self._last_percentage = percentage
            self._progress_signal.emit(percentage)
        return data
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self._file.close()


class UploadWorker(QThread):
    """Worker thread for uploading files to S3.
    
    Signals:
        progress: Emitted with percentage (0-100) during upload
        finished: Emitted when upload completes successfully
        error: Emitted when upload fails with error message
    """

    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(
        self, s3_service: S3FileService, file_path: str, prefix: Optional[str] = None
    ):
        super().__init__()
        self._s3_service = s3_service
        self._file_path = file_path
        self._prefix = prefix
        self._cancelled = False

    def run(self) -> None:
        """Execute the upload operation in background thread."""
        try:
            with ProgressFileReader(self._file_path, self.progress) as f:
                self._s3_service.upload_fileobj_to_prefix(
                    file_obj=f,
                    prefix=self._prefix
                )
            if not self._cancelled:
                self.finished.emit()
        except Exception as e:
            if not self._cancelled:
                self.error.emit(str(e))

    def cancel(self) -> None:
        """Request cancellation of the upload."""
        self._cancelled = True


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
        s3_service: Optional[S3FileService] = None,
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
        self._upload_worker: Optional[UploadWorker] = None

    def initialize(self) -> None:
        """Initialize the presenter and load initial data."""
        logger.debug("Initialize: starting")
        if self._s3_service:
            self._bucket_name = self._s3_service.bucket_name
            logger.debug(f"Initialize: S3 service found, bucket={self._bucket_name}")
            # Set S3 service in model for deletion operations
            self._model.set_s3_service(self._s3_service)
            logger.debug("Initialize: S3 service set in model")
        else:
            self._bucket_name = "Bucket"
            logger.debug("Initialize: No S3 service, using mock")
        
        logger.debug("Initialize: connecting model signals")
        # Connect model signals
        self._model.signals.file_deleted.connect(self._on_file_deleted)
        self._model.signals.error_occurred.connect(self._on_model_error)
        self._model.signals.folder_created.connect(self._on_folder_created)
        self._model.signals.folder_creation_error.connect(self._on_folder_creation_error)
        
        logger.debug("Initialize: loading bucket contents")
        self._load_bucket_contents()
        logger.debug("Initialize: complete")

    def navigate_to_folder(self, folder_name: str) -> None:
        """Navigate into a folder.

        Args:
            folder_name: Name of the folder to navigate into
        """
        logger.debug(f"navigate_to_folder called with: {folder_name}")
        if self._current_prefix:
            new_prefix = self._current_prefix + folder_name + "/"
        else:
            new_prefix = folder_name + "/"
        logger.debug(f"new_prefix: {new_prefix}")
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

        prefix_without_trailing = self._current_prefix.rstrip("/")
        if "/" not in prefix_without_trailing:
            if self._current_prefix:
                self.navigate_to_prefix(None)
        else:
            parent_prefix = prefix_without_trailing.rsplit("/", 1)[0] + "/"
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
            prefix_without_trailing = self._current_prefix.rstrip("/")
            parts = prefix_without_trailing.split("/")

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
        logger.debug(f"on_item_double_clicked: object={object_name}, is_folder={is_folder}")
        if is_folder:
            logger.debug(f"Navigating to folder: {object_name}")
            self.navigate_to_folder(object_name)
        logger.debug("on_item_double_clicked: complete")

    def _update_navigation_ui(self) -> None:
        """Update the view with navigation UI elements."""
        try:
            logger.debug("_update_navigation_ui: starting")
            breadcrumb = self.get_breadcrumb()
            logger.debug(f"_update_navigation_ui: breadcrumb={breadcrumb}")
            self._view.update_breadcrumb(breadcrumb)

            can_go_up = self._current_prefix is not None
            logger.debug(f"_update_navigation_ui: can_go_up={can_go_up}")
            self._view.enable_navigation_buttons(can_go_up=can_go_up)

            if self._current_prefix:
                path = "/" + self._current_prefix
                logger.debug(f"_update_navigation_ui: setting title with path={path}")
                self._view.setWindowTitle(f"Bucket Browser - {self._bucket_name}{path}")
            else:
                logger.debug("_update_navigation_ui: setting title to root")
                self._view.setWindowTitle(f"Bucket Browser - {self._bucket_name}")
            logger.debug("_update_navigation_ui: complete")
        except Exception as e:
            logger.error(f"_update_navigation_ui: error: {str(e)}", exc_info=True)
            self._view.show_error(f"Navigation UI Error: {str(e)}")

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
                continuation_token=self._continuation_token if append else None,
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
                f"Access Denied: {e}", on_retry=self._load_bucket_contents
            )
        except S3BucketNotFoundError as e:
            self._view.show_error_with_retry(
                f"Bucket Not Found: {e}", on_retry=self._load_bucket_contents
            )
        except S3CredentialsError as e:
            self._view.show_error_with_retry(
                f"Invalid Credentials: {e}", on_retry=self._load_bucket_contents
            )
        except S3ConnectionError as e:
            self._view.show_error_with_retry(
                f"Connection Error: {e}", on_retry=self._load_bucket_contents
            )
        except Exception as e:
            self._view.show_error_with_retry(
                f"Unexpected Error: {e}", on_retry=self._load_bucket_contents
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
        if not self._s3_service:
            self._view.show_error("Upload not available in mock mode")
            return

        file_path = self._view.show_upload_dialog()
        if not file_path:
            return

        # Cancel any existing upload
        if self._upload_worker and self._upload_worker.isRunning():
            self._upload_worker.cancel()
            self._upload_worker.wait()

        # Create progress dialog
        progress_dialog = self._view.show_upload_progress_dialog(file_path)

        # Create and configure worker
        self._upload_worker = UploadWorker(
            self._s3_service, file_path, self._current_prefix
        )

        # Connect signals - Qt automatically queues these to main thread
        self._upload_worker.progress.connect(progress_dialog.setValue)
        self._upload_worker.finished.connect(
            lambda: self._on_upload_finished(progress_dialog)
        )
        self._upload_worker.error.connect(
            lambda err: self._on_upload_error(err, progress_dialog)
        )
        progress_dialog.canceled.connect(self._upload_worker.cancel)

        # Start upload
        self._upload_worker.start()

    def _on_upload_finished(self, progress_dialog) -> None:
        """Handle successful upload completion."""
        self._view.close_upload_progress_dialog(progress_dialog)
        self._view.show_message("Upload completed successfully")
        self.on_refresh_clicked()
        if self._upload_worker:
            self._upload_worker = None

    def _on_upload_error(self, error_message: str, progress_dialog) -> None:
        """Handle upload error."""
        self._view.close_upload_progress_dialog(progress_dialog)
        self._view.show_error_with_retry(
            f"Upload failed: {error_message}", on_retry=self.on_upload_clicked
        )
        if self._upload_worker:
            self._upload_worker = None

    def handle_delete_file(self, filename: str) -> None:
        """Handle file deletion request from view.
        
        Shows a confirmation dialog and deletes the file if user confirms.
        
        Args:
            filename: Name of the file to delete (display name, not full key)
        """
        # Show confirmation dialog
        reply = QMessageBox.question(
            self._view,
            "Confirm Deletion",
            f"Are you sure you want to delete '{filename}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Default to No (safest choice)
        )
        
        if reply == QMessageBox.No:
            return  # User cancelled
        
        # Construct the full S3 key (path) for deletion
        if self._current_prefix:
            key = f"{self._current_prefix}{filename}"
        else:
            key = filename
        
        # Call model to delete the file
        try:
            self._model.delete_file(key)
        except Exception as e:
            self._view.show_error(f"Error deleting file: {str(e)}")

    def _on_file_deleted(self, filename: str) -> None:
        """Handle successful file deletion from model.
        
        Args:
            filename: Name of the deleted file
        """
        self._view.show_message(f"File '{filename}' deleted successfully")
        # Refresh the file list to show current state
        self.on_refresh_clicked()

    def on_create_folder_clicked(self) -> None:
        """Handle Create Folder button click."""
        if not self._s3_service:
            self._view.show_error("Create folder not available in mock mode")
            return
        
        # Show dialog and get folder name
        folder_name = self._view.show_create_folder_dialog()
        if not folder_name:
            return  # User cancelled
        
        # Create folder via model
        try:
            self._model.create_folder(self._current_prefix, folder_name)
        except Exception as e:
            self._view.show_error(f"Error creating folder: {str(e)}")
    
    def _on_folder_created(self, folder_name: str) -> None:
        """Handle successful folder creation from model.
        
        Args:
            folder_name: Name of the created folder
        """
        self._view.show_message(f"Folder '{folder_name}' created successfully")
        # Refresh the file list to show new folder
        self.on_refresh_clicked()
    
    def _on_folder_creation_error(self, error_message: str) -> None:
        """Handle folder creation error from model.
        
        Args:
            error_message: Error description
        """
        self._view.show_error(error_message)

    def _on_model_error(self, error_message: str) -> None:
        """Handle error signal from model.
        
        Args:
            error_message: Error description
        """
        self._view.show_error(error_message)
