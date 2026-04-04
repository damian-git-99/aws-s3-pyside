## Context

The bucket browser view (`src/views/bucket_browser_view.py`) currently has a toolbar with:
- Navigation: Home, Up, Refresh
- Folder actions: Create Folder, Upload
- File actions: Delete, Download, Preview, Generate Link
- Settings and Search

The 5 file action buttons (Delete, Download, Preview, Generate Link) occupy significant toolbar space. The goal is to move these to a right-click context menu on the table, freeing vertical space.

## Goals / Non-Goals

**Goals:**
- Remove Delete, Download, Preview, Generate Link buttons from toolbar
- Add context menu appearing on right-click over table rows
- Provide visual hint when file is selected indicating context menu availability
- Maintain single-file selection behavior
- Preserve all existing action behaviors (confirmation dialogs, image-only preview, etc.)

**Non-Goals:**
- Multi-file selection or batch operations
- Keyboard shortcuts (may be added later)
- Context menu for folders (file actions only for now)
- Changes to S3 service or presenter logic (handlers already exist)

## Decisions

### Decision: Context menu on QTableWidget via custom signal

**Choice**: Use `QTableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)` and connect to a custom slot that builds and shows the menu.

**Rationale**: This approach:
- Integrates naturally with Qt's event system
- Allows dynamic menu building based on selected item type
- Doesn't interfere with default table behavior
- Simple to implement and test

**Alternatives considered**:
- Subclassing QTableWidget: Overkill for this change
- Event filter: More complex, harder to maintain

### Decision: Context menu items

**Menu structure**:
```
┌─────────────────────┐
│ Preview          📄 │  ← Only shown for image files
│ Download        📥 │
│ Generate Link    🔗 │
│ ─────────────────── │
│ Delete           🗑️ │
└─────────────────────┘
```

**Rationale**: 
- Preview is conditional (images only) to avoid showing disabled items
- Delete at bottom as it's the most destructive action
- Separator between file preview/download actions and delete

### Decision: Visual hint on selection

**Choice**: Update status bar to show "Right-click for more actions" when a file is selected.

**Rationale**:
- Non-intrusive - uses existing status bar
- Clear call-to-action without adding new UI elements
- Disappears naturally when selection is cleared

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Users won't discover context menu | Add status bar hint on selection |
| Right-click feels slower than toolbar button | Future: add keyboard shortcuts (out of scope) |
| Context menu on empty space or folders | Only show menu when file is selected; menu items conditional on file type |
