import os
import shutil
from pathlib import Path
from src.assets.text_symbol_replace import clean_text_to_underscore

def find_and_rename_files(root_folder, file_extensions=None, dry_run=True, recursive=True):
    """
    Find files in folder and subfolders, rename them using clean_text_to_underscore function.
    
    Args:
        root_folder (str): Root folder path to search
        file_extensions (list): List of file extensions to process (e.g., ['.jpg', '.png', '.pdf'])
                              If None, processes all files
        dry_run (bool): If True, only show what would be renamed without actually renaming
        recursive (bool): If True, search subfolders recursively
        
    Returns:
        dict: Summary of operations performed
    """
    if file_extensions is None:
        file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg',  # Images
                          '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',  # Documents
                          '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.mpg', '.mpeg',  # Videos
                          '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma',  # Audio
                          '.zip', '.rar', '.7z', '.tar', '.gz',  # Archives
                          '.xlsx', '.xls', '.csv', '.ppt', '.pptx',  # Office
                          '.html', '.htm', '.css', '.js', '.php', '.py', '.java', '.cpp', '.c',  # Code
                          '.xml', '.json', '.yaml', '.yml', '.ini', '.cfg', '.conf',  # Config
                          '.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg',  # Executables
                          '.iso', '.img', '.bin', '.cue',  # Disk images
                          '.ttf', '.otf', '.woff', '.woff2', '.eot',  # Fonts
                          '.psd', '.ai', '.eps', '.sketch', '.fig',  # Design
                          '.sql', '.db', '.sqlite', '.mdb', '.accdb',  # Databases
                          '.log', '.bak', '.tmp', '.temp', '.cache',  # System files
                          '.md', '.markdown', '.rst', '.tex', '.latex',  # Markup
                          '.sh', '.bat', '.cmd', '.ps1', '.vbs',  # Scripts
                          '.apk', '.ipa', '.app', '.dmg', '.pkg',  # Mobile/Apps
                          '.3ds', '.obj', '.fbx', '.dae', '.blend', '.max', '.ma', '.mb',  # 3D Models
                          '.srt', '.sub', '.vtt', '.ass', '.ssa',  # Subtitles
                          '.torrent', '.magnet',  # Torrents
                          '.key', '.pem', '.crt', '.cer', '.p12', '.pfx',  # Certificates
                          '.dll', '.so', '.dylib', '.lib', '.a',  # Libraries
                          '.h', '.hpp', '.hxx', '.cxx', '.cc',  # C++ headers
                          '.swift', '.kt', '.scala', '.rb', '.go', '.rs', '.dart',  # Other languages
                          '.vue', '.jsx', '.tsx', '.ts', '.svelte',  # Frontend frameworks
                          '.dockerfile', '.dockerignore', '.gitignore', '.gitattributes',  # DevOps
                          '.env', '.properties', '.toml', '.lock', '.gradle', '.maven',  # Build tools
                          '.jpeg', '.JPG', '.JPEG', '.PNG', '.GIF', '.BMP', '.TIFF', '.WEBP', '.SVG',  # Uppercase images
                          '.PDF', '.DOC', '.DOCX', '.TXT', '.RTF', '.ODT',  # Uppercase documents
                          '.MP4', '.AVI', '.MOV', '.WMV', '.FLV', '.MKV', '.MPG', '.MPEG',  # Uppercase videos
                          '.MP3', '.WAV', '.FLAC', '.AAC', '.OGG', '.WMA']  # Uppercase audio
    
    # Convert extensions to lowercase for comparison
    file_extensions = [ext.lower() for ext in file_extensions]
    
    root_path = Path(root_folder)
    if not root_path.exists():
        print(f"Error: Folder '{root_folder}' does not exist!")
        return {"error": "Folder not found"}
    
    renamed_files = []
    skipped_files = []
    errors = []
    
    # Get all files based on recursive setting
    if recursive:
        files_to_process = []
        for ext in file_extensions:
            files_to_process.extend(root_path.rglob(f"*{ext}"))
            files_to_process.extend(root_path.rglob(f"*{ext.upper()}"))
    else:
        files_to_process = []
        for ext in file_extensions:
            files_to_process.extend(root_path.glob(f"*{ext}"))
            files_to_process.extend(root_path.glob(f"*{ext.upper()}"))
    
    print(f"Found {len(files_to_process)} files to process...")
    print(f"File extensions: {file_extensions}")
    print(f"Recursive search: {recursive}")
    print(f"Dry run mode: {dry_run}")
    print("-" * 60)
    
    for file_path in files_to_process:
        try:
            # Get original filename without extension
            original_name = file_path.stem
            file_extension = file_path.suffix
            
            # Clean the filename using our function
            cleaned_name = clean_text_to_underscore(original_name)
            
            # Create new filename
            new_filename = f"{cleaned_name}{file_extension}"
            new_file_path = file_path.parent / new_filename
            
            # Check if filename actually changed
            if original_name == cleaned_name:
                skipped_files.append({
                    "path": str(file_path),
                    "reason": "No changes needed"
                })
                continue
            
            # Check if target file already exists
            if new_file_path.exists() and new_file_path != file_path:
                skipped_files.append({
                    "path": str(file_path),
                    "reason": f"Target file already exists: {new_filename}"
                })
                continue
            
            if dry_run:
                print(f"WOULD RENAME: {file_path.name} -> {new_filename}")
                renamed_files.append({
                    "original": str(file_path),
                    "new": str(new_file_path),
                    "status": "would_rename"
                })
            else:
                # Actually rename the file
                shutil.move(str(file_path), str(new_file_path))
                print(f"RENAMED: {file_path.name} -> {new_filename}")
                renamed_files.append({
                    "original": str(file_path),
                    "new": str(new_file_path),
                    "status": "renamed"
                })
                
        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            print(f"ERROR: {error_msg}")
            errors.append(error_msg)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Files processed: {len(files_to_process)}")
    print(f"Files {'would be ' if dry_run else ''}renamed: {len(renamed_files)}")
    print(f"Files skipped: {len(skipped_files)}")
    print(f"Errors: {len(errors)}")
    
    if skipped_files:
        print("\nSkipped files:")
        for item in skipped_files[:10]:  # Show first 10
            print(f"  - {item['path']}: {item['reason']}")
        if len(skipped_files) > 10:
            print(f"  ... and {len(skipped_files) - 10} more")
    
    if errors:
        print("\nErrors:")
        for error in errors[:5]:  # Show first 5
            print(f"  - {error}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")
    
    return {
        "total_files": len(files_to_process),
        "renamed": len(renamed_files),
        "skipped": len(skipped_files),
        "errors": len(errors),
        "details": {
            "renamed_files": renamed_files,
            "skipped_files": skipped_files,
            "errors": errors
        }
    }

