from abc import ABC, abstractmethod
from typing import Any, Optional, TypeVar, Generic

from src.mvp.base_model import BaseModel
from src.mvp.base_view import BaseView


class BasePresenter(ABC):
    """Base class for all Presenters in the MVP architecture.
    
    The Presenter is responsible for:
    - Acting as intermediary between Model and View
    - Handling user events from the View
    - Reacting to Model data changes
    - Coordinating communication between Model and View
    """
    
    def __init__(self, model: BaseModel, view: BaseView):
        self._model = model
        self._view = view
        self._view.set_presenter(self)
        self._connect_model_signals()
    
    def _connect_model_signals(self) -> None:
        """Connect to Model signals to react to data changes."""
        self._model.signals.data_changed.connect(self._on_data_changed)
        self._model.signals.data_loaded.connect(self._on_data_loaded)
        self._model.signals.error_occurred.connect(self._on_error)
    
    def _on_data_changed(self) -> None:
        """Called when Model data changes. Override in subclasses."""
        self.update_view()
    
    def _on_data_loaded(self) -> None:
        """Called when Model data is loaded. Override in subclasses."""
        self.update_view()
    
    def _on_error(self, message: str) -> None:
        """Called when Model reports an error. Override in subclasses."""
        self._view.show_error(message)
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the presenter. Load initial data, etc."""
        pass
    
    @abstractmethod
    def update_view(self) -> None:
        """Update the view with current model data."""
        pass
    
    def get_model(self) -> BaseModel:
        """Get the associated model."""
        return self._model
    
    def get_view(self) -> BaseView:
        """Get the associated view."""
        return self._view
