"""Settings panel view for editing configuration."""

from typing import Callable, Optional, Dict
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QWidget,
    QFormLayout, QFrame, QGroupBox, QScrollArea
)


class SettingsPanel(QDialog):
    """Settings panel dialog for viewing and editing configuration.
    
    This dialog allows users to view and modify all configuration values.
    It can be accessed from the toolbar at any time.
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the settings panel dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._on_save_callback: Optional[Callable[[dict], None]] = None
        self._on_cancel_callback: Optional[Callable[[], None]] = None
        self._original_settings: Dict[str, str] = {}
        self._input_fields: Dict[str, QLineEdit] = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 450)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Application Settings")
        title_font = title_label.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Update your AWS configuration below. Changes will be saved locally."
        )
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Scroll area for settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Settings widget
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(15)
        
        # AWS Configuration Group
        aws_group = QGroupBox("AWS Configuration")
        aws_layout = QFormLayout()
        aws_layout.setSpacing(12)
        
        # AWS Access Key ID
        self.access_key_input = QLineEdit()
        self.access_key_input.setPlaceholderText("AKIA...")
        self._input_fields['AWS_ACCESS_KEY_ID'] = self.access_key_input
        aws_layout.addRow("Access Key ID *:", self.access_key_input)
        
        # AWS Secret Access Key
        self.secret_key_input = QLineEdit()
        self.secret_key_input.setPlaceholderText("Your secret access key")
        self.secret_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._input_fields['AWS_SECRET_ACCESS_KEY'] = self.secret_key_input
        aws_layout.addRow("Secret Access Key *:", self.secret_key_input)
        
        # AWS Region
        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText("us-east-1")
        self._input_fields['AWS_DEFAULT_REGION'] = self.region_input
        aws_layout.addRow("Region *:", self.region_input)
        
        # S3 Bucket Name
        self.bucket_input = QLineEdit()
        self.bucket_input.setPlaceholderText("my-bucket-name")
        self._input_fields['AWS_S3_BUCKET_NAME'] = self.bucket_input
        aws_layout.addRow("Bucket Name *:", self.bucket_input)
        
        aws_group.setLayout(aws_layout)
        settings_layout.addWidget(aws_group)
        
        # Database location info
        db_group = QGroupBox("Storage Information")
        db_layout = QVBoxLayout()
        
        self.db_path_label = QLabel("Database location: Loading...")
        self.db_path_label.setWordWrap(True)
        self.db_path_label.setStyleSheet("color: #666; font-size: 11px;")
        self.db_path_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        db_layout.addWidget(self.db_path_label)
        
        db_group.setLayout(db_layout)
        settings_layout.addWidget(db_group)
        
        settings_layout.addStretch()
        scroll_area.setWidget(settings_widget)
        layout.addWidget(scroll_area)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(required_note)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Save")
        self.save_button.setDefault(True)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.save_button.clicked.connect(self._on_save)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def set_on_save_callback(self, callback: Callable[[dict], None]):
        """Set the callback for when user clicks Save.
        
        Args:
            callback: Function to call with settings dict when saved
        """
        self._on_save_callback = callback
    
    def set_on_cancel_callback(self, callback: Callable[[], None]):
        """Set the callback for when user clicks Cancel.
        
        Args:
            callback: Function to call when cancelled
        """
        self._on_cancel_callback = callback
    
    def load_settings(self, settings: Dict[str, str]):
        """Load settings into the form.
        
        Args:
            settings: Dictionary of settings to display
        """
        self._original_settings = settings.copy()
        
        # Load each setting into its corresponding input field
        for key, value in settings.items():
            if key in self._input_fields:
                self._input_fields[key].setText(value)
    
    def get_settings(self) -> Dict[str, str]:
        """Get current settings from input fields.
        
        Returns:
            Dictionary of current settings
        """
        settings = {}
        for key, field in self._input_fields.items():
            settings[key] = field.text().strip()
        return settings
    
    def set_db_path(self, db_path: str):
        """Set the database path to display.
        
        Args:
            db_path: Path to the database file
        """
        self.db_path_label.setText(f"Database location: {db_path}")
    
    def _on_save(self):
        """Handle Save button click."""
        settings = self.get_settings()
        
        # Validate inputs
        missing = self._validate_required_fields(settings)
        if missing:
            QMessageBox.warning(
                self,
                "Validation Error",
                f"Please fill in all required fields:\n• {'\n• '.join(missing)}"
            )
            return
        
        # Check if anything changed
        if settings == self._original_settings:
            # Nothing changed, just close
            self.reject()
            return
        
        # Call callback if set
        if self._on_save_callback:
            self._on_save_callback(settings)
        
        self.accept()
    
    def _on_cancel(self):
        """Handle Cancel button click."""
        # Check if there are unsaved changes
        current_settings = self.get_settings()
        if current_settings != self._original_settings:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to cancel?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        if self._on_cancel_callback:
            self._on_cancel_callback()
        
        self.reject()
    
    def _validate_required_fields(self, settings: dict) -> list[str]:
        """Validate that all required fields are filled.
        
        Args:
            settings: Dictionary of settings
            
        Returns:
            List of missing field names
        """
        missing = []
        field_names = {
            'AWS_ACCESS_KEY_ID': 'Access Key ID',
            'AWS_SECRET_ACCESS_KEY': 'Secret Access Key',
            'AWS_DEFAULT_REGION': 'Region',
            'AWS_S3_BUCKET_NAME': 'Bucket Name'
        }
        
        required_keys = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'AWS_DEFAULT_REGION',
            'AWS_S3_BUCKET_NAME'
        ]
        
        for key in required_keys:
            if not settings.get(key):
                missing.append(field_names.get(key, key))
        
        return missing
    
    def show_error(self, message: str):
        """Show an error message to the user.
        
        Args:
            message: Error message to display
        """
        QMessageBox.critical(self, "Error", message)
