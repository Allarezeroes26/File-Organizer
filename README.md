## Python File Organizer

A simple Python automation tool that organizes your messy folders (like your Downloads folder) into neatly categorized subfolders — automatically! <br>
This project uses the built-in os and shutil modules to move files based on their extensions (images, documents, zips, programs, etc.).

---

## How It Works

The program reads every file in the target folder.
It checks the file’s extension and matches it to a category.
It automatically creates the necessary subfolders (if not already existing).
Files are then moved to their respective folders using shutil.move().
