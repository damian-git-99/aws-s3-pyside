## 1. View Implementation

- [x] 1.1 Add QLineEdit search field in toolbar setup (_setup_toolbar method)
- [x] 1.2 Configure search field placeholder text and styling
- [x] 1.3 Add textChanged signal connection to presenter callback
- [x] 1.4 Set fixed width for search field (e.g., 200px)

## 2. Presenter Implementation

- [x] 2.1 Add search_query instance variable to store current filter
- [x] 2.2 Add _search_timer (QTimer) for debounce in __init__
- [x] 2.3 Create on_search_text_changed method with debounce logic
- [x] 2.4 Implement _apply_search_filter method that filters _all_objects
- [x] 2.5 Connect view's search textChanged to presenter's handler
- [x] 2.6 Update display_data call to pass filtered list

## 3. Integration and Testing

- [x] 3.1 Test filtering with partial name matches
- [x] 3.2 Test case-insensitive search
- [x] 3.3 Test that clearing search shows all objects
- [x] 3.4 Test debounce behavior (300ms delay)
- [x] 3.5 Test that pagination still works with search active