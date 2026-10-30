"""
test_download_save.py
---------------------
PURPOSE:
    Tests download_and_save(): click Download, rename the new file to
    the input name, move it to output/.

HOW TO RUN (from the project root):
    python tests/test_download_save.py
    Switch to Chrome within 5 seconds. Apply must be done, Download white,
    and the download panel closed.
"""
import sys
sys.path.insert(0, "src")

import pyautogui
from PIL import Image
from image_list import get_images
import workflow

images = get_images()
print("Saving result for:", images[0].name)

print("Switch to Chrome. Starting in 5 seconds...")
pyautogui.sleep(5)

dest = workflow.download_and_save(images[0])
if dest:
    img = Image.open(dest)
    print("RESULT: OK", dest.name, img.size, "mode:", img.mode)
else:
    print("RESULT: FAILED")