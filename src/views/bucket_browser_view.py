from typing import Optional, List, Tuple
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QToolBar,
    QPushButton,
    QLabel,
    QMenuBar,
    QMenu,
    QMainWindow,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction,
    QDragEnterEvent,
    QDropEvent,
    QDragMoveEvent,
    QDragLeaveEvent,
)

from src.mvp.base_view import BaseView
from src.models.bucket_object import BucketObject
from src.utils.file_icons import FileIconManager
from src.views.image_preview_dialog import ImagePreviewDialog


class BucketBrowserView(BaseView):
    """View for the bucket browser main window.

    Displays a table with bucket objects (files and folders).
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._table: Optional[QTableWidget] = None
        self._toolbar: Optional[QToolBar] = None
        self._status_label: Optional[QLabel] = None
        self._menu_bar: Optional[QMenuBar] = None
        self._home_btn: Optional[QPushButton] = None
        self._up_btn: Optional[QPushButton] = None
        self._settings_btn: Optional[QPushButton] = None
        self._breadcrumb_widget: Optional[QWidget] = None
        self._breadcrumb_actions: List[QAction] = []
        self._header_container: Optional[QWidget] = None
        self._breadcrumb_container: Optional[QWidget] = None
        self._content_container: Optional[QWidget] = None
        self._stacked_layout: Optional[QStackedLayout] = None
        self._on_settings_callback: Optional[callable] = None
        self._preview_btn: Optional[QPushButton] = None
        self._search_input: Optional[QLineEdit] = None
        self._on_search_callback: Optional[callable] = None

        # Enable drag and drop EARLY
        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup the UI components."""
        self.setWindowTitle("Bucket Browser")
        self.resize(800, 600)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Menu Bar
        self._setup_menu_bar()
        if self._menu_bar:
            layout.setMenuBar(self._menu_bar)

        # Header container with breadcrumb and toolbar
        self._setup_header_container()
        if self._header_container:
            layout.addWidget(self._header_container)

        # Content container with stacked layout (table + empty state)
        self._setup_content_container()
        if self._content_container:
            layout.addWidget(self._content_container)

        # Status bar
        self._status_label = QLabel("Ready")
        layout.addWidget(self._status_label)

        self.setLayout(layout)

    def set_drop_highlight(self) -> None:
        """Show visual highlight indicating valid drop zone."""
        self.setStyleSheet("QWidget { border: 3px solid #3498db; }")

    def clear_drop_highlight(self) -> None:
        """Clear visual highlight when drag exits."""
        self.setStyleSheet("")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Handle drag enter event.

        Args:
            event: The drag enter event
        """
        event.acceptProposedAction()
        self.set_drop_highlight()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        """Handle drag move event.

        Args:
            event: The drag move event
        """
        if self._presenter:
            is_valid = self._presenter.on_drag_move(event)
            if is_valid:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        """Handle drag leave event.

        Args:
            event: The drag leave event
        """
        self.clear_drop_highlight()
        if self._presenter:
            self._presenter.on_drag_leave()
        event.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle drop event.

        Args:
            event: The drop event
        """
        self.clear_drop_highlight()
        if self._presenter:
            self._presenter.on_files_dropped(event)
        event.accept()

    def _setup_toolbar(self) -> None:
        """Setup the toolbar with action buttons."""
        self._toolbar = QToolBar()

        # Home button
        self._home_btn = QPushButton("Home")
        self._home_btn.setObjectName("home_btn")
        self._home_btn.clicked.connect(self._on_home_clicked)
        self._toolbar.addWidget(self._home_btn)

        # Up button
        self._up_btn = QPushButton("Up")
        self._up_btn.setObjectName("up_btn")
        self._up_btn.clicked.connect(self._on_up_clicked)
        self._toolbar.addWidget(self._up_btn)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self._on_refresh_clicked)
        self._toolbar.addWidget(refresh_btn)

        # Spacer
        spacer = QWidget()
        spacer.setFixedWidth(10)
        self._toolbar.addWidget(spacer)

        # Create Folder button
        create_folder_btn = QPushButton("Create Folder")
        create_folder_btn.setObjectName("create_folder_btn")
        create_folder_btn.clicked.connect(self._on_create_folder_clicked)
        self._toolbar.addWidget(create_folder_btn)

        # Upload button (placeholder)
        upload_btn = QPushButton("Upload")
        upload_btn.setObjectName("upload_btn")
        upload_btn.clicked.connect(self._on_upload_clicked)
        self._toolbar.addWidget(upload_btn)

        # Delete button - deletes selected file
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("delete_btn")
        delete_btn.setFixedSize(80, 28)
        delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        delete_btn.clicked.connect(self._on_delete_selected_clicked)
        self._toolbar.addWidget(delete_btn)

        # Download button - downloads selected file
        download_btn = QPushButton("Download")
        download_btn.setObjectName("download_btn")
        download_btn.setFixedSize(100, 28)
        download_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        download_btn.clicked.connect(self._on_download_clicked)
        self._toolbar.addWidget(download_btn)

        # Preview button - shows preview for selected image file
        self._preview_btn = QPushButton("Preview")
        self._preview_btn.setObjectName("preview_btn")
        self._preview_btn.setFixedSize(80, 28)
        self._preview_btn.setEnabled(False)  # Disabled by default
        self._preview_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """
        )
        self._preview_btn.clicked.connect(self._on_preview_clicked)
        self._toolbar.addWidget(self._preview_btn)

        # Settings button
        self._settings_btn = QPushButton("Settings")
        self._settings_btn.setObjectName("settings_btn")
        self._settings_btn.clicked.connect(self._on_settings_clicked)
        self._toolbar.addWidget(self._settings_btn)

        # Spacer before search
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._toolbar.addWidget(spacer)

        # Search input field
        self._search_input = QLineEdit()
        self._search_input.setObjectName("search_input")
        self._search_input.setPlaceholderText("Search files...")
        self._search_input.setFixedWidth(200)
        self._search_input.setStyleSheet(
            """
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """
        )
        self._search_input.textChanged.connect(self._on_search_text_changed)
        self._toolbar.addWidget(self._search_input)

        # Disable navigation buttons initially (at root)
        self.enable_navigation_buttons(can_go_up=False)

    def _setup_header_container(self) -> None:
        """Setup the header container with breadcrumb and toolbar in separate rows."""
        self._header_container = QWidget()
        self._header_container.setObjectName("header_container")
        header_layout = QVBoxLayout(self._header_container)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(8, 8, 8, 8)

        # Breadcrumb row
        self._breadcrumb_container = QWidget()
        self._breadcrumb_container.setObjectName("breadcrumb_container")
        breadcrumb_row_layout = QHBoxLayout(self._breadcrumb_container)
        breadcrumb_row_layout.setContentsMargins(0, 0, 0, 0)
        breadcrumb_row_layout.setSpacing(4)

        # Breadcrumb widget
        self._breadcrumb_widget = QWidget()
        self._breadcrumb_widget.setObjectName("breadcrumb_widget")
        self._breadcrumb_layout = QHBoxLayout(self._breadcrumb_widget)
        self._breadcrumb_layout.setContentsMargins(5, 0, 5, 0)
        self._breadcrumb_layout.addStretch()
        breadcrumb_row_layout.addWidget(self._breadcrumb_widget)
        breadcrumb_row_layout.addStretch()

        header_layout.addWidget(self._breadcrumb_container)

        # Toolbar row
        self._setup_toolbar()
        if self._toolbar:
            header_layout.addWidget(self._toolbar)

    def _setup_content_container(self) -> None:
        """Setup the content container with stacked layout for table and empty state."""
        # First setup the table
        self._setup_table()

        # Create content container
        self._content_container = QWidget()
        self._content_container.setObjectName("content_container")

        # Enable drag and drop on content container
        self._content_container.setAcceptDrops(True)

        # Create stacked layout
        self._stacked_layout = QStackedLayout(self._content_container)
        self._stacked_layout.setContentsMargins(0, 0, 0, 0)

        # Create empty state widget
        empty_state_widget = self._create_empty_state_widget()

        # Add widgets to stacked layout: index 0 = table, index 1 = empty state
        self._stacked_layout.addWidget(self._table)
        self._stacked_layout.addWidget(empty_state_widget)

        # Set initial state: show table (index 0)
        self._stacked_layout.setCurrentIndex(0)

    def _create_empty_state_widget(self) -> QWidget:
        """Create a properly styled empty state widget."""
        widget = QWidget()
        widget.setObjectName("empty_state_widget")

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel("📁")
        icon_label.setObjectName("empty_state_icon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 64px;")

        title_label = QLabel("No files in this folder")
        title_label.setObjectName("empty_state_title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333333;")

        description_label = QLabel("Upload files or create folders to see them here")
        description_label.setObjectName("empty_state_description")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: #666666; font-size: 13px;")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)

        return widget

    def _setup_menu_bar(self) -> None:
        """Setup the menu bar."""
        self._menu_bar = QMenuBar()

        # File menu
        file_menu = self._menu_bar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        # View menu
        view_menu = self._menu_bar.addMenu("View")
        view_menu.addAction("Refresh", self._on_refresh_clicked)

        # Help menu
        help_menu = self._menu_bar.addMenu("Help")
        help_menu.addAction("About")

    def _setup_table(self) -> None:
        """Setup the table widget."""
        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(
            ["Name", "Size", "Last Modified", "Storage Class"]
        )

        # Configure header
        header = self._table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # Disable sorting - folders-first order comes from service
        self._table.setSortingEnabled(False)

        # Selection mode
        self._table.setSelectionBehavior(QTableWidget.SelectRows)

        # Hide vertical header (row numbers)
        self._table.verticalHeader().setVisible(False)

        # Connect double-click signal
        self._table.cellDoubleClicked.connect(self._on_table_double_clicked)

        # Connect selection change signal for preview button
        self._table.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self) -> None:
        """Handle table selection change to update preview button state."""
        is_image = self._is_image_selected()
        self.enable_preview_button(is_image)

    def _is_image_selected(self) -> bool:
        """Check if currently selected item is an image file.

        Returns:
            True if selected item is an image, False otherwise
        """
        selected_rows = self._table.selectionModel().selectedRows()
        if not selected_rows:
            return False

        row = selected_rows[0].row()
        name_item = self._table.item(row, 0)
        if not name_item:
            return False

        filename = name_item.text()

        # Check if it's an image by looking at the current data
        for obj in getattr(self, "_current_data", []):
            if obj.name == filename:
                return obj.get_icon_type() == "image"

        return False

    def enable_preview_button(self, enabled: bool) -> None:
        """Enable or disable the preview button.

        Args:
            enabled: True to enable button, False to disable
        """
        if self._preview_btn:
            self._preview_btn.setEnabled(enabled)

    def _on_preview_clicked(self) -> None:
        """Handle preview button click."""
        if not self._presenter:
            return

        selected_rows = self._table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        name_item = self._table.item(row, 0)
        if not name_item:
            return

        filename = name_item.text()
        self._presenter.handle_preview_request(filename)

    def show_image_preview(self, image_data: bytes, filename: str) -> None:
        """Show image preview dialog.

        Args:
            image_data: Raw image bytes
            filename: Name of the image file
        """
        dialog = ImagePreviewDialog(image_data, filename, self)
        dialog.exec()

    def display_data(self, data: List[BucketObject]) -> None:
        """Display bucket objects in the table.

        Args:
            data: List of BucketObject instances to display
        """
        self._current_data = data

        # Show empty state or table based on data
        if not data:
            self._stacked_layout.setCurrentIndex(1)  # Show empty state
            self._table.setRowCount(0)
            self._update_status(0)
            return

        self._stacked_layout.setCurrentIndex(0)  # Show table
        self._table.setRowCount(len(data))

        for row, obj in enumerate(data):
            # Name column with icon
            name_item = QTableWidgetItem()
            name_item.setText(obj.name)
            icon = FileIconManager.get_icon_for_object(obj)
            name_item.setIcon(icon)
            self._table.setItem(row, 0, name_item)

            # Size column
            size_item = QTableWidgetItem()
            size_item.setText(obj.get_formatted_size())
            self._table.setItem(row, 1, size_item)

            # Last Modified column
            modified_item = QTableWidgetItem()
            modified_item.setText(obj.last_modified.strftime("%Y-%m-%d %H:%M"))
            self._table.setItem(row, 2, modified_item)

            # Storage Class column
            storage_item = QTableWidgetItem()
            storage_item.setText(obj.storage_class)
            self._table.setItem(row, 3, storage_item)

        # Update status
        self._update_status(len(data))

    def _update_status(self, count: int) -> None:
        """Update the status label with object count."""
        if self._status_label:
            self._status_label.setText(f"{count} objects")

    def _on_refresh_clicked(self) -> None:
        """Handle refresh button click."""
        if self._presenter:
            self._presenter.on_refresh_clicked()

    def _on_upload_clicked(self) -> None:
        """Handle upload button click."""
        if self._presenter:
            self._presenter.on_upload_clicked()

    def _on_delete_selected_clicked(self) -> None:
        """Handle delete button click - deletes selected file/folder."""
        if not self._presenter:
            return

        # Get selected row
        selected_rows = self._table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_error("No file selected. Please select a file to delete.")
            return

        row = selected_rows[0].row()

        # Get the filename from first column
        name_item = self._table.item(row, 0)
        if not name_item:
            return

        filename = name_item.text()

        # Check if it's a folder - don't allow deleting folders
        is_folder = False
        for obj in getattr(self, "_current_data", []):
            if obj.name == filename:
                is_folder = obj.is_folder
                break

        if is_folder:
            self.show_error("Cannot delete folders. Only files can be deleted.")
            return

        # Call presenter to handle deletion
        self._presenter.handle_delete_file(filename)

    def show_error(self, message: str) -> None:
        """Show error message in status bar."""
        if self._status_label:
            self._status_label.setText(f"Error: {message}")
            self._status_label.setStyleSheet("color: red;")

    def show_loading(self, show: bool = True) -> None:
        """Show or hide loading indicator."""
        if self._status_label:
            if show:
                self._status_label.setText("Loading...")
            else:
                self._status_label.setText("Ready")

    def show_error_with_retry(self, message: str, on_retry: callable) -> None:
        """Show error message with retry button.

        Args:
            message: Error message to display
            on_retry: Callback function when retry button is clicked
        """
        from PySide6.QtWidgets import QMessageBox, QPushButton

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Critical)

        # Add retry button
        retry_btn = msg_box.addButton("Retry", QMessageBox.ButtonRole.ActionRole)
        retry_btn.clicked.connect(on_retry)

        # Add close button
        msg_box.addButton(QMessageBox.StandardButton.Close)

        msg_box.exec()

    def show_load_more_button(self, show: bool = True) -> None:
        """Show or hide Load More button.

        Args:
            show: True to show button, False to hide
        """
        if not hasattr(self, "_load_more_btn"):
            # Create button if it doesn't exist
            self._load_more_btn = QPushButton("Load More")
            self._load_more_btn.setObjectName("load_more_btn")
            self._load_more_btn.clicked.connect(self._on_load_more_clicked)
            # Add to layout after table
            if self._table and self.layout():
                # Find position to insert (before status label)
                layout = self.layout()
                index = layout.indexOf(self._status_label)
                layout.insertWidget(index, self._load_more_btn)

        if hasattr(self, "_load_more_btn"):
            self._load_more_btn.setVisible(show)

    def _on_load_more_clicked(self) -> None:
        """Handle Load More button click."""
        if self._presenter:
            self._presenter.load_more()

    def _show_empty_state(self, show: bool = True) -> None:
        """Show or hide the empty state message.

        Args:
            show: True to show empty state, False to hide
        """
        if not hasattr(self, "_empty_state_label"):
            # Create empty state label if it doesn't exist
            from PySide6.QtWidgets import QLabel
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QFont

            self._empty_state_label = QLabel(
                "📁 No files uploaded yet\n\nThis bucket is empty. Upload files to see them here."
            )
            self._empty_state_label.setObjectName("empty_state_label")
            self._empty_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._empty_state_label.setWordWrap(True)

            # Style the empty state
            font = QFont()
            font.setPointSize(12)
            self._empty_state_label.setFont(font)
            self._empty_state_label.setStyleSheet(
                """
                QLabel#empty_state_label {
                    color: #666666;
                    padding: 40px;
                    background-color: #f5f5f5;
                    border: 2px dashed #cccccc;
                    border-radius: 8px;
                    margin: 20px;
                }
            """
            )

            # Add to layout (hide table when showing empty state)
            if self.layout():
                self.layout().addWidget(self._empty_state_label)

        if hasattr(self, "_empty_state_label"):
            self._empty_state_label.setVisible(show)
            self._table.setVisible(not show)

    def _on_table_double_clicked(self, row: int, col: int) -> None:
        """Handle double-click on table cell.

        Args:
            row: Row that was clicked
            col: Column that was clicked
        """
        if not self._presenter or not self._table:
            return

        name_item = self._table.item(row, 0)
        if not name_item:
            return

        object_name = name_item.text()

        is_folder = False
        for obj in getattr(self, "_current_data", []):
            if obj.name == object_name:
                is_folder = obj.is_folder
                break

        self._presenter.on_item_double_clicked(object_name, is_folder)

    def _on_home_clicked(self) -> None:
        """Handle Home button click."""
        if self._presenter:
            self._presenter.navigate_to_root()

    def _on_up_clicked(self) -> None:
        """Handle Up button click."""
        if self._presenter:
            self._presenter.navigate_up()

    def _on_settings_clicked(self) -> None:
        """Handle Settings button click."""
        if self._on_settings_callback:
            self._on_settings_callback()

    def set_on_settings_callback(self, callback: callable) -> None:
        """Set callback for Settings button click.

        Args:
            callback: Function to call when Settings button is clicked
        """
        self._on_settings_callback = callback

    def _on_breadcrumb_clicked(self, prefix: Optional[str]) -> None:
        """Handle breadcrumb segment click.

        Args:
            prefix: The prefix to navigate to (None for root)
        """
        if self._presenter:
            self._presenter.navigate_to_prefix(prefix)

    def update_breadcrumb(self, path_segments: List[Tuple[str, Optional[str]]]) -> None:
        """Update the breadcrumb display.

        Args:
            path_segments: List of tuples (display_name, prefix) for each segment
        """
        if not hasattr(self, "_breadcrumb_layout"):
            return

        while self._breadcrumb_layout.count() > 1:
            item = self._breadcrumb_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._breadcrumb_actions.clear()

        for i, (name, prefix) in enumerate(path_segments):
            if i > 0:
                separator = QLabel(">")
                separator.setStyleSheet("color: #999999; padding: 0 2px;")
                self._breadcrumb_layout.insertWidget(
                    self._breadcrumb_layout.count() - 1, separator
                )

            btn = QPushButton(name)
            btn.setFlat(True)
            btn.setObjectName(f"breadcrumb_{i}")
            btn.setStyleSheet("QPushButton { padding: 2px 4px; }")

            if i < len(path_segments) - 1:
                btn.clicked.connect(
                    lambda checked, p=prefix: self._on_breadcrumb_clicked(p)
                )
                btn.setStyleSheet(
                    """
                    QPushButton {
                        color: #0066cc;
                        text-decoration: underline;
                        background: none;
                        border: none;
                        padding: 2px 4px;
                    }
                    QPushButton:hover {
                        color: #0033aa;
                    }
                """
                )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        color: #333333;
                        font-weight: bold;
                        background: none;
                        border: none;
                        padding: 2px 4px;
                    }
                """
                )

            self._breadcrumb_layout.insertWidget(
                self._breadcrumb_layout.count() - 1, btn
            )

    def enable_navigation_buttons(self, can_go_up: bool) -> None:
        """Enable or disable navigation buttons.

        Args:
            can_go_up: Whether the Up button should be enabled
        """
        if self._home_btn:
            self._home_btn.setEnabled(can_go_up)
        if self._up_btn:
            self._up_btn.setEnabled(can_go_up)

    def show_upload_dialog(self) -> Optional[str]:
        """Show file picker dialog for upload.

        Returns:
            File path selected, or None if cancelled
        """
        from PySide6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File to Upload", "", "All Files (*)"
        )

        return file_path if file_path else None

    def show_upload_progress_dialog(self, file_path: str):
        """Show progress dialog for upload.

        Args:
            file_path: Path of file being uploaded (for display)

        Returns:
            QProgressDialog instance
        """
        from PySide6.QtWidgets import QProgressDialog
        import os

        filename = os.path.basename(file_path)

        progress_dialog = QProgressDialog(
            f"Uploading {filename}...",
            None,  # No cancel button - upload is synchronous
            0,
            100,
            self,
        )
        progress_dialog.setWindowTitle("Upload Progress")
        progress_dialog.setWindowModality(Qt.WindowModality.NonModal)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        progress_dialog.show()
        progress_dialog.raise_()

        return progress_dialog

    def close_upload_progress_dialog(self, progress_dialog) -> None:
        """Close the upload progress dialog.

        Args:
            progress_dialog: The dialog to close
        """
        if progress_dialog:
            progress_dialog.close()

    def show_save_file_dialog(self, filename: str) -> Optional[str]:
        """Show save file dialog for downloading.

        Args:
            filename: Default filename to suggest

        Returns:
            File path selected, or None if cancelled
        """
        from PySide6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", filename, "All Files (*)"
        )

        return file_path if file_path else None

    def show_download_progress_dialog(self, filename: str):
        """Show progress dialog for download.

        Args:
            filename: Name of file being downloaded (for display)

        Returns:
            QProgressDialog instance
        """
        from PySide6.QtWidgets import QProgressDialog

        progress_dialog = QProgressDialog(
            f"Downloading {filename}...",
            None,
            0,
            100,
            self,
        )
        progress_dialog.setWindowTitle("Download Progress")
        progress_dialog.setWindowModality(Qt.WindowModality.NonModal)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        progress_dialog.show()
        progress_dialog.raise_()

        return progress_dialog

    def close_download_progress_dialog(self, progress_dialog) -> None:
        """Close the download progress dialog.

        Args:
            progress_dialog: The dialog to close
        """
        if progress_dialog:
            progress_dialog.close()

    def _on_download_clicked(self) -> None:
        """Handle download button click - downloads selected file."""
        if not self._presenter:
            return

        # Get selected row
        selected_rows = self._table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_error("Please select a file to download")
            return

        row = selected_rows[0].row()

        # Get the filename from first column
        name_item = self._table.item(row, 0)
        if not name_item:
            return

        filename = name_item.text()

        # Check if it's a folder - don't allow downloading folders
        is_folder = False
        for obj in getattr(self, "_current_data", []):
            if obj.name == filename:
                is_folder = obj.is_folder
                break

        if is_folder:
            self.show_error("Folders cannot be downloaded. Please select a file.")
            return

        # Call presenter to handle download
        self._presenter.handle_download_file(filename)

    def show_message(self, message: str) -> None:
        """Show a message in the status bar.

        Args:
            message: Message to display
        """
        if self._status_label:
            self._status_label.setText(message)
            self._status_label.setStyleSheet("color: green;")

    def _on_create_folder_clicked(self) -> None:
        """Handle Create Folder button click."""
        if self._presenter:
            self._presenter.on_create_folder_clicked()

    def show_create_folder_dialog(self, parent=None) -> Optional[str]:
        """Show dialog for creating a new folder.

        Args:
            parent: Parent widget for the dialog

        Returns:
            Folder name entered by user, or None if cancelled
        """
        dialog = CreateFolderDialog(parent or self)
        if dialog.exec() == QDialog.Accepted:
            return dialog.get_folder_name()
        return None

    def _on_search_text_changed(self, text: str) -> None:
        """Handle search text changes.

        Args:
            text: The current search text
        """
        if self._on_search_callback:
            self._on_search_callback(text)

    def set_on_search_callback(self, callback: callable) -> None:
        """Set callback for search text changes.

        Args:
            callback: Function to call when search text changes
        """
        self._on_search_callback = callback


