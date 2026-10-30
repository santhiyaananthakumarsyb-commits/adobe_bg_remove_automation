"""
detector.py
-----------
PURPOSE:
    Reusable functions to find buttons on screen with OpenCV template
    matching, wait for them, and click them. Every workflow script
    imports this file.

FUNCTIONS:
    locate(name, threshold, region) -> (x, y) center of the button or None
    wait_for(name, timeout)         -> (x, y) once visible, or None on timeout
    wait_gone(name, timeout)        -> True once the button disappears
    click(name, timeout)            -> waits, then clicks; True/False

TEMPLATES:
    Loaded from templates/<name>.png
    (upload, remove_background, apply, download).

TUNING:
    THRESHOLD = minimum confidence to accept a match.
    Our templates scored 0.985 to 1.000, so 0.90 is safe.
"""
import time
import cv2
import numpy as np
import pyautogui

THRESHOLD = 0.90             # minimum match confidence (0 to 1)
NEUTRAL_SPOT = (1000, 100)   # mouse parks here so no button shows a hover look

_cache = {}                  # templates are loaded once and reused


def _load(name):
    """Read templates/<name>.png once and keep it in memory."""
    if name not in _cache:
        img = cv2.imread(f"templates/{name}.png")
        if img is None:
            raise FileNotFoundError(f"templates/{name}.png not found")
        _cache[name] = img
    return _cache[name]


def locate(name, threshold=THRESHOLD, region=None):
    """Take one screenshot and search for the template.
    region = (left, top, width, height) limits the search area.
    Returns (x, y) of the button center in FULL-SCREEN coordinates,
    or None if not found."""
    template = _load(name)
    th, tw = template.shape[:2]

    screen = cv2.cvtColor(np.array(pyautogui.screenshot(region=region)),
                          cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    ox, oy = (region[0], region[1]) if region else (0, 0)
    return (ox + max_loc[0] + tw // 2, oy + max_loc[1] + th // 2)


def wait_for(name, timeout=15, interval=0.5, threshold=THRESHOLD):
    """Keep searching until the button appears or the timeout ends.
    Better than a blind sleep: continues as soon as the button shows."""
    pyautogui.moveTo(*NEUTRAL_SPOT)   # avoid hover effects
    end = time.time() + timeout
    while time.time() < end:
        point = locate(name, threshold)
        if point:
            return point
        time.sleep(interval)
    return None


def wait_gone(name, timeout=15, interval=0.5, threshold=THRESHOLD):
    """Wait until the template is NO LONGER on screen.
    Returns True when it disappears, False on timeout."""
    end = time.time() + timeout
    while time.time() < end:
        if locate(name, threshold) is None:
            return True
        time.sleep(interval)
    return False


def click(name, timeout=15):
    """Wait for the button, then click its center. Returns True if clicked."""
    point = wait_for(name, timeout)
    if point is None:
        print(f"[detector] '{name}' not found within {timeout}s")
        return False
    pyautogui.click(point[0], point[1])
    print(f"[detector] clicked '{name}' at {point}")
    return True