import os
import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt

CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "Videos": [".mp4", ".mov", ".mkv", ".avi", ".3gp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Shortcuts": [".lnk"],
    "Torrents": [".torrent"],
    "Programs": [".exe", ".msi"],
    "Others": []
}


def organize_folder(path, log_widget):
    if not os.path.exists(path):
        log_widget.append("❌ Path not found.")
        return
    
    log_widget.append(f"\n📁 Organizing folder: {path}\n")
    
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        
        if os.path.isfile(full_path):
            ext = os.path.splitext(file)[1].lower()
            moved = False

            try:
                for category, extensions in CATEGORIES.items():
                    if ext in extensions:
                        folder_path = os.path.join(path, category)
                        os.makedirs(folder_path, exist_ok=True)
                        shutil.move(full_path, os.path.join(folder_path, file))
                        log_widget.append(f"✅ {file} → {category}/")
                        moved = True
                        break

                if not moved:
                    folder_path = os.path.join(path, "Others")
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(full_path, os.path.join(folder_path, file))
                    log_widget.append(f"✅ {file} → Others/")

            except FileNotFoundError:
                log_widget.append(f"⚠️ Skipped (File not found): {file}")
            except PermissionError:
                log_widget.append(f"🚫 Skipped (Access denied): {file}")

    log_widget.append("\n🎉 Organization complete!")


class FileOrganizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🗂️ File Organizer")
        self.setGeometry(400, 200, 600, 400)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select a folder to organize:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Folder path here...")
        self.path_input.setReadOnly(True)

        self.browse_button = QPushButton("📁 Browse Folder")
        self.browse_button.clicked.connect(self.browse_folder)

        self.organize_button = QPushButton("🚀 Organize Files")
        self.organize_button.clicked.connect(self.start_organizing)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.organize_button)
        layout.addWidget(QLabel("Logs:"))
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: 'Segoe UI';
                font-size: 14px;
            }

            QLabel {
                font-weight: bold;
                color: #ddd;
                margin-top: 5px;
                margin-bottom: 3px;
            }

            QLineEdit {
                background-color: #2b2b3d;
                border: 2px solid #3c3c55;
                border-radius: 6px;
                padding: 6px;
                color: #f8f8f2;
            }
            QLineEdit:focus {
                border: 2px solid #5b8def;
                background-color: #33334d;
            }

            QPushButton {
                background-color: #3b3b5c;
                border-radius: 6px;
                padding: 8px;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #5b5b7d;
            }
            QPushButton:hover {
                background-color: #5b8def;
                border: 1px solid #7fa4ff;
            }
            QPushButton:pressed {
                background-color: #2b2b3d;
            }

            QTextEdit {
                background-color: #24243a;
                border: 2px solid #3c3c55;
                border-radius: 6px;
                padding: 8px;
                color: #e0e0e0;
            }

            QMessageBox {
                background-color: #1e1e2f;
                color: #f0f0f0;
            }
        """)


    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_input.setText(folder)

    def start_organizing(self):
        folder_path = self.path_input.text()
        if not folder_path:
            QMessageBox.warning(self, "No Folder", "Please select a folder first!")
            return

        self.log_output.clear()
        organize_folder(folder_path, self.log_output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerGUI()
    window.show()
    sys.exit(app.exec_())
