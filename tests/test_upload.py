"""
test_upload.py
--------------
PURPOSE:
    Tests the Upload step with the FIRST image in the input folder.
    Stops after the image loads.

HOW TO RUN (from the project root):
    python tests/test_upload.py
    Switch to Chrome within 5 seconds (EMPTY editor, Upload visible).
"""
import sys
sys.path.insert(0, "src")

import pyautogui
from image_list import get_images
import workflow

images = get_images()
print(f"Found {len(images)} image(s):")
for p in images:
    print("  ", p.name)

if not images:
    sys.exit("input folder is empty")

print("\nSwitch to Chrome (empty editor). Starting in 5 seconds...")
pyautogui.sleep(5)

ok = workflow.upload_image(images[0])
print("RESULT:", "OK" if ok else "FAILED")