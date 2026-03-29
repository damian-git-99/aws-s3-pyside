"""Image preview dialog for displaying images from S3."""

from typing import Optional

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton,
    QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage


class ImagePreviewDialog(QDialog):
    """Modal dialog for previewing images from S3.

    Displays an image with scroll support for large images.
    """

    def __init__(
        self, image_data: bytes, filename: str, parent: Optional[QWidget] = None
    ):
        """Initialize the image preview dialog.

        Args:
            image_data: Raw image bytes
            filename: Name of the file being previewed
            parent: Parent widget
        """
        super().__init__(parent)
        self._image_data = image_data
        self._filename = filename
        self._image_label: Optional[QLabel] = None

        self._setup_ui()
        self._load_image()

    def _setup_ui(self) -> None:
        """Setup the dialog UI components."""
        self.setWindowTitle(f"Preview - {self._filename}")
        self.resize(800, 600)
        self.setMinimumSize(400, 300)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Scroll area for image
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: 1px solid #cccccc;
                background-color: #f5f5f5;
            }
        """
        )

        # Image label inside scroll area
        self._image_label = QLabel()
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setStyleSheet("background-color: transparent;")
        self._scroll_area.setWidget(self._image_label)

        layout.addWidget(self._scroll_area)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def _load_image(self) -> None:
        """Load and display the image from bytes."""
        if not self._image_data:
            self._show_error("No image data available")
            return

        try:
            # Load image from bytes
            image = QImage()
            image.loadFromData(self._image_data)

            if image.isNull():
                self._show_error("Failed to load image. Format may not be supported.")
                return

            # Convert to pixmap
            pixmap = QPixmap.fromImage(image)

            # Display the image
            if self._image_label:
                self._image_label.setPixmap(pixmap)
                self._image_label.adjustSize()

        except Exception as e:
            self._show_error(f"Error loading image: {str(e)}")

    def _show_error(self, message: str) -> None:
        """Display an error message in the dialog.

        Args:
            message: Error message to display
        """
        if self._image_label:
            self._image_label.setText(f"❌ {message}")
            self._image_label.setStyleSheet(
                "color: #e74c3c; font-size: 14px; padding: 20px;"
            )
