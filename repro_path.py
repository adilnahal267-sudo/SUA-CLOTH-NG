import os

print(f"Current working directory: {os.getcwd()}")

# Mimic config.py logic
upload_folder_current = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
print(f"Current Configured Upload Folder: {upload_folder_current}")

# Proposed robust logic
basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder_robust = os.path.join(basedir, 'app', 'static', 'uploads')
print(f"Robust Upload Folder: {upload_folder_robust}")

# Check if they match
if upload_folder_current == upload_folder_robust:
    print("Paths match in this environment.")
else:
    print("Paths DO NOT match.")

# Test write permission
test_file = os.path.join(upload_folder_robust, 'test_write.txt')
try:
    with open(test_file, 'w') as f:
        f.write("test")
    print(f"Successfully wrote to {test_file}")
    os.remove(test_file)
    print("Successfully removed test file")
except Exception as e:
    print(f"Failed to write/remove file: {e}")
