import os
nested_path = "test_dir/subdir1/subdir2"

os.makedirs(nested_path, exist_ok=True)
print("Directories created.")
with open("test_dir/file1.txt", "w") as f:
    f.write("Hello")

with open("test_dir/file2.py", "w") as f:
    f.write("print('Python file')")

with open("test_dir/subdir1/file3.txt", "w") as f:
    f.write("Nested file")

print("\nContents of test_dir:")
for item in os.listdir("test_dir"):
    print(item)

print("\nSearching for .txt files:")

for root, dirs, files in os.walk("test_dir"):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))