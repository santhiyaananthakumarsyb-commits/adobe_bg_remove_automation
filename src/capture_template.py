"""
capture_template.py
-------------------
PURPOSE:
    Saves a small cropped image ("template") of a button, centered on the
    mouse position. OpenCV will later search the screen for these templates
    to find where to click (Upload, Remove background, Apply, Download).

WHY NOT USE THE SNIPPING TOOL:
    This script captures with the same method PyAutoGUI uses at run time,
    so the template pixels match what the automation will see.

WHEN TO USE:
    - Milestone 3 (template capture), once per button
    - Again for any button whose look changes (Adobe UI update, new theme)

HOW TO RUN (from the project root):
    python src/capture_template.py <name>
    Examples:
        python src/capture_template.py upload
        python src/capture_template.py remove_background
        python src/capture_template.py apply
        python src/capture_template.py download

    Then, within 6 seconds, switch to Chrome and HOVER (do not click) the
    mouse over the CENTER of the button. Keep it still until "Saved" appears.

OUTPUT:
    templates/<name>.png   (160 x 50 pixel crop around the mouse)
"""

import sys
import pyautogui
from pathlib import Path

# The template name must be given on the command line.
# sys.argv[0] is the script name, sys.argv[1] is the name you typed.
if len(sys.argv) != 2:
    print("Usage: python src/capture_template.py <name>")
    sys.exit(1)

name = sys.argv[1]

# Make sure the templates folder exists.
Path("templates").mkdir(exist_ok=True)

print(f"Capturing template: {name}")
print("Switch to Chrome. Hover the mouse over the CENTER of the button.")
print("Capturing in 6 seconds...")

# Delay so you can switch to Chrome and position the mouse.
pyautogui.sleep(6)

# Read where the mouse is now: this is the center of the crop.
x, y = pyautogui.position()
print("Mouse position:", x, y)

# Crop box size in pixels. Small enough to contain only the button,
# large enough to be unique on screen.
w, h = 160, 50

# Top-left corner of the box. max(0, ...) stops it going off-screen.
left = max(0, x - w // 2)
top = max(0, y - h // 2)

# Capture only that region of the screen.
shot = pyautogui.screenshot(region=(left, top, w, h))

out = f"templates/{name}.png"
shot.save(out)
print("Saved", out, "size:", shot.size)