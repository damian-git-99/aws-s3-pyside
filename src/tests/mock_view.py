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


def create_mock_view() -> MockView:
    """Factory function to create a MockView instance."""
    return MockView()
