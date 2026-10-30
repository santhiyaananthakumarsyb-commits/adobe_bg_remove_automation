"""
test_edit_new.py
----------------
PURPOSE:
    Tests reset_editor(): click Edit new and wait for Upload.
    Does not process any image.

HOW TO RUN (from the project root):
    python tests/test_edit_new.py
    Switch to Chrome within 5 seconds, with an image loaded
    (Edit new visible at the top left).
"""
import sys
sys.path.insert(0, "src")

import pyautogui
import workflow

print("Switch to Chrome (image loaded). Starting in 5 seconds...")
pyautogui.sleep(5)

ok = workflow.reset_editor()
print("RESULT:", "OK" if ok else "FAILED")