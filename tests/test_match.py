"""
test_match.py
-------------
PURPOSE:
    Checks that a saved template can be found on the live screen.
    Prints the match confidence and the center point, then MOVES the mouse
    there. It does NOT click.

WHEN TO USE:
    - Right after capturing a new template (Milestone 3)
    - When a button stops being detected, to see the confidence score

HOW TO RUN (from the project root):
    python src/test_match.py upload
    Then switch to Chrome within 5 seconds (button must be visible).

HOW TO READ THE RESULT:
    confidence close to 1.00 = excellent match
    confidence above 0.80    = usable
    confidence below 0.80    = template not found or screen looks different
"""

import sys
import cv2
import numpy as np
import pyautogui

if len(sys.argv) != 2:
    print("Usage: python src/test_match.py <template_name>")
    sys.exit(1)

name = sys.argv[1]

# Load the template image saved earlier (OpenCV reads it as BGR).
template = cv2.imread(f"templates/{name}.png")
if template is None:
    print(f"Template not found: templates/{name}.png")
    sys.exit(1)

th, tw = template.shape[:2]   # template height and width

print("Switch to Chrome. Searching in 5 seconds...")
pyautogui.sleep(5)

# Take a screenshot and convert it from RGB (Pillow) to BGR (OpenCV).
screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

# Slide the template over the screen and score every position.
result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

# Find the best score and where it happened (top-left corner).
_, max_val, _, max_loc = cv2.minMaxLoc(result)

# Center of the matched area = the point we would click.
cx = max_loc[0] + tw // 2
cy = max_loc[1] + th // 2

print(f"Confidence: {max_val:.3f}")
print(f"Match center: ({cx}, {cy})")

# Move the mouse there so you can see where it landed. No click.
pyautogui.moveTo(cx, cy, duration=0.5)