import sys
import os
import shutil
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QProgressBar,
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from src.assets.text_symbol_replace import clean_text_to_underscore
from src.uiitems.close_button import CloseButton
from src.uiitems.directory_input import DirectoryInput
from src.uiitems.custom_alert import CustomAlert
from src.uiitems.dash_line import DashedLine


class MainWorkflowApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.input_directory = ""
        self.output_directory = ""
        self.setMouseTracking(True)
        self.oldPos = self.pos()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName("App")

        self.setStyleSheet(
            """
            QWidget {
                font-family: 'Arial';
                background-color: transparent; 
                border: 2px solid #CDEBF0; 
                border-radius: 20px;
            }
            QPushButton {
                background-color: #CDEBF0;
                color: black;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #BEE0E8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                margin: 10px;
            }
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 8px;
                text-align: center;
                margin: 10px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 6px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(self.create_title_bar())
        layout.addWidget(self.create_logo_label())

        # Add dashed line separator
        dash_line_1 = DashedLine(color='#CDEBF0', orientation='horizontal')
        layout.addWidget(dash_line_1)

        self.resize(540, 880)

        # Input directory using DirectoryInput component
        self.input_directory_input = DirectoryInput(
            parent=self,
            placeholder="Select Input Directory",
            dialog_title="Select Input Directory",
            initial_dir="/"
        )
        self.input_directory_input.directorySelected.connect(self.on_input_directory_selected)
        layout.addWidget(self.input_directory_input)

        # Output directory using DirectoryInput component
        self.output_directory_input = DirectoryInput(
            parent=self,
            placeholder="Select Output Directory", 
            dialog_title="Select Output Directory",
            initial_dir="/"
        )
        self.output_directory_input.directorySelected.connect(self.on_output_directory_selected)
        layout.addWidget(self.output_directory_input)

        # Add dashed line separator
        dash_line_2 = DashedLine(color='#CDEBF0', orientation='horizontal')
        layout.addWidget(dash_line_2)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Submit button with black background and blue border
        self.submit_button = self.create_button("Start Cooking", self.process_files)
        self.submit_button.setEnabled(False)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                font-weight: bold;
                border: 2px solid #CDEBF0;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #cccccc;
                border-color: #999999;
            }
        """)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def create_title_bar(self):
        title_bar = QHBoxLayout()
        close_button = CloseButton()
        close_button.clicked.connect(self.close)
        title_bar.addWidget(close_button, alignment=Qt.AlignRight)
        return title_bar

    def create_logo_label(self):
        logo = QLabel(self)
        # Get the base path for the application
        if getattr(sys, "frozen", False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the cover image
        cover_path = os.path.join(base_path, "static", "logo_imgs", "cover.png")
        # Check if file exists and load it
        if os.path.exists(cover_path):
            pixmap = QPixmap(cover_path).scaled(500, 800)
        else:
            # Fallback: create a placeholder or use a default image
            print(f"Warning: Cover image not found at {cover_path}")
            pixmap = QPixmap(500, 800)
            pixmap.fill(Qt.lightGray)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        return logo

    def log_message(self, message):
        """Add a message to the log text area"""
        self.log_text.append(message)
        self.log_text.ensureCursorVisible()

    def create_button(self, text, slot, style=None):
        button = QPushButton(text, self)
        button.clicked.connect(slot)
        button.setStyleSheet(
            style
            if style
            else """
            QPushButton {
                background-color: #CDEBF0;
                color: black;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #BEE0E8;
            }
        """
        )
        return button

    def on_input_directory_selected(self, directory_path):
        """Handle input directory selection from DirectoryInput"""
        self.input_directory = directory_path
        self.update_submit_button_state()

    def on_output_directory_selected(self, directory_path):
        """Handle output directory selection from DirectoryInput"""
        self.output_directory = directory_path
        self.update_submit_button_state()

    def update_submit_button_state(self):
        """Enable/disable submit button based on directory selection"""
        if self.input_directory and self.output_directory:
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def process_files(self):
        """Process files from input to output directory"""
        if not self.input_directory or not self.output_directory:
            alert = CustomAlert(self, "Please select both input and output directories.", is_error=True)
            alert.show()
            return

        try:
            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.submit_button.setEnabled(False)
            
            # Get all files from input directory
            input_path = Path(self.input_directory)
            files_to_process = []
            
            # Find all files recursively
            for file_path in input_path.rglob("*"):
                if file_path.is_file():
                    files_to_process.append(file_path)
            
            if not files_to_process:
                alert = CustomAlert(self, "No files found in the input directory.", is_error=True)
                alert.show()
                self.progress_bar.setVisible(False)
                self.submit_button.setEnabled(True)
                return
            
            self.progress_bar.setMaximum(len(files_to_process))
            
            processed_count = 0
            error_count = 0
            
            for i, file_path in enumerate(files_to_process):
                try:
                    # Get relative path from input directory
                    relative_path = file_path.relative_to(input_path)
                    
                    # Clean the filename using our function
                    original_name = file_path.stem
                    file_extension = file_path.suffix
                    cleaned_name = clean_text_to_underscore(original_name)
                    
                    # Create new filename
                    new_filename = f"{cleaned_name}{file_extension}"
                    
                    # Create output path maintaining directory structure
                    output_path = Path(self.output_directory) / relative_path.parent
                    output_path.mkdir(parents=True, exist_ok=True)
                    
                    # Final output file path
                    final_output_path = output_path / new_filename
                    
                    # Copy file to output directory with cleaned name
                    shutil.copy2(file_path, final_output_path)
                    
                    processed_count += 1
                    
                except Exception as e:
                    error_count += 1
                    if error_count == 1:  # Show first error
                        alert = CustomAlert(self, f"Error processing {file_path.name}: {str(e)}", is_error=True)
                        alert.show()
                
                # Update progress
                self.progress_bar.setValue(i + 1)
                QApplication.processEvents()  # Keep UI responsive
            
            # Hide progress bar
            self.progress_bar.setVisible(False)
            
            # Show completion message
            if error_count == 0:
                alert = CustomAlert(self, f"Successfully processed {processed_count} files!", is_error=False)
                alert.show()
            else:
                alert = CustomAlert(self, f"Processed {processed_count} files successfully.\n{error_count} files had errors.", is_error=True)
                alert.show()
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            alert = CustomAlert(self, f"An error occurred: {str(e)}", is_error=True)
            alert.show()
        
        finally:
            self.submit_button.setEnabled(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWorkflowApp()
    window.show()
    sys.exit(app.exec_())