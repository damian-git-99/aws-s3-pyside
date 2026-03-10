"""Mock helpers for testing Presenters without PySide6 widgets."""
from typing import List, Any, Optional
from unittest.mock import MagicMock

from src.mvp.base_view import BaseView
from src.mvp.contracts import IBucketObject


class MockView(BaseView):
    """Mock View for testing Presenters without actual PySide6 widgets.
    
    This mock implements all View methods and tracks calls for verification.
    """
    
    def __init__(self):
        # Don't call QWidget.__init__ to avoid Qt dependencies
        self._presenter = None
        self._displayed_data: List[IBucketObject] = []
        self._error_message: Optional[str] = None
        self._loading_shown: bool = False
        self._setup_ui_called: bool = False
    
    def setup_ui(self) -> None:
        """Mock setup_ui."""
        self._setup_ui_called = True
    
    def display_data(self, data: List[IBucketObject]) -> None:
        """Mock display_data - stores the data for verification."""
        self._displayed_data = data
    
    def show_error(self, message: str) -> None:
        """Mock show_error - stores the error message."""
        self._error_message = message
    
    def show_loading(self, show: bool = True) -> None:
        """Mock show_loading."""
        self._loading_shown = show
    
    # Helper methods for test verification
    def get_displayed_data(self) -> List[IBucketObject]:
        """Get the data that was displayed."""
        return self._displayed_data
    
    def get_error_message(self) -> Optional[str]:
        """Get the error message that was shown."""
        return self._error_message
    
    def was_setup_ui_called(self) -> bool:
        """Check if setup_ui was called."""
        return self._setup_ui_called
    
    def was_loading_shown(self) -> bool:
        """Check if loading was shown."""
        return self._loading_shown

    def show_error_with_retry(self, message: str, on_retry: callable) -> None:
        """Mock show_error_with_retry - stores the error message and callback."""
        self._error_message = message
        self._retry_callback = on_retry

    def show_load_more_button(self, show: bool = True) -> None:
        """Mock show_load_more_button."""
        self._load_more_button_visible = show

    def get_retry_callback(self) -> Optional[callable]:
        """Get the retry callback that was passed."""
        return getattr(self, '_retry_callback', None)

    def was_load_more_button_shown(self) -> bool:
        """Check if load more button was shown."""
        return getattr(self, '_load_more_button_visible', False)

    def _show_empty_state(self, show: bool = True) -> None:
        """Mock _show_empty_state."""
        self._empty_state_shown = show

    def was_empty_state_shown(self) -> bool:
        """Check if empty state was shown."""
        return getattr(self, '_empty_state_shown', False)

    def update_breadcrumb(self, path_segments) -> None:
        """Mock update_breadcrumb."""
        self._breadcrumb_segments = path_segments

    def enable_navigation_buttons(self, can_go_up: bool = True) -> None:
        """Mock enable_navigation_buttons."""
        self._can_go_up = can_go_up

    def get_breadcrumb_segments(self):
        """Get the breadcrumb segments that were set."""
        return getattr(self, '_breadcrumb_segments', None)

    def can_go_up(self) -> bool:
        """Check if up navigation was enabled."""
        return getattr(self, '_can_go_up', False)

    def setWindowTitle(self, title: str) -> None:
        """Mock setWindowTitle."""
        self._window_title = title

    def get_window_title(self) -> str:
        """Get the window title."""
        return getattr(self, '_window_title', '')

    def show_upload_dialog(self) -> Optional[str]:
        """Mock show_upload_dialog."""
        return getattr(self, '_upload_dialog_result', None)

    def show_upload_progress_dialog(self, file_path: str):
        """Mock show_upload_progress_dialog."""
        mock_dialog = MagicMock()
        self._progress_dialog = mock_dialog
        return mock_dialog

    def close_upload_progress_dialog(self, progress_dialog) -> None:
        """Mock close_upload_progress_dialog."""
        self._progress_dialog_closed = True

    def show_message(self, message: str) -> None:
        """Mock show_message."""
        self._message = message

    def set_upload_dialog_result(self, file_path: Optional[str]) -> None:
        """Set the result to return from show_upload_dialog."""
        self._upload_dialog_result = file_path

    def was_progress_dialog_closed(self) -> bool:
        """Check if progress dialog was closed."""
        return getattr(self, '_progress_dialog_closed', False)

    def get_message(self) -> Optional[str]:
        """Get the message that was shown."""
        return getattr(self, '_message', None)


def create_mock_view() -> MockView:
    """Factory function to create a MockView instance."""
    return MockView()
