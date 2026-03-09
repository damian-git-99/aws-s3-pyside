from typing import Protocol, Any, List, Optional
from datetime import datetime


class IBucketObject(Protocol):
    """Protocol for bucket objects (files and folders)."""
    
    name: str
    size: int
    last_modified: datetime
    storage_class: str
    is_folder: bool
    
    def get_formatted_size(self) -> str:
        """Return human-readable size string."""
        ...


class IBucketBrowserModel(Protocol):
    """Protocol for Bucket Browser Model."""
    
    def load_data(self) -> None:
        """Load bucket data."""
        ...
    
    def get_data(self) -> List[IBucketObject]:
        """Return list of bucket objects."""
        ...
    
    def refresh_data(self) -> None:
        """Refresh data from source."""
        ...


class IBucketBrowserView(Protocol):
    """Protocol for Bucket Browser View."""
    
    def set_presenter(self, presenter: Any) -> None:
        """Set the presenter for this view."""
        ...
    
    def display_data(self, data: List[IBucketObject]) -> None:
        """Display bucket objects in the view."""
        ...
    
    def setup_ui(self) -> None:
        """Setup the UI components."""
        ...
    
    def show_error(self, message: str) -> None:
        """Show error message."""
        ...


class IBucketBrowserPresenter(Protocol):
    """Protocol for Bucket Browser Presenter."""
    
    def initialize(self) -> None:
        """Initialize the presenter."""
        ...
    
    def update_view(self) -> None:
        """Update the view with current data."""
        ...
    
    def on_refresh_clicked(self) -> None:
        """Handle refresh button click."""
        ...
    
    def on_upload_clicked(self) -> None:
        """Handle upload button click."""
        ...
