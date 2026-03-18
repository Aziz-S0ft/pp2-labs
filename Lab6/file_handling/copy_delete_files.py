import shutil
import os

source_file = "sample.txt"
backup_file = "sample_backup.txt"
try:
    shutil.copy(source_file, backup_file)
    print("File copied successfully (backup created).")
except FileNotFoundError:
    print("Source file not found. Run write_files.py first.")
if os.path.exists(backup_file):
    print("\nBackup file content:\n")
    with open(backup_file, "r") as f:
        print(f.read())

def safe_delete(file_path):
    if os.path.exists(file_path):
        confirm = input(f"Do you really want to delete '{file_path}'? (yes/no): ")
        if confirm.lower() == "yes":
            os.remove(file_path)
            print(f"{file_path} deleted.")
        else:
            print("Deletion canceled.")
    else:
        print("File does not exist.")

safe_delete(backup_file)