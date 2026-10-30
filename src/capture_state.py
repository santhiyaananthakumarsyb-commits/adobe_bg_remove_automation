"""
capture_state.py
----------------
PURPOSE:
    Moves the mouse away from the page, waits, then saves a full
    screenshot to logs/state.png. Shows the screen exactly as the
    detector sees it (e.g. the COLLAPSED left panel).

HOW TO RUN:
    python src/capture_state.py
    Switch to Chrome within 5 seconds (image loaded, Apply already clicked).
"""
import pyautogui
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
print("Switch to Chrome. Capturing in 5 seconds...")
pyautogui.sleep(5)

pyautogui.moveTo(1000, 100)   # far from the left panel
pyautogui.sleep(1.5)          # give the panel time to collapse

pyautogui.screenshot().save("logs/state.png")
print("Saved logs/state.png")