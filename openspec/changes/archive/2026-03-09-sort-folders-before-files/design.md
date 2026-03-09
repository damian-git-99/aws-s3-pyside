## Context

The bucket browser currently has folders-first sorting implemented in the S3 service layer (`s3_service.py:129`) and sets sort keys in the view layer (`bucket_browser_view.py:143`). However, when users click column headers to sort the table, the folders-first order can be overridden since the table has `setSortingEnabled(True)`.

Current implementation:
- Service sorts: `objects.sort(key=lambda x: (not x.is_folder, x.name.lower()))`
- View sets sort key: `sort_key = f"{'0' if obj.is_folder else '1'}{obj.name.lower()}`"

## Goals / Non-Goals

**Goals:**
- Ensure folders ALWAYS appear before files in the file listing
- Maintain folders-first order even when user sorts by any column
- Provide consistent UX across all sorting interactions

**Non-Goals:**
- Changing the S3 service sorting logic (already correct)
- Adding new sort columns or options
- Modifying the visual appearance of folders/files

## Decisions

**Decision 1: Disable interactive sorting on the Name column, use custom sort proxy**
- **Rationale**: The Name column is the primary sort column. By disabling the built-in sort and using a custom sort proxy model, we can enforce folders-first ordering regardless of user clicks.
- **Alternative considered**: Override `sortByColumn()` to intercept sort requests - rejected as more complex and prone to bugs

**Decision 2: Use QSortFilterProxyModel for consistent sorting**
- **Rationale**: A proxy model allows us to maintain sorting logic in one place and ensures consistent behavior across all columns
- **Implementation**: Custom proxy that always applies folders-first sort as primary key, then user-selected column as secondary

**Decision 3: Keep service-layer sorting as backup**
- **Rationale**: Double protection - even if UI sorting fails, data arrives pre-sorted
- **Trade-off**: Slight redundancy but ensures correctness

## Risks / Trade-offs

**Risk**: Users may expect standard table sorting behavior (folders mixed with files when sorting by size/date)
- **Mitigation**: This is a design choice favoring UX consistency. Most file browsers (Finder, Explorer) keep folders first.

**Risk**: Proxy model adds complexity
- **Mitigation**: Well-tested Qt pattern, minimal custom code needed

**Risk**: Performance impact on large lists
- **Mitigation**: Sorting 50 items (current page size) is negligible. Proxy model sorts are efficient.
