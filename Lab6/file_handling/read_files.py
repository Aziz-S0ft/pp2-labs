file_name = "sample.txt"

try:
    with open(file_name, "r") as f:
        content = f.read()
        print("File contents:\n")
        print(content)
except FileNotFoundError:
    print("File not found. Run write_files.py first.")