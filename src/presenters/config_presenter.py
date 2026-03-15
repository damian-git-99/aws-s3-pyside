"""Config presenter for managing settings interactions."""

from typing import Optional
from PySide6.QtWidgets import QWidget

from src.config.config_manager import ConfigManager
from src.views.setup_wizard_view import SetupWizardDialog
from src.views.settings_panel_view import SettingsPanel


class ConfigPresenter:
    """Presenter for configuration management.
    
    Coordinates between ConfigManager (Model) and the settings views.
    Handles business logic for setup wizard and settings panel.
    """
    
    def __init__(self, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        """Initialize the config presenter.
        
        Args:
            config_manager: Configuration manager instance
            parent: Parent widget for dialogs
        """
        self._config_manager = config_manager
        self._parent = parent
        self._setup_wizard: Optional[SetupWizardDialog] = None
        self._settings_panel: Optional[SettingsPanel] = None
    
    def show_setup_wizard(self) -> bool:
        """Show the setup wizard dialog.
        
        Returns:
            True if user completed setup, False if cancelled
        """
        self._setup_wizard = SetupWizardDialog(self._parent)
        
        # Connect callbacks
        self._setup_wizard.set_on_finish_callback(self._on_setup_wizard_finish)
        self._setup_wizard.set_on_cancel_callback(self._on_setup_wizard_cancel)
        
        # Show dialog modally
        result = self._setup_wizard.exec()
        
        # Clean up
        self._setup_wizard = None
        
        return result == SetupWizardDialog.DialogCode.Accepted
    
    def _on_setup_wizard_finish(self, settings: dict):
        """Handle setup wizard finish.
        
        Args:
            settings: Dictionary of settings from the wizard
        """
        self.save_initial_config(settings)
    
    def _on_setup_wizard_cancel(self):
        """Handle setup wizard cancel."""
        # Configuration was not saved, user will exit
        pass
    
    def save_initial_config(self, settings: dict):
        """Save initial configuration from setup wizard.
        
        Args:
            settings: Dictionary of settings to save
        """
        self._config_manager.set_many(settings)
    
    def show_settings_panel(self):
        """Show the settings panel dialog."""
        self._settings_panel = SettingsPanel(self._parent)
        
        # Load current settings
        current_settings = self._config_manager.get_all()
        self._settings_panel.load_settings(current_settings)
        
        # Set database path
        self._settings_panel.set_db_path(self._config_manager._db_path)
        
        # Connect callbacks
        self._settings_panel.set_on_save_callback(self._on_settings_save)
        self._settings_panel.set_on_cancel_callback(self._on_settings_cancel)
        
        # Show dialog modally
        self._settings_panel.exec()
        
        # Clean up
        self._settings_panel = None
    
    def _on_settings_save(self, settings: dict):
        """Handle settings panel save.
        
        Args:
            settings: Dictionary of updated settings
        """
        self.save_settings(settings)
    
    def _on_settings_cancel(self):
        """Handle settings panel cancel."""
        # Changes were not saved
        pass
    
    def save_settings(self, settings: dict):
        """Save settings to configuration.
        
        Args:
            settings: Dictionary of settings to save
        """
        self._config_manager.set_many(settings)
    
    def cancel_settings(self):
        """Cancel settings changes.
        
        This method can be called to reset any pending changes.
        """
        # Currently, changes are only applied on save, so no action needed
        pass
    
    def connect_signals(self):
        """Connect ConfigManager signals to view updates.
        
        This method connects the configuration manager's signals
        to any views that need to react to configuration changes.
        """
        # Connect config_saved signal
        self._config_manager.config_saved.connect(self._on_config_saved)
        
        # Connect config_changed signal for individual key changes
        self._config_manager.config_changed.connect(self._on_config_changed)
    
    def _on_config_saved(self):
        """Handle configuration saved event."""
        # Could notify other parts of the app that config changed
        pass
    
    def _on_config_changed(self, key: str, value: str):
        """Handle individual configuration change event.
        
        Args:
            key: Configuration key that changed
            value: New configuration value
        """
        # Could notify other parts of the app about specific key changes
        pass
    
    def is_configured(self) -> bool:
        """Check if application has minimum required configuration.
        
        Returns:
            True if at least basic configuration exists
        """
        return self._config_manager.has_config()
    
    def is_fully_configured(self) -> bool:
        """Check if all required configuration is present.
        
        Returns:
            True if all required configuration keys have values
        """
        return self._config_manager.is_fully_configured()
    
    def get_missing_config_keys(self) -> list[str]:
        """Get list of required configuration keys that are missing.
        
        Returns:
            List of missing configuration key names
        """
        return self._config_manager.get_missing_keys()
