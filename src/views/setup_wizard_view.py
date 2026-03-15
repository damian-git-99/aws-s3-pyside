"""Setup wizard view for first-time configuration."""

from typing import Callable, Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QWidget,
    QFormLayout, QFrame
)


class SetupWizardDialog(QDialog):
    """Setup wizard dialog for first-time configuration.
    
    This dialog is shown on first launch when no configuration exists.
    It prompts the user for required AWS environment variables.
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the setup wizard dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._on_finish_callback: Optional[Callable[[dict], None]] = None
        self._on_cancel_callback: Optional[Callable[[], None]] = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Welcome - Initial Configuration")
        self.setMinimumSize(500, 400)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("Welcome to Bucket Browser")
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Please configure your AWS credentials to get started. "
            "These settings will be saved locally and can be changed later."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #ccc;")
        layout.addWidget(separator)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # AWS Access Key ID
        self.access_key_input = QLineEdit()
        self.access_key_input.setPlaceholderText("AKIA...")
        form_layout.addRow("AWS Access Key ID *:", self.access_key_input)
        
        # AWS Secret Access Key
        self.secret_key_input = QLineEdit()
        self.secret_key_input.setPlaceholderText("Your secret access key")
        self.secret_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("AWS Secret Access Key *:", self.secret_key_input)
        
        # AWS Region
        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText("us-east-1")
        form_layout.addRow("AWS Region *:", self.region_input)
        
        # S3 Bucket Name
        self.bucket_input = QLineEdit()
        self.bucket_input.setPlaceholderText("my-bucket-name")
        form_layout.addRow("S3 Bucket Name *:", self.bucket_input)
        
        layout.addLayout(form_layout)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(required_note)
        
        # Spacer
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)
        
        self.finish_button = QPushButton("Finish")
        self.finish_button.setDefault(True)
        self.finish_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.finish_button.clicked.connect(self._on_finish)
        button_layout.addWidget(self.finish_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def set_on_finish_callback(self, callback: Callable[[dict], None]):
        """Set the callback for when user clicks Finish.
        
        Args:
            callback: Function to call with settings dict when finished
        """
        self._on_finish_callback = callback
    
    def set_on_cancel_callback(self, callback: Callable[[], None]):
        """Set the callback for when user clicks Cancel.
        
        Args:
            callback: Function to call when cancelled
        """
        self._on_cancel_callback = callback
    
    def _on_finish(self):
        """Handle Finish button click."""
        # Validate inputs
        settings = self._get_settings()
        missing = self._validate_required_fields(settings)
        
        if missing:
            QMessageBox.warning(
                self,
                "Validation Error",
                f"Please fill in all required fields:\n• {'\n• '.join(missing)}"
            )
            return
        
        # Call callback if set
        if self._on_finish_callback:
            self._on_finish_callback(settings)
        
        self.accept()
    
    def _on_cancel(self):
        """Handle Cancel button click."""
        # Confirm cancellation
        reply = QMessageBox.question(
            self,
            "Cancel Setup",
            "Are you sure you want to cancel? The application will close.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self._on_cancel_callback:
                self._on_cancel_callback()
            self.reject()
    
    def _get_settings(self) -> dict:
        """Get current settings from input fields.
        
        Returns:
            Dictionary of settings
        """
        return {
            'AWS_ACCESS_KEY_ID': self.access_key_input.text().strip(),
            'AWS_SECRET_ACCESS_KEY': self.secret_key_input.text().strip(),
            'AWS_DEFAULT_REGION': self.region_input.text().strip(),
            'AWS_S3_BUCKET_NAME': self.bucket_input.text().strip()
        }
    
    def _validate_required_fields(self, settings: dict) -> list[str]:
        """Validate that all required fields are filled.
        
        Args:
            settings: Dictionary of settings
            
        Returns:
            List of missing field names
        """
        missing = []
        field_names = {
            'AWS_ACCESS_KEY_ID': 'AWS Access Key ID',
            'AWS_SECRET_ACCESS_KEY': 'AWS Secret Access Key',
            'AWS_DEFAULT_REGION': 'AWS Region',
            'AWS_S3_BUCKET_NAME': 'S3 Bucket Name'
        }
        
        for key, value in settings.items():
            if not value:
                missing.append(field_names.get(key, key))
        
        return missing
