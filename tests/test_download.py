"""
test_download.py
----------------
PURPOSE:
    Clicks Download and reports what NEW file appears in the Downloads
    folder (name, size, time). Does NOT move anything yet.

HOW TO RUN (from the project root):
    python tests/test_download.py
    Switch to Chrome within 5 seconds. Apply must already be done and
    Download must be white (active).
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, "src")

import pyautogui
import detector

DOWNLOADS = Path.home() / "Downloads"

before = {p.name for p in DOWNLOADS.iterdir()}
print("Downloads folder:", DOWNLOADS)
print("Files before:", len(before))

print("Switch to Chrome. Starting in 5 seconds...")
pyautogui.sleep(5)

if not detector.click("download", timeout=10):
    sys.exit("Download button not found")

print("Clicked Download. Watching for a new file (30 s)...")
end = time.time() + 30
while time.time() < end:
    new = [p for p in DOWNLOADS.iterdir() if p.name not in before]
    if new:
        for p in new:
            print(f"NEW: {p.name}  {p.stat().st_size} bytes")
    time.sleep(2)
    if new and not any(p.suffix == ".crdownload" for p in new):
        break

print("Done. Take a screenshot of Chrome now.")