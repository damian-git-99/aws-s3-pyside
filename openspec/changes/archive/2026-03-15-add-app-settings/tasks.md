## 1. Config Module Setup (Model)

- [x] 1.1 Create `src/config/__init__.py` with module exports
- [x] 1.2 Implement `ConfigManager` class with SQLite connection handling
- [x] 1.3 Create database schema initialization (settings table)
- [x] 1.4 Implement `get(key)` method to retrieve settings
- [x] 1.5 Implement `set(key, value)` method to save settings
- [x] 1.6 Implement `has_config()` method to check if any config exists
- [x] 1.7 Add Qt signals: `config_changed`, `config_saved`
- [x] 1.8 Implement config file path resolution (user data directory, PyInstaller compatible)

## 2. Setup Wizard View

- [x] 2.1 Create `src/views/setup_wizard_view.py` with SetupWizardDialog class
- [x] 2.2 Design wizard UI with form inputs for required environment variables
- [x] 2.3 Add validation for required fields
- [x] 2.4 Add "Finish" and "Cancel" buttons with proper handlers
- [x] 2.5 Connect signals to presenter callbacks

## 3. Settings Panel View

- [x] 3.1 Create `src/views/settings_panel_view.py` with SettingsPanel class
- [x] 3.2 Design settings panel UI with editable key-value pairs
- [x] 3.3 Add "Save" and "Cancel" buttons
- [x] 3.4 Implement `load_settings(settings_dict)` method
- [x] 3.5 Implement `get_settings()` method to retrieve current values
- [x] 3.6 Add validation feedback for invalid inputs
- [x] 3.7 Connect signals to presenter callbacks

## 4. Config Presenter

- [x] 4.1 Create `src/presenters/config_presenter.py` with ConfigPresenter class
- [x] 4.2 Implement `show_setup_wizard()` method
- [x] 4.3 Implement `save_initial_config(settings_dict)` method
- [x] 4.4 Implement `show_settings_panel()` method
- [x] 4.5 Implement `save_settings(settings_dict)` method
- [x] 4.6 Implement `cancel_settings()` method
- [x] 4.7 Connect ConfigManager signals to view updates

## 5. Main Application Integration

- [x] 5.1 Modify `src/main.py` to import ConfigManager
- [x] 5.2 Add logic to check for existing config on startup
- [x] 5.3 Show SetupWizard before main window if no config exists
- [x] 5.4 Add settings button to main window toolbar
- [x] 5.5 Connect settings button to ConfigPresenter.show_settings_panel()
- [x] 5.6 Initialize ConfigPresenter in main application flow

## 6. Testing and Validation

- [x] 6.1 Test first-time launch shows setup wizard
- [x] 6.2 Test subsequent launches skip wizard
- [x] 6.3 Test settings persistence across restarts
- [x] 6.4 Test settings button opens settings panel
- [x] 6.5 Test save/cancel functionality in settings panel
- [x] 6.6 Test validation of required fields
- [x] 6.7 Create PyInstaller build and test config persistence
- [x] 6.8 Verify SQLite file location in user data directory (not temp)

## 7. Documentation

- [x] 7.1 Add docstrings to ConfigManager methods
- [x] 7.2 Add docstrings to ConfigPresenter methods
- [x] 7.3 Add docstrings to view classes
- [x] 7.4 Update README.md with configuration usage instructions
