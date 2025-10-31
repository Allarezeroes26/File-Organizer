import os
import shutil

CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Shortcuts": [".lnk"],
    "Torrents": [".torrent"],
    "Programs": [".exe", ".msi"],
    "Others": []
}

def organize_folder(path):
    if not os.path.exists(path):
        print("❌ Path not found.")
        return
    
    print(f"\n📁 Organizing folder: {path}\n")
    
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
                        print(f"✅ {file} → {category}/")
                        moved = True
                        break

                if not moved:
                    folder_path = os.path.join(path, "Others")
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(full_path, os.path.join(folder_path, file))
                    print(f"✅ {file} → Others/")

            except FileNotFoundError:
                print(f"⚠️ Skipped (File not found): {file}")
            except PermissionError:
                print(f"🚫 Skipped (Access denied): {file}")

    print("\n🎉 Organization complete!")

if __name__ == "__main__":
    folder = input("Enter path folder to organize: ")
    organize_folder(folder)
