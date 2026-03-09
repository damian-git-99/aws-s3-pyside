from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from PySide6.QtCore import QObject, Signal


class ModelSignals(QObject):
    """Qt signals for Model-Presenter communication."""
    data_changed = Signal()
    data_loaded = Signal()
    error_occurred = Signal(str)


class BaseModel(ABC):
    """Base class for all Models in the MVP architecture.
    
    The Model is responsible for:
    - Managing data and business logic
    - Notifying the Presenter about data changes via Qt signals
    - No knowledge of the UI (no PySide6 widget imports)
    """
    
    def __init__(self):
        self.signals = ModelSignals()
    
    def notify_data_changed(self) -> None:
        """Emit signal when data changes."""
        self.signals.data_changed.emit()
    
    def notify_data_loaded(self) -> None:
        """Emit signal when data is loaded."""
        self.signals.data_loaded.emit()
    
    def notify_error(self, message: str) -> None:
        """Emit signal when an error occurs."""
        self.signals.error_occurred.emit(message)
    
    @abstractmethod
    def load_data(self) -> None:
        """Load data from the data source. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_data(self) -> Any:
        """Return the current data. Must be implemented by subclasses."""
        pass