def rename_image_files(folder_path, dry_run=True):
    """
    Convenience function specifically for image files.
    
    Args:
        folder_path (str): Folder path to process
        dry_run (bool): If True, only show what would be renamed
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
    return find_and_rename_files(folder_path, image_extensions, dry_run, recursive=True)

def rename_all_files(folder_path, dry_run=True):
    """
    Convenience function for all file types.
    
    Args:
        folder_path (str): Folder path to process
        dry_run (bool): If True, only show what would be renamed
    """
    return find_and_rename_files(folder_path, None, dry_run, recursive=True)

def rename_all_files_in_imgs(dry_run=False):
    """
    Convenience function to rename ALL file types in the imgs directory.
    This includes images, documents, videos, and any other file types.
    
    Args:
        dry_run (bool): If True, only show what would be renamed
    """
    imgs_dir = "imgs"
    
    if not os.path.exists(imgs_dir):
        print(f"Error: Directory '{imgs_dir}' does not exist!")
        return None
    
    print(f"Processing directory: {os.path.abspath(imgs_dir)}")
    print("Processing ALL file types (images, documents, videos, etc.)")
    
    # Process all file types in the imgs directory
    return find_and_rename_files(imgs_dir, None, dry_run, recursive=True)

def interactive_rename():
    """
    Interactive mode for file renaming.
    """
    print("=== File Rename Tool ===")
    print("This tool will rename files by removing symbols and spaces, replacing with underscores.")
    print()
    
    # Get folder path
    while True:
        folder_path = input("Enter folder path to process: ").strip()
        if os.path.exists(folder_path):
            break
        print("Folder does not exist. Please try again.")
    
    # Get file type preference
    print("\nWhat type of files do you want to rename?")
    print("1. Image files only (.jpg, .png, .gif, etc.)")
    print("2. All files")
    print("3. Custom file extensions")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
    elif choice == "2":
        file_extensions = None
    elif choice == "3":
        extensions_input = input("Enter file extensions separated by commas (e.g., .jpg,.png,.pdf): ").strip()
        file_extensions = [ext.strip() for ext in extensions_input.split(',') if ext.strip()]
    else:
        print("Invalid choice. Using image files only.")
        file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
    
    # Dry run first
    print(f"\nRunning dry run first to show what would be changed...")
    result = find_and_rename_files(folder_path, file_extensions, dry_run=True, recursive=True)
    
    if result.get("renamed", 0) > 0:
        confirm = input(f"\nFound {result['renamed']} files to rename. Proceed with actual renaming? (y/n): ").strip().lower()
        if confirm == 'y':
            print("\nProceeding with actual renaming...")
            result = find_and_rename_files(folder_path, file_extensions, dry_run=False, recursive=True)
            print("Renaming completed!")
        else:
            print("Renaming cancelled.")
    else:
        print("No files need renaming.")

# Example usage
if __name__ == "__main__":
    # Example 1: Rename ALL file types in the imgs directory (dry run first)
    print("Running dry run on imgs directory...")
    print("This will process ALL file types: images, documents, videos, etc.")
    result = rename_all_files_in_imgs(dry_run=True)
    
    if result and result.get("renamed", 0) > 0:
        print(f"\nFound {result['renamed']} files to rename.")
        confirm = input("Proceed with actual renaming? (y/n): ").strip().lower()
        if confirm == 'y':
            print("\nProceeding with actual renaming...")
            result = rename_all_files_in_imgs(dry_run=False)
            print("Renaming completed!")
        else:
            print("Renaming cancelled.")
    else:
        print("No files need renaming.")
    
    # Example 2: Rename image files in a folder (dry run)
    # folder_path = r"C:\Users\YourName\Pictures"
    # rename_image_files(folder_path, dry_run=True)
    
    # Example 3: Rename all files in a folder
    # folder_path = r"C:\Users\YourName\Documents"
    # rename_all_files(folder_path, dry_run=True)
    
    # Example 4: Interactive mode
    # interactive_rename()
    
    # Example 5: Custom file types
    # custom_extensions = ['.jpg', '.png', '.pdf', '.docx']
    # find_and_rename_files(r"C:\Users\YourName\Documents", custom_extensions, dry_run=True)

