## 1. Create Custom Sort Proxy Model

- [x] 1.1 Create `FolderFirstSortProxyModel` class in `src/views/` that extends `QSortFilterProxyModel`
- [x] 1.2 Override `lessThan()` method to enforce folders-first sorting as primary key
- [x] 1.3 Add method to set secondary sort column (the user-selected column)
- [x] 1.4 Handle sort direction (ascending/descending) within each group

## 2. Update Bucket Browser View

- [x] 2.1 Replace direct table sorting with proxy model in `bucket_browser_view.py`
- [x] 2.2 Create proxy model instance and set source model to table model
- [x] 2.3 Connect column header clicks to update proxy model's secondary sort column
- [x] 2.4 Remove `setSortingEnabled(True)` and manage sorting manually via proxy
- [x] 2.5 Ensure `is_folder` data is accessible to proxy model for sorting decisions

## 3. Integration and Testing

- [x] 3.1 Update presenter to work with new sorting mechanism if needed
- [x] 3.2 Test folders-first order with default view
- [x] 3.3 Test sorting by name maintains folders-first
- [x] 3.4 Test sorting by size/date maintains folders-first
- [x] 3.5 Test reverse sorting maintains folders-first
- [x] 3.6 Run existing tests to ensure no regressions

## 4. Documentation

- [x] 4.1 Add docstrings to new proxy model class
- [x] 4.2 Update any relevant comments in view layer
