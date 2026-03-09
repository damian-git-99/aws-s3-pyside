"""Modern styles for the bucket browser application."""

MODERN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QToolBar {
    background-color: #ffffff;
    border: none;
    padding: 8px;
    spacing: 8px;
}

QToolBar QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 500;
}

QToolBar QPushButton:hover {
    background-color: #1976D2;
}

QToolBar QPushButton:pressed {
    background-color: #0D47A1;
}

QToolBar QPushButton#upload_btn {
    background-color: #4CAF50;
}

QToolBar QPushButton#upload_btn:hover {
    background-color: #388E3C;
}

QTableWidget {
    background-color: white;
    border: none;
    gridline-color: #e0e0e0;
    selection-background-color: #e3f2fd;
    selection-color: #000000;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #e0e0e0;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
}

QHeaderView::section {
    background-color: #fafafa;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #e0e0e0;
    font-weight: 600;
    color: #333333;
}

QHeaderView::section:hover {
    background-color: #f0f0f0;
}

QLabel {
    color: #666666;
    padding: 8px;
}

QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
}

QMenuBar::item {
    padding: 8px 16px;
    background: transparent;
}

QMenuBar::item:selected {
    background-color: #e3f2fd;
}

QStatusBar {
    background-color: #fafafa;
    border-top: 1px solid #e0e0e0;
}
"""


def apply_style(app) -> None:
    """Apply the modern style to the application."""
    app.setStyleSheet(MODERN_STYLE)
