# pyinstaller-build Specification

## Purpose

Provide a mechanism to generate a standalone single-file executable from the PySide6 application source code using PyInstaller, allowing distribution without requiring Python or dependencies on the target system.

## Requirements

### Requirement: Single-file executable generation
The system SHALL provide a mechanism to generate a single-file executable from the PySide6 application source code.

#### Scenario: Developer builds executable
- **WHEN** the developer runs the build script
- **THEN** a single executable file SHALL be created in the dist/ directory

### Requirement: PySide6 GUI bundling
The generated executable SHALL properly bundle all PySide6 dependencies including Qt platform plugins required for the GUI to function.

#### Scenario: Executable runs without Python installed
- **WHEN** a user runs the generated executable on a system without Python installed
- **THEN** the PySide6 GUI application SHALL launch and function correctly

#### Scenario: Platform plugins are available
- **WHEN** the executable starts
- **THEN** the Qt platform plugin SHALL be found and loaded without errors

### Requirement: Hidden imports configuration
The build configuration SHALL include all necessary hidden imports for the MVP architecture modules (models, views, presenters).

#### Scenario: All modules load correctly
- **WHEN** the executable imports application modules
- **THEN** all MVP components SHALL be available and functional

### Requirement: Build script convenience
The system SHALL provide a simple build script that handles the PyInstaller invocation with proper parameters.

#### Scenario: Developer uses build script
- **WHEN** the developer runs `python build.py` or `uv run python build.py`
- **THEN** the executable SHALL be built without requiring manual pyinstaller command-line arguments

### Requirement: Cross-platform support
The build system SHALL support generating executables for Windows, Linux, and macOS from their respective platforms.

#### Scenario: Build on different platforms
- **WHEN** the build script is run on Windows
- **THEN** a Windows executable (.exe) SHALL be generated
- **WHEN** the build script is run on Linux
- **THEN** a Linux binary SHALL be generated
- **WHEN** the build script is run on macOS
- **THEN** a macOS application bundle SHALL be generated
