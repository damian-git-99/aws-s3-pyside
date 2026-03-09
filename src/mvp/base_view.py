from abc import abstractmethod
from typing import Any, Optional
from PySide6.QtWidgets import QWidget


class BaseView(QWidget):
    """Base class for all Views in the MVP architecture.
    
    The View is responsible for:
    - Displaying data to the user
    - Capturing user events and forwarding them to the Presenter
    - Being passive (no business logic, just presentation)
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._presenter: Optional[Any] = None
    
    def set_presenter(self, presenter: Any) -> None:
        """Set the presenter that will handle view events."""
        self._presenter = presenter
    
    def get_presenter(self) -> Optional[Any]:
        """Get the current presenter."""
        return self._presenter
    
    @abstractmethod
    def setup_ui(self) -> None:
        """Setup the UI components. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def display_data(self, data: Any) -> None:
        """Display data in the view. Must be implemented by subclasses."""
        pass
    
    def show_error(self, message: str) -> None:
        """Show an error message. Can be overridden by subclasses."""
        pass
    
    def show_loading(self, show: bool = True) -> None:
        """Show or hide loading indicator. Can be overridden by subclasses."""
        pass
