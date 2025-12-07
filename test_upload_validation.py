import os
import sys

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.routes.items import allowed_file
from config import Config

def test_path_resolution():
    print("Testing Path Resolution...")
    basedir = os.path.abspath(os.path.dirname(os.path.join(os.getcwd(), 'config.py')))
    expected_upload_folder = os.path.join(basedir, 'app', 'static', 'uploads')
    
    # Instantiate Config to see what it resolves to
    config = Config()
    print(f"Configured Upload Folder: {config.UPLOAD_FOLDER}")
    print(f"Expected Upload Folder:   {expected_upload_folder}")
    
    if config.UPLOAD_FOLDER == expected_upload_folder:
        print("PASS: Path resolution matches.")
    else:
        print("FAIL: Path resolution mismatch.")

def test_extension_validation():
    print("\nTesting Extension Validation...")
    test_cases = {
        'image.jpg': True,
        'image.png': True,
        'image.jpeg': True,
        'image.gif': True,
        'image.webp': True,
        'script.js': False,
        'document.pdf': False,
        'image': False,
        'image.JPG': True, # Case insensitivity
    }
    
    all_passed = True
    for filename, expected in test_cases.items():
        result = allowed_file(filename)
        if result == expected:
            print(f"PASS: {filename} -> {result}")
        else:
            print(f"FAIL: {filename} -> {result} (Expected {expected})")
            all_passed = False
            
    if all_passed:
        print("PASS: All extension tests passed.")
    else:
        print("FAIL: Some extension tests failed.")

if __name__ == "__main__":
    test_path_resolution()
    test_extension_validation()
