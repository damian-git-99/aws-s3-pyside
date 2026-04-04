# Coding Conventions

**Analysis Date:** 2026-04-04

## Naming Patterns

**Files:**
- Lowercase with underscores (snake_case): `bucket_browser_model.py`, `s3_errors.py`
- Test files prefixed with `test_`: `test_bucket_browser_model.py`, `test_s3_service.py`

**Classes:**
- PascalCase with descriptive names: `BucketBrowserModel`, `S3AccessDeniedError`, `MockView`
- Abstract base classes prefixed with `Base`: `BaseModel`, `BaseView`, `BasePresenter`

**Functions/Methods:**
- snake_case: `get_data()`, `delete_file()`, `notify_data_changed()`
- Private methods prefixed with single underscore: `_load_mock_data()`, `_on_data_changed()`

**Variables:**
- snake_case: `bucket_name`, `continuation_token`, `_s3_service`
- Type hints used consistently: `model: BucketBrowserModel`, `s3_service: Optional[S3FileService]`

**Constants:**
- UPPER_CASE with underscores: Not heavily used; prefer module-level variables

## Code Style

**Formatting:**
- 4-space indentation
- 88 character line length (inferred from code samples)
- Double quotes for docstrings, single quotes acceptable elsewhere

**Type Hints:**
- Mandatory throughout codebase
- Use `Optional[T]` for nullable types: `Optional[str]`, `Optional[S3FileService]`
- Use `List[T]`, `Tuple[T, ...]`, `Any` from `typing` module
- Import types: `from typing import List, Optional, Tuple, Any`

**Docstrings:**
- Triple-quoted docstrings for all classes and public methods
- Follow Google style (description + Args + Returns + Raises)
- Example from `src/models/bucket_browser_model.py`:
```python
def delete_file(self, key: str) -> None:
    """Delete a file from S3 bucket.

    Args:
        key: The S3 key (path) of the file to delete (e.g., "folder/file.txt")

    Raises:
        Various S3Error subclasses on failure
    """
```

**Imports:**
- Standard library first: `import unittest`, `from datetime import datetime`
- Third-party next: `from PySide6.QtCore import Signal`, `from unittest.mock import MagicMock`
- Local application last: `from src.mvp.base_model import BaseModel`, `from src.services.s3_service import S3FileService`
- Relative imports NOT used (always absolute with `src.` prefix)

**Blank Lines:**
- 2 blank lines between top-level classes and functions
- 1 blank line between methods in a class

## Error Handling

**Patterns:**
1. **Custom Exception Hierarchy**: All S3 errors inherit from `S3Error` base class
   ```python
   class S3Error(Exception):
       """Base class for all S3-related errors."""
       pass
   ```

2. **Specific Error Types**: Create specific exceptions for each failure mode
   - `S3AccessDeniedError`, `S3BucketNotFoundError`, `S3ConnectionError`
   - Located in `src/services/s3_errors.py`

3. **Error Propagation with Context**: Include relevant context in error messages
   ```python
   class S3AccessDeniedError(S3Error):
       def __init__(self, bucket_name: str):
           self.bucket_name = bucket_name
           super().__init__(f"Access denied to bucket '{bucket_name}'...")
   ```

4. **Model-View Communication**: Use Qt signals for error notification
   - `error_occurred = Signal(str)` emits error messages to Presenter
   - `download_error = Signal(str)` for operation-specific errors

5. **Try-Except in Service Layer**: Catch boto3 exceptions, convert to domain errors
   ```python
   try:
       self._s3.list_objects_v2(...)
   except ClientError as e:
       code = e.response['Error']['Code']
       if code == '403':
           raise S3AccessDeniedError(self.bucket_name)
   ```

## Logging

**Framework:** Python `logging` module

**Usage Pattern:**
```python
import logging

logger = logging.getLogger(__name__)

# Debug for flow tracking
logger.debug(f"navigate_to_folder called with: {folder_name}")
logger.debug(f"new_prefix: {new_prefix}")

# Error with stack traces
logger.error(f"Error previewing image: {e}", exc_info=True)
```

**Levels:**
- `debug()`: Function entry/exit, state changes
- `info()`: User actions (uploads, downloads)
- `error()`: Exceptions with `exc_info=True` for stack traces

## Comments

**When to Comment:**
- Docstrings for all public APIs (required)
- Inline comments for complex logic only
- Type annotations replace parameter comments

**Style:**
- Complete sentences with proper punctuation
- Focus on "why" not "what" for inline comments

## Function Design

**Size:** 
- Keep functions under 50 lines
- Single responsibility principle

**Parameters:**
- Use type hints
- Use `Optional` for nullable parameters
- Named parameters for clarity in calls

**Return Values:**
- Use `-> None` for void returns
- Use `-> List[T]`, `-> Optional[T]` for typed returns
- Return early for guard clauses

**Example Pattern:**
```python
def navigate_to_folder(self, folder_name: str) -> None:
    """Navigate into a folder."""
    logger.debug(f"navigate_to_folder called with: {folder_name}")
    if self._current_prefix:
        new_prefix = self._current_prefix + folder_name + "/"
    else:
        new_prefix = folder_name + "/"
    self.navigate_to_prefix(new_prefix)
```

## Module Design

**Exports:**
- `__init__.py` files used for package organization
- Not using `__all__` exports (implicit exports allowed)

**MVP Architecture Pattern:**
- **Model**: `src/models/` - Data and business logic, emits Qt signals
- **View**: `src/views/` - UI components, passive, forwards events to Presenter
- **Presenter**: `src/presenters/` - Intermediary, handles user actions

**Package Structure:**
```
src/
├── mvp/              # Base MVP classes
├── models/           # Domain models
├── views/            # PySide6 widgets
├── presenters/       # Business logic coordinators
├── services/         # External service wrappers
├── utils/            # Shared utilities
└── tests/            # Test files
```

**Class Naming by Layer:**
- Model: `BucketBrowserModel`, `BucketObject` (dataclass)
- View: `BucketBrowserView`, `CreateFolderDialog`
- Presenter: `BucketBrowserPresenter`
- Service: `S3FileService`

## Testing Conventions

See `TESTING.md` for full testing patterns.

**Key Testing Conventions:**
- Test classes inherit from `unittest.TestCase`
- Test methods prefixed with `test_`
- Descriptive test names: `test_delete_file_success`, `test_empty_bucket_shows_empty_state`
- Arrange-Act-Assert pattern with explicit comments
- Use `MagicMock` for dependencies, `MockView` for Qt isolation

---

*Convention analysis: 2026-04-04*
