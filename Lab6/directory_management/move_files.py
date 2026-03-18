import shutil
import os

source_file = "test_dir/file1.txt"
destination_dir = "test_dir/subdir1/"

if os.path.exists(source_file):
    shutil.move(source_file, destination_dir)
    print("File moved.")
else:
    print("Source file not found.")

source_file_2 = "test_dir/file2.py"
copy_destination = "test_dir/subdir1/file2_copy.py"

if os.path.exists(source_file_2):
    shutil.copy(source_file_2, copy_destination)
    print("File copied.")
else:
    print("Source file not found.")