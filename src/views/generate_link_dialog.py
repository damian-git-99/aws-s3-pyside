from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard


class GenerateLinkDialog(QDialog):
    """Dialog for generating pre-signed URLs."""

    def __init__(self, filename: str, parent=None):
        super().__init__(parent)
        self._filename = filename
        self._generated_url = ""
        self.setWindowTitle(f"Generate Link - {filename}")
        self.setModal(True)
        self.resize(600, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        file_label = QLabel(f"File: <b>{self._filename}</b>")
        layout.addWidget(file_label)

        expiration_layout = QHBoxLayout()
        expiration_label = QLabel("Link expires in:")
        self._expiration_combo = QComboBox()
        self._expiration_combo.addItem("1 hour", 1)
        self._expiration_combo.addItem("1 day", 24)
        self._expiration_combo.addItem("7 days", 168)
        self._expiration_combo.addItem("30 days", 720)
        expiration_layout.addWidget(expiration_label)
        expiration_layout.addWidget(self._expiration_combo)
        expiration_layout.addStretch()
        layout.addLayout(expiration_layout)

        self._generate_btn = QPushButton("Generate Link")
        self._generate_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        layout.addWidget(self._generate_btn)

        url_label = QLabel("Generated URL:")
        layout.addWidget(url_label)

        self._url_input = QLineEdit()
        self._url_input.setReadOnly(True)
        self._url_input.setPlaceholderText("Click 'Generate Link' to create URL")
        layout.addWidget(self._url_input)

        self._copy_btn = QPushButton("Copy to Clipboard")
        self._copy_btn.setEnabled(False)
        self._copy_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """
        )
        layout.addWidget(self._copy_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def get_selected_expiration_hours(self) -> int:
        """Return selected expiration in hours."""
        return self._expiration_combo.currentData()

    def set_generated_url(self, url: str):
        """Display the generated URL."""
        self._generated_url = url
        self._url_input.setText(url)
        self._copy_btn.setEnabled(True)

    def get_generate_button(self) -> QPushButton:
        """Return generate button for connecting signals."""
        return self._generate_btn

    def get_copy_button(self) -> QPushButton:
        """Return copy button for connecting signals."""
        return self._copy_btn

    def copy_to_clipboard(self):
        """Copy URL to clipboard and show confirmation."""
        if self._generated_url:
            clipboard = QClipboard()
            clipboard.setText(self._generated_url)
            QMessageBox.information(self, "Copied", "Link copied to clipboard!")
