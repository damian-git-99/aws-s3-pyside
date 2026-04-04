# Testing Patterns

**Analysis Date:** 2026-04-04

## Test Framework

**Runner:**
- Python standard `unittest` module
- No external test runner configured
- Config: Not applicable (no pytest/vitest config)

**Run Commands:**
```bash
# Run all tests
uv run python -m unittest discover src/tests/

# Run specific test file
uv run python -m unittest src.tests.test_bucket_browser_presenter

# Run specific test class
uv run python -m unittest src.tests.test_bucket_browser_presenter.TestBucketBrowserPresenterNavigation

# Run single test method
uv run python -m unittest src.tests.test_bucket_browser_presenter.TestBucketBrowserPresenter.test_navigate_to_folder
```

## Test File Organization

**Location:**
- Co-located within `src/tests/` directory
- All test files in single flat directory (no subdirectories)

**Naming:**
- All test files prefixed with `test_`: `test_s3_service.py`, `test_file_icons.py`

**Structure:**
```
src/tests/
├── __init__.py
├── mock_view.py              # Mock implementations
├── test_bucket_browser_model.py
├── test_bucket_browser_presenter.py
├── test_config.py
├── test_data_loading.py
├── test_file_icons.py
├── test_s3_errors.py
└── test_s3_service.py
```

## Test Structure

**Suite Organization:**
```python
import unittest
from unittest.mock import MagicMock, patch
from src.models.bucket_browser_model import BucketBrowserModel


class TestBucketBrowserModel(unittest.TestCase):
    """Test cases for BucketBrowserModel."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = BucketBrowserModel()
        self.mock_s3_service = MagicMock(spec=S3FileService)
        self.model.set_s3_service(self.mock_s3_service)

    def test_delete_file_success(self):
        """Model should successfully delete a file."""
        # Arrange
        file_deleted_signal_received = []
        self.model.signals.file_deleted.connect(
            lambda filename: file_deleted_signal_received.append(filename)
        )

        # Act
        self.model.delete_file('test-file.txt')

        # Assert
        self.mock_s3_service.delete_object.assert_called_once_with('test-file.txt')
        self.assertEqual(len(file_deleted_signal_received), 1)
```

**Patterns:**

1. **Arrange-Act-Assert with Comments:**
   ```python
   # Arrange
   mock_objects = [BucketObject(...)]
   self.mock_s3_service.list_objects.return_value = S3ListResult(...)

   # Act
   self.presenter.initialize()

   # Assert
   self.mock_s3_service.list_objects.assert_called_once()
   ```

2. **Signal Testing Pattern:**
   ```python
   signal_received = []
   self.model.signals.file_deleted.connect(
       lambda filename: signal_received.append(filename)
   )
   
   self.model.delete_file('test.txt')
   
   self.assertEqual(len(signal_received), 1)
   self.assertEqual(signal_received[0], 'test.txt')
   ```

3. **Side Effect Testing for Errors:**
   ```python
   self.mock_s3_service.delete_object.side_effect = S3AccessDeniedError('test-bucket')
   
   self.model.delete_file('file.txt')
   
   self.assertEqual(len(error_signal_received), 1)
   self.assertIn('Access denied', error_signal_received[0])
   ```

## Mocking

**Framework:** `unittest.mock` (standard library)

**Patterns:**

1. **Dependency Injection via Constructor:**
   ```python
   def setUp(self):
       self.model = BucketBrowserModel()
       self.view = MockView()
       self.mock_s3_service = MagicMock(spec=S3FileService)
       self.presenter = BucketBrowserPresenter(
           self.model, self.view, s3_service=self.mock_s3_service
       )
   ```

2. **Qt Widget Mocking with MockView:**
   - Located in `src/tests/mock_view.py`
   - Implements `BaseView` interface without Qt dependencies
   - Tracks method calls and state for verification
   ```python
   class MockView(BaseView):
       def __init__(self):
           self._presenter = None
           self._displayed_data: List[IBucketObject] = []
           self.messages: List[str] = []
           self.errors: List[str] = []
       
       def show_error(self, message: str) -> None:
           self._error_message = message
           self.errors.append(message)
   ```

3. **Patching for External Dependencies:**
   ```python
   from PySide6.QtWidgets import QMessageBox
   
   with patch('PySide6.QtWidgets.QMessageBox.question') as mock_question:
       mock_question.return_value = QMessageBox.Yes
       self.presenter.handle_delete_file('file.txt')
   ```

