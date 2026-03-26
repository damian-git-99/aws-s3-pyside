## Context

The current implementation in `bucket_browser_view.py` has issues when displaying an empty bucket:

1. **Layout instability**: When the table is hidden with `setVisible(False)`, it still occupies space in the layout, causing the empty state to appear below where the table should be.

2. **Toolbar buttons shift**: The QToolBar doesn't maintain stable positioning when the table visibility changes.

3. **Poor empty state styling**: The current `_show_empty_state` method creates a basic QLabel with inline styles that look unprofessional.

**Current layout structure:**
```
QVBoxLayout
├── MenuBar
├── Header Container (breadcrumb + toolbar)
├── QTableWidget (hidden when empty but still in layout)
├── Empty State Label (added to layout but not properly contained)
└── Status Label
```

## Goals / Non-Goals

**Goals:**
- Create a stable content area widget that contains either the table OR the empty state
- Keep toolbar buttons fixed in position regardless of content state
- Design a visually appealing empty state with proper centering and styling
- Ensure smooth transitions between empty and populated states

**Non-Goals:**
- Add new functionality (upload, download, etc.) - just fixing UI
- Change any backend behavior
- Add animations or complex transitions

## Decisions

### 1. Content Container Widget
**Decision**: Create a dedicated `QWidget` container that holds both the table and empty state.

**Rationale**: Using a container allows us to use a stacked layout where only one child is visible at a time, eliminating layout shifts.

**Alternative considered**: Using `QLayout::removeWidget()` to remove the table from layout when empty - this works but is more complex to manage.

### 2. Empty State Styling
**Decision**: Use a modern, clean design with:
- Folder icon (📁) 
- Two-line message: title + description
- Soft gray background
- Proper centering using `setAlignment(Qt.AlignCenter)`

**Alternative considered**: Keeping inline styles - rejected because they are hard to maintain and don't look professional.

### 3. Toolbar Layout
**Decision**: Keep toolbar in its own container (already done) but ensure it uses proper spacing/stretch to prevent button shifting.

**Rationale**: The header container already exists, but we need to ensure proper sizing policy.

## Risks / Trade-offs

- **Risk**: Breaking existing table behavior
  - **Mitigation**: Keep all existing table functionality; only change visibility handling

- **Risk**: Empty state not matching app theme
  - **Mitigation**: Use neutral colors that work with both light themes

## Open Questions

None - the approach is straightforward.