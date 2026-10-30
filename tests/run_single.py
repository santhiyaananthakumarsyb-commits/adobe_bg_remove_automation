"""
run_single.py
-------------
PURPOSE:
    Runs the complete workflow for the FIRST image in the input folder:
    upload, remove background, apply, download, save to output/.

HOW TO RUN (from the project root):
    python tests/run_single.py
    Switch to Chrome within 5 seconds. The EMPTY editor must be showing
    (press F5 first, and make sure the download panel is closed).
"""
import sys
sys.path.insert(0, "src")

import pyautogui
from PIL import Image
from image_list import get_images
import workflow

images = get_images()
if not images:
    sys.exit("input folder is empty")

print("Processing:", images[0].name)
print("Switch to Chrome (empty editor). Starting in 5 seconds...")
pyautogui.sleep(5)

dest = workflow.process_one(images[0])
if dest:
    img = Image.open(dest)
    print("RESULT: OK", dest.name, img.size, "mode:", img.mode)
else:
    print("RESULT: FAILED")