"""
test_expand.py
--------------
PURPOSE:
    Tests whether the labeled 'remove_background' template is found after
    moving the mouse onto the left panel (so it expands).
    Does NOT click anything.

HOW TO RUN (from the project root):
    python tests/test_expand.py
    Switch to Chrome within 5 seconds (image loaded, Apply already clicked).
"""
import sys
sys.path.insert(0, "src")

import pyautogui
import detector

print("Switch to Chrome. Testing in 5 seconds...")
pyautogui.sleep(5)

# 1) Mouse away: panel should be collapsed
pyautogui.moveTo(*detector.NEUTRAL_SPOT)
pyautogui.sleep(1.5)
print("Mouse away :", detector.locate("remove_background") or "not found")

# 2) Mouse onto the panel (a neutral spot on it, not on the button): expands
pyautogui.moveTo(60, 400, duration=0.4)
pyautogui.sleep(1.5)
print("Mouse on panel:", detector.locate("remove_background") or "not found")