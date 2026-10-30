"""
test_remove_apply.py
--------------------
PURPOSE:
    Tests Steps 4 and 5: click Remove background, wait for the preview,
    click Apply. Stops BEFORE Download.

HOW TO RUN (from the project root):
    python tests/test_remove_apply.py
    Switch to Chrome within 5 seconds. The image must be loaded, with
    "Remove background" visible and NOT yet clicked.
"""
import sys
sys.path.insert(0, "src")

import pyautogui
import workflow

print("Switch to Chrome (image loaded). Starting in 5 seconds...")
pyautogui.sleep(5)

ok = workflow.remove_background_and_apply()
print("RESULT:", "OK" if ok else "FAILED")