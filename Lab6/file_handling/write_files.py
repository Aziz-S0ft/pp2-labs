file_name = "sample.txt"
with open(file_name, "w") as f:
    f.write("Line 1: Hello, World!\n")
    f.write("Line 2: This is a sample file.\n")
print("File created and initial data written.")
with open(file_name, "a") as f:
    f.write("Line 3: Appended line.\n")
    f.write("Line 4: Another appended line.\n")
print("New lines appended.")