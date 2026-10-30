"""
workflow.py
-----------
PURPOSE:
    The manual Firefly steps as Python functions, one function per step.
    Each function returns True/False (or a Path/None) so the caller can
    stop or skip an image when something fails.

FUNCTIONS:
    open_firefly()                 Open Firefly in a new Chrome tab and wait
                                   until the empty editor (Upload) shows.
    upload_image(path)             Manual steps 1-3: click Upload, paste the
                                   file path in the Open dialog, press Enter,
                                   wait until the image has loaded.
    remove_background_and_apply()  Manual steps 4-5: click Remove background,
                                   wait for the preview, click Apply.
    download_and_save(path)        Manual steps 6-7: click Download, wait for
                                   the new file in Downloads, rename it to
                                   <input name>.png, move it to OUTPUT_DIR,
                                   close Chrome's download panel.
    reset_editor()                 Click Edit new, wait for Upload.
    process_one(path)              All steps for ONE image.
    close_firefly()                Close the current tab (Ctrl+W).

REQUIRES:
    detector.py, config.py, and the templates in templates/
    (upload, remove_background, apply, download, edit_new).
"""
import shutil
import time
from pathlib import Path

import pyautogui
import pyperclip
import pygetwindow as gw

import detector
from config import OUTPUT_DIR

DOWNLOADS = Path.home() / "Downloads"   # where Chrome saves downloads
FIREFLY_URL = "https://firefly.adobe.com/image-editor"


# ------------------------------------------------------- open / close tab
def open_firefly():
    """Open Firefly in a NEW tab of the current Chrome window and wait
    until the empty editor (Upload) is visible."""
    pyautogui.hotkey("ctrl", "t")          # new tab, address bar focused
    time.sleep(1)
    pyperclip.copy(FIREFLY_URL)
    pyautogui.hotkey("ctrl", "v")          # paste the address
    pyautogui.press("enter")
    if detector.wait_for("upload", timeout=60) is None:
        print("[workflow] Firefly did not load (Upload not found)")
        return False
    print("[workflow] Firefly opened")
    return True


def close_firefly():
    """Close the current tab (the Firefly tab we opened)."""
    pyautogui.hotkey("ctrl", "w")
    print("[workflow] Firefly tab closed")


# ---------------------------------------------------------------- upload
def _wait_for_open_dialog(timeout=10):
    """Wait for the Windows 'Open' file dialog to appear."""
    end = time.time() + timeout
    while time.time() < end:
        if [w for w in gw.getAllWindows() if w.title == "Open"]:
            return True
        time.sleep(0.3)
    return False


def upload_image(image_path):
    """Steps 1 to 3. The EMPTY editor (Upload visible) must be showing."""
    # Step 1: click Upload
    if not detector.click("upload", timeout=10):
        return False

    # Step 2: wait for the Open dialog
    if not _wait_for_open_dialog():
        print("[workflow] Open dialog did not appear")
        return False
    time.sleep(0.5)

    # Step 3: paste the full path into File name, press Enter (= Open)
    pyperclip.copy(str(image_path))
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)
    pyautogui.press("enter")

    # Download turns white only once an image is loaded
    # (greyed out on the empty editor, so it does not match there).
    if detector.wait_for("download", timeout=30) is None:
        print("[workflow] image did not load (Download not active)")
        return False

    print(f"[workflow] uploaded: {image_path}")
    return True


# ------------------------------------------------- remove background + apply
def remove_background_and_apply():
    """Steps 4 and 5. The image must already be loaded."""
    # Step 4: click Remove background
    if not detector.click("remove_background", timeout=15):
        return False

    # Processing takes a few seconds; Apply appears when the preview is ready
    if detector.wait_for("apply", timeout=60) is None:
        print("[workflow] Apply never appeared (processing failed?)")
        return False

    # Step 5: click Apply, then wait for the Apply/Cancel bar to disappear
    if not detector.click("apply", timeout=10):
        return False
    if not detector.wait_gone("apply", timeout=15):
        print("[workflow] Apply bar did not close")
        return False

    print("[workflow] background removed and applied")
    return True


# ------------------------------------------------------ download + save
def _wait_new_download(before, timeout=60):
    """Wait for a NEW finished file in Downloads (ignores .crdownload).
    Returns the Path once its size stops changing, or None on timeout."""
    end = time.time() + timeout
    while time.time() < end:
        new = [p for p in DOWNLOADS.iterdir()
               if p.name not in before
               and p.suffix.lower() not in (".crdownload", ".tmp")]
        if new:
            f = max(new, key=lambda p: p.stat().st_mtime)
            size1 = f.stat().st_size
            time.sleep(1)
            if f.exists() and size1 > 0 and f.stat().st_size == size1:
                return f
        time.sleep(0.5)
    return None


def download_and_save(image_path):
    """Steps 6 and 7. Apply must be done and Download must be white.
    Returns the final Path in OUTPUT_DIR, or None on failure."""
    before = {p.name for p in DOWNLOADS.iterdir()}

    # Step 6: click Download (Chrome saves straight to Downloads)
    if not detector.click("download", timeout=10):
        return None

    f = _wait_new_download(before)
    if f is None:
        print("[workflow] no new file appeared in Downloads")
        return None

    # Step 7: name the output after the input; never overwrite a file
    stem = Path(image_path).stem
    dest = OUTPUT_DIR / f"{stem}.png"
    n = 1
    while dest.exists():
        dest = OUTPUT_DIR / f"{stem}_{n}.png"
        n += 1
    shutil.move(str(f), str(dest))
    print(f"[workflow] saved: {dest}")

    # Close Chrome's download panel so it cannot hide the Download button
    time.sleep(1)
    pyautogui.press("esc")
    if detector.wait_for("download", timeout=10) is None:
        print("[workflow] WARNING: Download button not visible after Esc")

    return dest


# ------------------------------------------------------------------ reset
def reset_editor():
    """Return to the EMPTY editor (Upload visible) for the next image.
    Clicks 'Edit new', then waits for Upload to appear."""
    if not detector.click("edit_new", timeout=10):
        return False
    if detector.wait_for("upload", timeout=15) is None:
        print("[workflow] Upload did not appear after Edit new")
        return False
    print("[workflow] editor reset")
    return True


# ------------------------------------------------------------ one image
def process_one(image_path):
    """All steps for one image. Start from the EMPTY editor.
    Returns the output Path, or None if any step failed."""
    if not upload_image(image_path):
        return None
    if not remove_background_and_apply():
        return None
    return download_and_save(image_path)