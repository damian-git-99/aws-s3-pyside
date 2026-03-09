## Purpose

Set up the basic PySide6 project structure with proper Python packaging and UV environment support.

## Requirements

## ADDED Requirements

### Requirement: Python project configuration
The project SHALL be configured as a Python package using pyproject.toml with PEP 517/518 standards.

#### Scenario: pyproject.toml exists
- **WHEN** examining project root
- **THEN** pyproject.toml file SHALL exist with valid configuration

### Requirement: PySide6 dependency
The project SHALL include PySide6 as a runtime dependency.

#### Scenario: PySide6 in dependencies
- **WHEN** checking pyproject.toml
- **THEN** PySide6 SHALL be listed in dependencies section

### Requirement: Project structure
The project SHALL follow standard Python package structure.

#### Scenario: src directory exists
- **WHEN** examining project directory
- **THEN** src/ directory SHALL exist containing the application package

### Requirement: Entry point
The project SHALL have a runnable entry point.

#### Scenario: main.py exists
- **WHEN** examining src/ directory
- **THEN** main.py SHALL exist and be executable as `python -m <package>`

### Requirement: UV environment support
The project SHALL support uv for creating isolated virtual environments without global installs.

#### Scenario: UV venv works
- **WHEN** running `uv venv` in project root
- **THEN** .venv directory SHALL be created with virtual environment

#### Scenario: UV sync installs dependencies
- **WHEN** running `uv sync` in project root
- **THEN** all dependencies from pyproject.toml SHALL be installed in .venv

#### Scenario: UV run executes application
- **WHEN** running `uv run python -m src.main`
- **THEN** application SHALL launch without requiring global package installations
