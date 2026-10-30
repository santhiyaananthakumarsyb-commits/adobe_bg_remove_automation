"""
calibrate.py
------------
PURPOSE:
    Takes ONE full-screen screenshot after a 5 second delay and saves it
    to logs/calibration_screen.png.
    This is our "reference picture" of how Chrome + Firefly should look
    before automation runs.

WHEN TO USE:
    - Milestone 2 (screen calibration)
    - Any time the layout may have changed (new Chrome tabs, bookmarks bar
      shown/hidden, zoom changed, new monitor, new Windows scaling)
    - When template matching suddenly stops finding buttons

HOW TO RUN (from the project root):
    python src/calibrate.py
    Then switch to Chrome (Firefly empty editor page) within 5 seconds.

OUTPUT:
    logs/calibration_screen.png  (compare this with earlier screenshots;
    the size should match pyautogui.size(), e.g. 1366 x 768)
"""

import pyautogui
from pathlib import Path

# Create the logs folder if it does not exist yet.
Path("logs").mkdir(exist_ok=True)

print("Switch to Chrome (Firefly empty editor page).")
print("Taking a screenshot in 5 seconds...")

# Delay so you have time to switch from VS Code to Chrome.
pyautogui.sleep(5)

# Capture the whole screen and save it as an image.
shot = pyautogui.screenshot()
shot.save("logs/calibration_screen.png")

print("Saved logs/calibration_screen.png")
print("Size:", shot.size)   # should equal the screen size from check_setup.py