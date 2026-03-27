## Context

The application follows an MVP (Model-View-Presenter) architecture for PySide6. File uploads are currently handled through:

- **BucketBrowserView**: Main file browser widget
- **BucketBrowserPresenter**: Handles view logic, file operations, and Qt signals
- **UploadWorker**: Background thread for S3 uploads with progress tracking
- **S3FileService**: S3 operations (upload/download/delete)

Currently, file uploads are triggered through a file picker dialog. The drag-and-drop feature extends the existing file picker area to accept dropped files directly.

## Goals / Non-Goals

**Goals:**
- Enable users to drag single files onto the file browser for upload
- Provide visual feedback (highlight, cursor changes) during drag operations
- Validate drops to accept only single files (reject folders and multiple files)
- Integrate seamlessly with existing MVP architecture (no breaking changes)
- Maintain consistent error handling and progress tracking as file picker uploads
- Log drag-and-drop events for debugging

**Non-Goals:**
- Support multiple file drag-and-drop (single file only)
- Support folder uploads
- Add drag-and-drop functionality to other views (settings, setup wizard)
- Implement custom drag cursor graphics beyond PySide6 defaults

## Decisions

**Decision 1: Extend BucketBrowserView to handle drop events**
- Rationale: The view is the natural place to handle user interactions. Following MVP, the view detects drops and delegates processing to the presenter.
- Alternative considered: Create separate DragDropHandler class (adds complexity without clear benefit given single responsibility of file browser).

**Decision 2: Reuse existing UploadWorker and S3FileService**
- Rationale: Drag-drop uploads should behave identically to file picker uploads. Code reuse ensures consistency.
- Alternative: Create separate drag-drop-specific upload logic (would duplicate logic and complicate maintenance).

**Decision 3: Validate drops in dragEnterEvent, process in dropEvent**
- Rationale: This two-phase approach prevents invalid drops at the UI level and provides immediate visual feedback.
- Implementation: dragEnterEvent checks MIME data for files, dropEvent performs upload.

**Decision 4: Single-file only drops**
- Rationale: Simplifies validation logic and aligns with current S3 service design (uploads one file at a time).
- Alternative: Support multiple files (requires batching logic, more complex state management).

**Decision 5: Visual feedback via stylesheet highlight during drag**
- Rationale: PySide6-native approach, no custom graphics needed. Simple CSS-like styling is maintainable.
- Alternative: Custom graphics/overlays (more complex, diminishing UX returns).

## Risks / Trade-offs

**[Risk] Drop validation timing** → Mitigation: Perform validation in dragEnterEvent to reject early; use dropEvent only for confirmed valid drops.

**[Risk] Large file drops** → Mitigation: Reuse existing UploadWorker progress tracking to handle long uploads; no new risk vs. file picker approach.

**[Risk] Drop outside current folder** → Mitigation: Drag-drop always uploads to current folder (like file picker). Clearly document this behavior.

**[Trade-off] Single file only** → Benefit: Simpler code. Cost: Users must drag files one at a time (acceptable for typical workflow).

## Migration Plan

1. Add drag-drop event handlers to BucketBrowserView (dragEnterEvent, dragMoveEvent, dropEvent)
2. Implement drop validation in presenter (check MIME data, file count, types)
3. Reuse existing UploadWorker for processing
4. Add visual feedback (stylesheet highlight when dragging over view)
5. Test with various file types and edge cases
6. Deploy alongside next release; no database or config changes needed

## Implementation Architecture

```
BucketBrowserView (updated)
  ├── dragEnterEvent() → check MIME data → presenter.on_drag_enter()
  ├── dragLeaveEvent() → remove highlight → presenter.on_drag_leave()
  └── dropEvent() → presenter.on_files_dropped()

BucketBrowserPresenter (updated)
  ├── on_drag_enter(event) → validate, set highlight, update cursor
  ├── on_drag_leave() → clear highlight
  └── on_files_dropped(file_paths) → reuse existing UploadWorker

Qt Signals Flow:
  Drop → presenter → UploadWorker → progress signal → view updates UI
```

No new models or services required.

## Open Questions

- Cursor change handling: Should custom drag cursor be set, or rely on OS defaults?
- Drop zone clarity: Should entire view be drop zone or a specific visual region?
