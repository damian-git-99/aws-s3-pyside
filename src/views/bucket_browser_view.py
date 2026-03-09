from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QToolBar, QPushButton, QLabel, QMenuBar, QMenu, QMainWindow
)
from PySide6.QtCore import Qt

from src.mvp.base_view import BaseView
from src.models.bucket_object import BucketObject
from src.utils.file_icons import FileIconManager


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
        
        # Toolbar
        self._setup_toolbar()
        if self._toolbar:
            layout.addWidget(self._toolbar)
        
        # Table
        self._setup_table()
        if self._table:
            layout.addWidget(self._table)
        
        # Status bar
        self._status_label = QLabel("Ready")
        layout.addWidget(self._status_label)
        
        self.setLayout(layout)
    
    def _setup_toolbar(self) -> None:
        """Setup the toolbar with action buttons."""
        self._toolbar = QToolBar()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self._on_refresh_clicked)
        self._toolbar.addWidget(refresh_btn)
        
        # Spacer
        spacer = QWidget()
        spacer.setFixedWidth(10)
        self._toolbar.addWidget(spacer)
        
        # Upload button (placeholder)
        upload_btn = QPushButton("Upload")
        upload_btn.setObjectName("upload_btn")
        upload_btn.clicked.connect(self._on_upload_clicked)
        self._toolbar.addWidget(upload_btn)
    
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
        self._table.setHorizontalHeaderLabels([
            "Name", "Size", "Last Modified", "Storage Class"
        ])
        
        # Configure header
        header = self._table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Enable sorting
        self._table.setSortingEnabled(True)
        
        # Selection mode
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Hide vertical header (row numbers)
        self._table.verticalHeader().setVisible(False)
    
    def display_data(self, data: List[BucketObject]) -> None:
        """Display bucket objects in the table.
        
        Args:
            data: List of BucketObject instances to display
        """
        self._table.setRowCount(len(data))
        
        for row, obj in enumerate(data):
            # Name column with icon
            name_item = QTableWidgetItem()
            name_item.setText(obj.name)
            icon = FileIconManager.get_icon_for_object(obj)
            name_item.setIcon(icon)
            
            # Set sorting data - folders first, then alphabetical
            sort_key = f"{'0' if obj.is_folder else '1'}{obj.name.lower()}"
            name_item.setData(Qt.UserRole, sort_key)
            self._table.setItem(row, 0, name_item)
            
            # Size column
            size_item = QTableWidgetItem()
            size_item.setText(obj.get_formatted_size())
            size_item.setData(Qt.UserRole, obj.size)
            self._table.setItem(row, 1, size_item)
            
            # Last Modified column
            modified_item = QTableWidgetItem()
            modified_item.setText(obj.last_modified.strftime("%Y-%m-%d %H:%M"))
            modified_item.setData(Qt.UserRole, obj.last_modified)
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
