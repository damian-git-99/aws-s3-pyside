#!/usr/bin/env python3
"""Main entry point for the Bucket Browser application."""
import sys
import logging
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QStyleFactory
from PySide6.QtGui import QPalette, QColor

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

from src.config.config_manager import ConfigManager, get_config_manager
from src.config import ConfigManager as ConfigManagerClass
from src.presenters.config_presenter import ConfigPresenter
from src.models.bucket_browser_model import BucketBrowserModel
from src.views.bucket_browser_view import BucketBrowserView
from src.presenters.bucket_browser_presenter import BucketBrowserPresenter
from src.services.s3_service import S3FileService
from src.utils.styles import apply_style


def configure_light_palette(app):
    """Configure application with explicit light palette to disable dark mode."""
    app.setStyle('Fusion')
    
    # Force light palette with explicit colors
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    app.setPalette(palette)


def show_config_error(missing_vars):
    """Show error dialog for missing configuration.
    
    Args:
        missing_vars: List of missing environment variable names
    """
    app = QApplication(sys.argv)
    configure_light_palette(app)
    
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


def run_setup_wizard(config_presenter):
    """Run the setup wizard for first-time configuration.
    
    Args:
        config_presenter: ConfigPresenter instance
        
    Returns:
        True if setup was completed, False if cancelled
    """
    return config_presenter.show_setup_wizard()


def main():
    """Main application entry point."""
    # Create QApplication first (needed for dialogs)
    app = QApplication(sys.argv)

    # Force light theme to prevent Windows dark mode issues
    configure_light_palette(app)

    # Apply modern styling
    apply_style(app)

    # Initialize configuration manager
    config_manager = get_config_manager()
    
    # Check if this is first-time setup
    needs_setup = not config_manager.has_config()
    
    # Create config presenter (without parent for now, will set later)
    config_presenter = ConfigPresenter(config_manager)
    
    if needs_setup:
        # Show setup wizard
        setup_completed = run_setup_wizard(config_presenter)
        
        if not setup_completed:
            # User cancelled setup, exit application
            sys.exit(0)
    
    # Verify we have all required configuration
    if not config_manager.is_fully_configured():
        missing = config_manager.get_missing_keys()
        show_config_error(missing)
        sys.exit(1)
    
    # Load configuration and create S3 service
    config = config_manager.get_all()
    bucket_name = config.get('AWS_S3_BUCKET_NAME', '')
    
    # Set environment variables for boto3
    os.environ['AWS_ACCESS_KEY_ID'] = config.get('AWS_ACCESS_KEY_ID', '')
    os.environ['AWS_SECRET_ACCESS_KEY'] = config.get('AWS_SECRET_ACCESS_KEY', '')
    os.environ['AWS_DEFAULT_REGION'] = config.get('AWS_DEFAULT_REGION', '')
    
    s3_service = S3FileService(bucket_name=bucket_name)

    # Create Model
    model = BucketBrowserModel()

    # Create View
    view = BucketBrowserView()
    
    # Set parent for config presenter (for modal dialogs)
    config_presenter._parent = view
    
    # Connect settings button to config presenter
    view.set_on_settings_callback(config_presenter.show_settings_panel)

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
