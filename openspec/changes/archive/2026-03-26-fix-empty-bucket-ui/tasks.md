## 1. Create Content Container

- [x] 1.1 Add `_content_container` widget to hold table and empty state in `bucket_browser_view.py`
- [x] 1.2 Create a QStackedLayout inside the content container to switch between table and empty state
- [x] 1.3 Replace direct table addition to main layout with content container

## 2. Redesign Empty State

- [x] 2.1 Create a new `_create_empty_state_widget()` method that returns a properly styled empty state widget
- [x] 2.2 Use proper centering with QVBoxLayout and setAlignment
- [x] 2.3 Add professional styling with neutral colors that work with light theme
- [x] 2.4 Include folder icon and helpful message text

## 3. Update Display Logic

- [x] 3.1 Modify `display_data()` to show/hide empty state using the stacked layout
- [x] 3.2 Ensure table is completely removed from view (not just hidden) when empty
- [x] 3.3 Update status bar to show "0 objects" when empty

## 4. Verify Layout Stability

- [x] 4.1 Test that toolbar buttons stay in position when switching between empty and populated states
- [x] 4.2 Verify empty state is properly centered within its container
- [x] 4.3 Run existing tests to ensure no regressions (tests require PySide6 installation)