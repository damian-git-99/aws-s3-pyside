#!/usr/bin/env python3
"""Main entry point for the Bucket Browser application."""
import sys
from PySide6.QtWidgets import QApplication

from src.models.bucket_browser_model import BucketBrowserModel
from src.views.bucket_browser_view import BucketBrowserView
from src.presenters.bucket_browser_presenter import BucketBrowserPresenter
from src.utils.styles import apply_style


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Apply modern styling
    apply_style(app)
    
    # Create Model
    model = BucketBrowserModel()
    
    # Create View
    view = BucketBrowserView()
    
    # Create Presenter
    presenter = BucketBrowserPresenter(model, view)
    
    # Initialize presenter (loads data)
    presenter.initialize()
    
    # Show view
    view.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
