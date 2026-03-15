# settings-management Specification

## Purpose
Manages application configuration with persistent storage using SQLite. Provides first-time setup wizard and settings editing interface for AWS credentials and application preferences.

## Requirements

### Requirement: Persist configuration in SQLite
The system SHALL store all configuration data in a SQLite database file located in the user's data directory.

#### Scenario: Configuration file created on first write
- **WHEN** the application saves a setting for the first time
- **THEN** a SQLite database file is created in the user's data directory
- **AND** the database contains a `settings` table with columns: key, value, created_at, updated_at

#### Scenario: Configuration persists between sessions
- **WHEN** the application saves a setting with key "api_url" and value "https://api.example.com"
- **AND** the application is closed and reopened
- **THEN** the system retrieves the value "https://api.example.com" for key "api_url"

### Requirement: First-time setup wizard
The system SHALL display a setup wizard on first launch when no configuration exists.

#### Scenario: Setup wizard shown on first launch
- **WHEN** the application starts and no configuration database exists
- **THEN** the setup wizard dialog is displayed before the main window
- **AND** the wizard prompts for required environment variables

#### Scenario: Setup wizard not shown on subsequent launches
- **WHEN** the application starts and a configuration database already exists
- **THEN** the main application window is displayed immediately
- **AND** the setup wizard is NOT shown

#### Scenario: Setup wizard saves configuration
- **WHEN** the user completes the setup wizard with valid inputs
- **THEN** the configuration is saved to SQLite
- **AND** the main application window is displayed

### Requirement: Settings button in toolbar
The system SHALL provide a settings button in the main toolbar for accessing configuration.

#### Scenario: Settings button visible in toolbar
- **WHEN** the main application window is displayed
- **THEN** a settings button is visible in the toolbar

#### Scenario: Settings dialog opens on button click
- **WHEN** the user clicks the settings button in the toolbar
- **THEN** the settings dialog/panel is displayed
- **AND** current configuration values are loaded

### Requirement: Settings editing interface
The system SHALL provide an interface for viewing and editing configuration values.

#### Scenario: Display current settings
- **WHEN** the settings panel is opened
- **THEN** all stored configuration keys and values are displayed
- **AND** values are editable

#### Scenario: Save modified settings
- **WHEN** the user modifies a configuration value and clicks save
- **THEN** the new value is persisted to SQLite
- **AND** the updated_at timestamp is refreshed

#### Scenario: Validate required fields
- **WHEN** the user attempts to save settings with empty required fields
- **THEN** an error message is displayed
- **AND** the settings are NOT saved

#### Scenario: Cancel settings changes
- **WHEN** the user clicks cancel in the settings dialog
- **THEN** no changes are saved
- **AND** the dialog closes

### Requirement: PyInstaller compatibility
The system SHALL persist configuration correctly when running as a PyInstaller bundle.

#### Scenario: Configuration persists in PyInstaller build
- **WHEN** the application runs as a PyInstaller executable
- **AND** the user saves configuration changes
- **THEN** the changes persist after closing and reopening the application
- **AND** the database is stored in the user's data directory, not in the temporary bundle directory