4. **Environment Variable Mocking:**
   ```python
   def setUp(self):
       self.original_env = {...}
       for key in self.original_env:
           if key in os.environ:
               del os.environ[key]

   def tearDown(self):
       for key, value in self.original_env.items():
           if value is not None:
               os.environ[key] = value
   ```

5. **Botocore Client Mocking:**
   ```python
   self.mock_s3_client = MagicMock()
   self.service = S3FileService(
       bucket_name="test-bucket",
       s3_client=self.mock_s3_client
   )
   ```

**What to Mock:**
- AWS S3 client (`boto3`)
- Qt widgets (use `MockView`)
- File system operations
- Environment variables
- Time-dependent functions (if deterministic behavior needed)

**What NOT to Mock:**
- Data classes and simple value objects
- Internal model state
- Signal connections (test them for real)

## Fixtures and Factories

**Test Data:**
- Mock data embedded in test methods
- No external fixture files
- Use `subTest` for parameterized assertions:
  ```python
  for ext in image_extensions:
      with self.subTest(ext=ext):
          file = BucketObject(name=f"image{ext}", ...)
          self.assertEqual(file.get_icon_type(), "image")
  ```

**Mock Data Pattern:**
```python
mock_objects = [
    BucketObject(
        name='file1.txt',
        size=1024,
        last_modified=datetime.now(),
        storage_class='STANDARD'
    ),
]
```

## Test Types

**Unit Tests:**
- Test single class in isolation
- Mock all dependencies
- Fast execution
- Files: `test_s3_errors.py`, `test_file_icons.py`, `test_config.py`

**Integration Tests:**
- Test interaction between Model and Service
- May use real mock data generation
- Files: `test_data_loading.py`

**Presenter Tests (Hybrid):**
- Test Presenter with mocked Model and View
- Verify signal connections and callbacks
- Test file: `test_bucket_browser_presenter.py` (542 lines)

**E2E Tests:**
- Not implemented

## Common Testing Patterns

**Async Testing (Qt Signals):**
```python
# Connect to signal and collect results
error_signal_received = []
self.model.signals.error_occurred.connect(
    lambda msg: error_signal_received.append(msg)
)

# Trigger action
self.model.delete_file('file.txt')

# Assert signal was emitted
self.assertEqual(len(error_signal_received), 1)
```

**Error Testing:**
```python
def test_delete_file_access_denied(self):
    """Model should emit error signal on access denied."""
    # Arrange
    error_signal_received = []
    self.model.signals.error_occurred.connect(
        lambda msg: error_signal_received.append(msg)
    )
    self.mock_s3_service.delete_object.side_effect = S3AccessDeniedError('test-bucket')

    # Act
    self.model.delete_file('file.txt')

    # Assert
    self.assertEqual(len(error_signal_received), 1)
    self.assertIn('Access denied', error_signal_received[0])
```

**Exception Testing:**
```python
def test_delete_file_without_s3_service(self):
    """Model should raise error when S3 service not configured."""
    model_no_service = BucketBrowserModel()

    with self.assertRaises(RuntimeError) as context:
        model_no_service.delete_file('file.txt')

    self.assertIn('S3 service not configured', str(context.exception))
```

**Navigation State Testing:**
```python
def test_navigate_to_folder_changes_prefix(self):
    """Test that navigate_to_folder updates the current prefix."""
    # Arrange
    self.mock_s3_service.list_objects.reset_mock()
    
    # Act
    self.presenter.navigate_to_folder("my-folder")
    
    # Assert
    self.assertEqual(self.presenter._current_prefix, "my-folder/")
    self.mock_s3_service.list_objects.assert_called_once()
```

**Class Organization by Feature:**
```python
class TestBucketBrowserPresenter(unittest.TestCase):
    """Test cases for BucketBrowserPresenter."""
    # Core functionality tests

class TestBucketBrowserPresenterNavigation(unittest.TestCase):
    """Test cases for navigation functionality."""
    # Navigation-specific tests

class TestBucketBrowserPresenterFallback(unittest.TestCase):
    """Test cases for presenter fallback."""
    # Fallback behavior tests
```

## Testing Utilities

**MockView (`src/tests/mock_view.py`):**
- `get_displayed_data()` - Returns data passed to view
- `get_error_message()` - Returns last error shown
- `was_loading_shown()` - Check if loading state was set
- `can_go_up()` - Check navigation button state
- `set_save_file_dialog_result(path)` - Mock dialog return value
- `messages` - List of all messages shown
- `errors` - List of all errors shown

**Running Tests:**
```bash
# From project root
uv run python -m unittest discover src/tests/

# With verbose output
uv run python -m unittest discover src/tests/ -v
```

---

*Testing analysis: 2026-04-04*
