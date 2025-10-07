from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal

class DirectoryInput(QWidget):
    directorySelected = pyqtSignal(str)

    def __init__(self, parent=None, placeholder="Select a directory", dialog_title="Select Directory", 
                 initial_dir="/", bgcolor=None):
        super().__init__(parent)
        self.dialog_title = dialog_title
        self.initial_dir = initial_dir
        self.placeholder = placeholder

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Full-width button to trigger directory dialog
        self.btn_browse = QPushButton(placeholder)
        self.btn_browse.clicked.connect(self.browse_directory)
        
        # Add button to layout
        layout.addWidget(self.btn_browse)

        # Styling the button
        self.apply_styling()

    def apply_styling(self):
        self.btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #CDEBF0;
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 12px;
                margin: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #BEE0E8;
            }
            QPushButton:pressed {
                background-color: #A8D4E0;
            }
        """)

    def browse_directory(self):
        directory_path = QFileDialog.getExistingDirectory(self, self.dialog_title, self.initial_dir)
        if directory_path:
            self.btn_browse.setText(directory_path)
            self.directorySelected.emit(directory_path)  # Emitting signal with the selected directory path
