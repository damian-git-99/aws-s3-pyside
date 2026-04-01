## Context

The bucket browser displays files and folders from S3 in a table. When navigating into folders with many objects, users must scroll through the entire list to find specific files. There is currently no search or filter functionality.

The solution should filter locally (in memory) using data already loaded from S3, not make additional API calls.

## Goals / Non-Goals

**Goals:**
- Add search input in toolbar for filtering objects by name
- Implement debounce (300ms) to avoid excessive filtering while typing
- Filter applies to currently loaded objects in memory
- Clear search restores all objects in current folder
- Case-insensitive partial matching

**Non-Goals:**
- Server-side search (S3 prefix filtering)
- Search across multiple pages (only searches loaded data)
- Regex or advanced search patterns
- Search history or favorites

## Decisions

### 1. Filter Implementation: In-memory filtering in presenter

**Chosen approach**: Filter in the presenter by updating `_all_objects` reference before calling `display_data()`

**Alternative considered**: QSortFilterProxyModel - More idiomatic for Qt but adds complexity with proxy models

**Rationale**: Simpler implementation, sufficient for typical folder sizes (hundreds of objects), easier to test

### 2. Debounce Timer: QTimer in presenter

**Chosen approach**: QTimer.singleShot with 300ms delay in presenter

**Alternative considered**: QLineEdit's textChanged with direct filtering - Too responsive, can cause UI freeze with rapid typing

**Rationale**: QTimer is built into PySide6, 300ms provides good balance between responsiveness and avoiding excessive operations

### 3. Case-insensitive matching using Python's lower()

**Rationale**: Simple, effective, works well with non-ASCII filenames

## Risks / Trade-offs

- **Risk**: Large folders (1000+ files) may have slight UI lag during filtering → **Mitigation**: Debounce reduces frequent re-filtering; for very large folders, consider async filtering in future
- **Risk**: Search only works on currently loaded page (pagination) → **Mitigation**: Document this limitation; user can load more pages before searching
- **Risk**: Empty search shows all files, potentially losing previous filter context → **Mitigation**: By design - empty search resets to show all objects