class CreateFolderDialog(QDialog):
    """Dialog for creating a new folder."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Folder")
        self.setModal(True)
        self.resize(300, 100)

        layout = QVBoxLayout()

        # Label
        label = QLabel("Folder name:")
        layout.addWidget(label)

        # Input field
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Enter folder name")
        layout.addWidget(self._name_input)

        # Buttons
        button_box = QDialogButtonBox()
        create_button = button_box.addButton(
            "Create", QDialogButtonBox.ButtonRole.AcceptRole
        )
        cancel_button = button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        create_button.clicked.connect(self._on_accepted)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # Set focus to input
        self._name_input.setFocus()

    def _on_accepted(self) -> None:
        """Handle Create button click."""
        folder_name = self._name_input.text().strip()

        if not folder_name:
            QMessageBox.warning(self, "Invalid Name", "Folder name cannot be empty.")
            return

        # Check for invalid characters
        invalid_chars = '/\\:*?"<>|'
        if any(char in folder_name for char in invalid_chars):
            QMessageBox.warning(
                self,
                "Invalid Name",
                f"Folder name cannot contain any of these characters: {invalid_chars}",
            )
            return

        self.accept()

    def get_folder_name(self) -> str:
        """Return the folder name entered by user."""
        return self._name_input.text().strip()

    def _on_search_text_changed(self, text: str) -> None:
        """Handle search text changes.

        Args:
            text: The current search text
        """
        if self._on_search_callback:
            self._on_search_callback(text)

    def set_on_search_callback(self, callback: callable) -> None:
        """Set callback for search text changes.

        Args:
            callback: Function to call when search text changes
        """
        self._on_search_callback = callback
