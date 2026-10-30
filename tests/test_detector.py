"""
test_detector.py
----------------
PURPOSE:
    Checks locate() for all four templates against the CURRENT screen.
    Does NOT click anything.

HOW TO RUN (from the project root):
    python tests/test_detector.py
    Then switch to Chrome within 5 seconds.

EXPECTED RESULT (editor with image loaded, Apply already clicked):
    remove_background  FOUND
    download           FOUND
    upload             not found   (only on the empty editor)
    apply              not found   (only during the preview)
    Seeing "not found" for the last two proves the detector doesn't give
    false matches.
"""

import sys
sys.path.insert(0, "src")   # lets us import src/detector.py

import pyautogui
import detector

print("Switch to Chrome. Testing in 5 seconds...")
pyautogui.sleep(5)
pyautogui.moveTo(*detector.NEUTRAL_SPOT)
pyautogui.sleep(0.5)

for name in ["upload", "remove_background", "apply", "download"]:
    point = detector.locate(name)
    print(f"{name:18} {'FOUND at ' + str(point) if point else 'not found'}")