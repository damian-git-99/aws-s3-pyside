## 1. Remove toolbar buttons

- [x] 1.1 Remove `_preview_btn` and `enable_preview_button` method from BucketBrowserView
- [x] 1.2 Remove `_generate_link_btn` and `enable_generate_link_button` method from BucketBrowserView
- [x] 1.3 Remove Delete button from `_setup_toolbar`
- [x] 1.4 Remove Download button from `_setup_toolbar`
- [x] 1.5 Remove Preview button from `_setup_toolbar`
- [x] 1.6 Remove Generate Link button from `_setup_toolbar`

## 2. Add context menu to table

- [x] 2.1 Set `QTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)` in `_setup_table`
- [x] 2.2 Connect `customContextMenuRequested` signal to new `_on_context_menu` slot
- [x] 2.3 Implement `_on_context_menu(pos)` method to build and show menu
- [x] 2.4 Add Preview action to menu (conditional on image file)
- [x] 2.5 Add Download action to menu (hidden for folders)
- [x] 2.6 Add Generate Link action to menu (hidden for folders)
- [x] 2.7 Add separator and Delete action to menu (hidden for folders)
- [x] 2.8 Connect menu actions to existing handlers (`_on_preview_clicked`, `_on_download_clicked`, `_on_generate_link_clicked`, `_on_delete_selected_clicked`)

## 3. Add visual hint on selection

- [x] 3.1 Update `_on_selection_changed` to show "Right-click for more actions" in status bar
- [x] 3.2 Clear hint when selection is cleared (no files selected)