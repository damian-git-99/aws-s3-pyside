from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        self.setWindowTitle("S3 File Manager")
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("S3 File Manager"))
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
