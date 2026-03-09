from typing import List

from src.mvp.base_presenter import BasePresenter
from src.models.bucket_browser_model import BucketBrowserModel
from src.models.bucket_object import BucketObject
from src.views.bucket_browser_view import BucketBrowserView


class BucketBrowserPresenter(BasePresenter):
    """Presenter for the bucket browser."""
    
    def __init__(self, model: BucketBrowserModel, view: BucketBrowserView):
        super().__init__(model, view)
        self._model: BucketBrowserModel = model
        self._view: BucketBrowserView = view
    
    def initialize(self) -> None:
        """Initialize the presenter and load initial data."""
        self._view.show_loading(True)
        try:
            data = self._model.get_data()
            self._view.display_data(data)
        except Exception as e:
            self._view.show_error(str(e))
        finally:
            self._view.show_loading(False)
    
    def update_view(self) -> None:
        """Update the view with current model data."""
        try:
            data = self._model.get_data()
            self._view.display_data(data)
        except Exception as e:
            self._view.show_error(str(e))
    
    def on_refresh_clicked(self) -> None:
        """Handle refresh button click."""
        self._view.show_loading(True)
        try:
            self._model.refresh_data()
            # update_view will be called via signal
        except Exception as e:
            self._view.show_error(str(e))
            self._view.show_loading(False)
    
    def on_upload_clicked(self) -> None:
        """Handle upload button click."""
        # Placeholder - no functionality for now
        # This will be implemented when upload feature is added
        pass
