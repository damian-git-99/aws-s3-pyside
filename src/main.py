#!/usr/bin/env python3
"""Main entry point for the Bucket Browser application."""
import sys
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

# Configure logging to show in console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Silence boto3/botocore logs - only show warnings and errors
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('s3transfer').setLevel(logging.WARNING)

from src.config import validate_config, ConfigurationError, load_config
from src.models.bucket_browser_model import BucketBrowserModel
from src.views.bucket_browser_view import BucketBrowserView
from src.presenters.bucket_browser_presenter import BucketBrowserPresenter
from src.services.s3_service import S3FileService
from src.utils.styles import apply_style


def show_config_error(missing_vars):
    """Show error dialog for missing configuration.
    
    Args:
        missing_vars: List of missing environment variable names
    """
    app = QApplication(sys.argv)
    
    error_msg = (
        "<h3>Configuration Error</h3>"
        "<p>The following required environment variables are missing:</p>"
        "<ul>"
    )
    for var in missing_vars:
        error_msg += f"<li><code>{var}</code></li>"
    error_msg += (
        "</ul>"
        "<p><b>To fix this:</b></p>"
        "<ol>"
        "<li>Copy <code>.env.example</code> to <code>.env</code></li>"
        "<li>Fill in your AWS credentials in <code>.env</code></li>"
        "<li>Ensure <code>.env</code> is not committed to version control</li>"
        "</ol>"
        "<p>Get AWS credentials from your <a href='https://console.aws.amazon.com/iam/'>AWS IAM Console</a>.</p>"
    )
    
    msg_box = QMessageBox()
    msg_box.setWindowTitle("AWS Configuration Required")
    msg_box.setTextFormat(Qt.TextFormat.RichText)
    msg_box.setText(error_msg)
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.exec()
    
    sys.exit(1)


def main():
    """Main application entry point."""
    # Check configuration before creating QApplication
    is_valid, missing_vars = validate_config()
    if not is_valid:
        show_config_error(missing_vars)
    
    app = QApplication(sys.argv)

    # Apply modern styling
    apply_style(app)

    # Load configuration and create S3 service
    config = load_config()
    s3_service = S3FileService(bucket_name=config.bucket_name)

    # Create Model
    model = BucketBrowserModel()

    # Create View
    view = BucketBrowserView()

    # Create Presenter with S3 service
    presenter = BucketBrowserPresenter(model, view, s3_service=s3_service)

    # Initialize presenter (loads data)
    presenter.initialize()

    # Show view
    view.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
