from PyQt5.QtWidgets import QMessageBox, QPushButton, QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

class CustomAlert(QWidget):
    close_app_signal = pyqtSignal()

    def __init__(self, parent=None, message="", is_error=False):
        super().__init__(parent)
        self.oldPos = QPoint()
        self.initUI(message, is_error)

    def initUI(self, message, is_error):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        # Remove translucent background to allow proper background color
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set maximum width to 800px
        self.setMaximumWidth(800)
        
        # Create main container with light blue background color and black border
        self.setStyleSheet("""
            QWidget {
                background-color: #CDEBF0;
                border: 3px solid #000000;
                border-radius: 15px;
            }
        """)

        # X close button in top-right corner
        close_button = QPushButton('×', self)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                font-weight: bold;
                border: none;
                font-size: 20px;
                padding: 5px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.accept)

        # Message content - show directly without title
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)  # Enable text wrapping
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setMinimumWidth(300)  # Ensure minimum width for proper wrapping
        self.message_label.setMaximumWidth(750)  # Leave some margin from the 800px max width
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: black;
                background-color: transparent;
                font-size: 16px;
                padding: 30px;
                margin: 20px;
                border-radius: 8px;
                min-height: 80px;
                font-weight: 600;
            }}
        """)

        # Main layout with margins to preserve border
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Small margins to preserve border visibility
        layout.setSpacing(0)
        
        # Add close button to top-right corner
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Push close button to the right
        top_layout.addWidget(close_button)
        top_layout.setContentsMargins(0, 10, 10, 0)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.message_label)
        
        self.setLayout(layout)
        
        # Set initial size and make it resizable
        self.resize(500, 200)
        self.setMinimumSize(400, 150)
        self.setMaximumSize(800, 400)

    def accept(self):
        self.close()  # Implement accept to close the widget
    def show_completion_alert(self):
        # Custom close button
        close_button = QPushButton('X', self)
        close_button.setStyleSheet("""
            QPushButton {
                color: black;
                background-color: white;
                border: none;
                font-size: 20px;
                margin: 0;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close)

        # Create a message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Generation Complete")
        msg_box.setText("The app generation is done. Do you want to close the window?")
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: pink;
                color: white;
                font-size: 16px;
                padding: 50px;
            }
            QPushButton {
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 50);
                padding: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        msg_box.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.button(QMessageBox.Yes).clicked.connect(self.yes_clicked)
        msg_box.button(QMessageBox.No).clicked.connect(msg_box.reject)

        # Move custom close button to the top-right corner of the message box
        close_button.setParent(msg_box)
        close_button.move(msg_box.width() - 30, 10)

        ret = msg_box.exec_()  # Use exec_ to block interaction with other windows

        if ret == QMessageBox.Yes:
            self.close()

    def yes_clicked(self):
        self.close_app_signal.emit()  # Emit signal when 'Yes' is clicked
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def set_success_message(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: green;")

    def set_error_message(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: red;")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = CustomAlert()
    ex.show_completion_alert()
    sys.exit(app.exec_())