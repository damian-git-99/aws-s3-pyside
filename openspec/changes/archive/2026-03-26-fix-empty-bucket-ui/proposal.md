## Why

When a bucket folder has no files or subfolders, the UI looks broken: the toolbar buttons shift position, the empty state message looks ugly and uncentered, and the layout feels unstable. This creates a poor user experience and makes the app feel unfinished.

## What Changes

- Create a dedicated content area widget that properly manages table vs empty state visibility
- Fix toolbar button positioning so they stay stable regardless of content state
- Redesign the empty state UI with better styling, centering, and visual hierarchy
- Ensure smooth transitions between empty and populated states without layout shifts

## Capabilities

### New Capabilities

- **empty-bucket-ui**: Improved empty state display with proper layout management

### Modified Capabilities

- None - this is a pure UI/UX improvement

## Impact

- Only affects `src/views/bucket_browser_view.py` - the view layer
- No changes to model, presenter, or service layers
- No new dependencies added