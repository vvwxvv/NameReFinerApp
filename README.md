# NameRefinerApp - Intelligent File Naming & Organization Tool

A modern, stylish desktop application for intelligent file renaming and organization, built with PyQt5. **NameRefinerApp** is designed to clean up file names by removing symbols, replacing spaces with underscores, and organizing files systematically for better file management and organization.

## Features

- **Intelligent File Renaming:** Clean up file names by removing symbols and replacing spaces with underscores
- **Smart Naming Rules:** 
  - Replace spaces with underscores (`_`)
  - Remove all symbols and special characters
  - Add underscore before numbers that follow words (e.g., `text1` becomes `text_1`)
  - Convert all text to lowercase for consistency
- **Batch Processing:** Process multiple files and folders simultaneously
- **Recursive Folder Support:** Process files in subfolders automatically
- **Multiple File Types:** Support for images, documents, videos, audio, archives, and more
- **Dry Run Mode:** Preview changes before applying them
- **Progress Tracking:** Visual feedback during file processing operations
- **Custom UI Elements:** Includes blinking buttons, custom alerts, and a frameless, translucent window
- **Modern Interface:** Clean, modern UI with custom styling and animations
- **Cross-Platform:** Designed for Windows, but can be adapted for other platforms

## File Naming Examples

Here are examples of how the app transforms file names:

### Basic Symbol and Space Replacement
- `My Vacation Photo (2023).jpg` → `my_vacation_photo_2023.jpg`
- `Document@#$%Final.pdf` → `document_final.pdf`
- `File@Name#123$%^&*().txt` → `file_name_123.txt`

### Number Handling After Words
- `A Bite of the Moon1.jpg` → `a_bite_of_the_moon_1.jpg`
- `SOLO EXHIBITION- Hotel Smoke and Ash2.JPG` → `solo_exhibition_hotel_smoke_and_ash_2.jpg`
- `The Cambrian Period5.JPG` → `the_cambrian_period_5.jpg`

### Complex Examples
- `400 million years ago, it was the ocean, and 400 million years later, it is the desert1.txt` → `400_million_years_ago_it_was_the_ocean_and_400_million_years_later_it_is_the_desert_1.txt`
- `Hello, World! How are you?.docx` → `hello_world_how_are_you.docx`
- `Multiple    spaces   here.png` → `multiple_spaces_here.png`

## Screenshots

> _Add screenshots of your app here (UI, before/after file renaming, etc.)_

## Getting Started

### Prerequisites

- Python 3.12+
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/BackgroundImageRemover.git
   cd BackgroundImageRemover
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up virtual environment (recommended):**

   ```bash
   python -m venv appenv
   appenv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

### Running the App

```bash
python main.py
```

The main window will appear, allowing you to select a folder containing files you want to rename. You can choose to process specific file types or all files, and preview the changes before applying them. The app will intelligently clean up file names according to the naming rules.

### Packaging as an EXE (Windows)

This project includes build scripts for easy packaging. To build a standalone executable:

**Using batch file:**
```bash
build.bat
```

**Using PowerShell:**
```powershell
.\build.ps1
```

**Manual build:**
```bash
pyinstaller build_exe.spec
```

The output will be in the `dist/` directory as `FileNameRefinerApp.exe`.

## Project Structure

```
FileNameRefinerApp/
│
├── main.py                # Main application entry point (PyQt5 GUI)
├── requirements.txt       # Python dependencies
├── build_exe.spec         # PyInstaller spec for Windows packaging
├── build.bat              # Windows batch build script
├── build.ps1              # PowerShell build script
├── src/
│   ├── assets/            # File renaming and utility scripts
│   │   ├── subfolder_file_rename.py # Main file renaming logic
│   │   └── text_symbol_replace.py # Text cleaning and transformation utilities
│   ├── uiitems/           # Custom UI widgets
│   │   ├── close_button.py # Custom close button
│   │   ├── blink_button.py # Animated blinking button
│   │   ├── text_box.py    # Custom text input
│   │   ├── preview_box.py # File preview component
│   │   ├── notification_bar.py # Notification display
│   │   ├── file_input.py  # File input component
│   │   ├── dash_line.py   # Decorative dash line
│   │   ├── custom_alert.py # Custom alert dialogs
│   │   ├── collapsible_box.py # Collapsible UI sections
│   │   └── directory_input.py # Directory selection component
│   └── widgets/           # Main application widgets
│       ├── drag_drop.py   # Drag and drop functionality
│       ├── img_renamer.py # File renaming widget
│       ├── initiation_files_input.py # File input widget
│       ├── select_initiation_csv.py # CSV selection widget
│       └── login.py       # Login widget
├── static/
│   ├── logo_imgs/         # App icons and logos
│   │   ├── cover.png      # App cover image
│   │   └── favicon.ico    # App icon
│   └── styles.css         # CSS styling (for documentation)
├── appenv/                # Virtual environment directory
└── README.md
```

## Dependencies

- **PyQt5** - GUI framework
- **pathlib** - Modern path handling
- **shutil** - File operations
- **re** - Regular expressions for text processing
- **os** - Operating system interface
- **pyinstaller** - For creating standalone executables

## File Naming Features

The intelligent file naming system includes:

- **Symbol Removal:** Removes all special characters and symbols from file names
- **Space Replacement:** Converts spaces to underscores for better file system compatibility
- **Number Handling:** Adds underscores before numbers that follow words (e.g., `text1` → `text_1`)
- **Case Normalization:** Converts all text to lowercase for consistency
- **Multiple Underscore Cleanup:** Removes consecutive underscores and trims leading/trailing underscores
- **Batch Processing:** Handles multiple files and folders simultaneously
- **File Type Support:** Works with images, documents, videos, audio, archives, and more
- **Dry Run Mode:** Preview changes before applying them
- **Error Handling:** Comprehensive error handling and logging
- **Recursive Processing:** Processes files in subfolders automatically

## Build Scripts

The project includes several build scripts for convenience:

- **build.bat** - Windows batch script for building executable
- **build.ps1** - PowerShell script for building executable
- **build_exe.spec** - Main PyInstaller specification file
- **main.spec** - Alternative PyInstaller specification file

## Customization

- **UI Styling:** Modify the stylesheet in `main.py` for custom colors and layout
- **File Types:** Extend `src/assets/subfolder_file_rename.py` to support additional file extensions
- **Naming Rules:** Customize text transformation rules in `src/assets/text_symbol_replace.py`
- **UI Components:** Customize widgets in `src/uiitems/` and `src/widgets/` directories

## License

MIT License. See [LICENSE](LICENSE) for details.
