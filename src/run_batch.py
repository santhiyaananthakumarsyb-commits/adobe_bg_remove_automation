"""
run_batch.py
------------
PURPOSE:
    Opens Firefly in a new Chrome tab, then processes the images in the
    input folder one at a time:
    upload -> remove background -> apply -> download -> save to output/
    -> Edit new (reset) -> next image.
    Finished images are remembered in logs/done.txt, so a restart
    CONTINUES where the last run stopped instead of starting at image 1.

HOW TO RUN (from the project root):
    python src/run_batch.py
        Uses the folders set in src/config.py.
    python src/run_batch.py --input "D:\\Work\\bags" --output "D:\\Work\\done"
        Uses the folders you give (quote paths that contain spaces).
    python src/run_batch.py --fresh
        Start again from image 1 (clears logs/done.txt).
    python src/run_batch.py 2
        Process only the next 2 images (for testing).
    Options can be combined. Switch to Chrome (any normal page) within
    5 seconds. Do not click other tabs while it runs.

HOW TO STOP:
    1. Move the mouse to the TOP-LEFT corner of the screen (stops at once).
    2. Or create the file logs\\STOP  (stops AFTER the current image):
           New-Item logs\\STOP
    3. Or press Ctrl+C in the terminal (only works if it has focus).
    An interrupted image is NOT marked done, so it runs again.

NOTE:
    done.txt stores image names only. If you switch to a different input
    folder, add --fresh so old names do not cause images to be skipped.

OUTPUT:
    Processed PNGs in the output folder, logs/batch_log.csv, logs/done.txt
"""
import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

import pyautogui

sys.path.insert(0, str(Path(__file__).resolve().parent))
import workflow
from config import PROJECT_ROOT, INPUT_DIR, OUTPUT_DIR
from image_list import get_images

pyautogui.FAILSAFE = True   # mouse to top-left corner = abort

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "batch_log.csv"    # history of every attempt
DONE_FILE = LOG_DIR / "done.txt"        # names of finished input images
STOP_FILE = LOG_DIR / "STOP"            # create this file to stop


def log(name, status, detail=""):
    """Append one row to logs/batch_log.csv."""
    new = not LOG_FILE.exists()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "image", "status", "detail"])
        w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    name, status, detail])


def load_done():
    """Names of images already finished in earlier runs."""
    if not DONE_FILE.exists():
        return set()
    return {line.strip() for line in
            DONE_FILE.read_text(encoding="utf-8").splitlines() if line.strip()}


def mark_done(name):
    """Remember a finished image (written at once, so a stop cannot lose it)."""
    with open(DONE_FILE, "a", encoding="utf-8") as f:
        f.write(name + "\n")


def parse_args():
    p = argparse.ArgumentParser(description="Firefly background-removal batch")
    p.add_argument("--input", help="folder with the images to process")
    p.add_argument("--output", help="folder for the finished PNG files")
    p.add_argument("--fresh", action="store_true",
                   help="ignore earlier progress and start from image 1")
    p.add_argument("limit", nargs="?", type=int,
                   help="process only this many images (for testing)")
    return p.parse_args()


def main():
    args = parse_args()

    input_dir = Path(args.input) if args.input else INPUT_DIR
    output_dir = Path(args.output) if args.output else OUTPUT_DIR

    if not input_dir.is_dir():
        sys.exit(f"Input folder not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # workflow.py saves into workflow.OUTPUT_DIR, so point it at our folder
    workflow.OUTPUT_DIR = output_dir

    print("Input folder :", input_dir)
    print("Output folder:", output_dir)

    if args.fresh and DONE_FILE.exists():
        DONE_FILE.unlink()
        print("Fresh start: progress cleared.")
    if STOP_FILE.exists():
        STOP_FILE.unlink()          # remove a leftover stop request

    all_images = get_images(input_dir)
    if not all_images:
        sys.exit("No images found in the input folder")

    done = load_done()
    pending = [p for p in all_images if p.name not in done]
    if not pending:
        sys.exit("All images are already done. Use --fresh to start again.")
    if args.limit:
        pending = pending[:args.limit]

    total = len(all_images)
    print(f"{total} image(s) in input, {len(done)} already done, "
          f"{len(pending)} to process now")
    print("Switch to Chrome (any normal page). Starting in 5 seconds...")
    time.sleep(5)

    # Open Firefly in a new tab and wait for the empty editor (Upload)
    if not workflow.open_firefly():
        sys.exit("Could not open Firefly. Check internet and Adobe login.")

    ok_count, failed = 0, []
    stopped = False
    try:
        for i, img in enumerate(pending, 1):
            if STOP_FILE.exists():
                print("\nSTOP file found. Stopping before", img.name)
                stopped = True
                break

            position = total - len(pending) + i      # place in the whole list
            print(f"\n[{position}/{total}] {img.name}")
            try:
                dest = workflow.process_one(img)
            except Exception as e:           # includes the fail-safe abort
                print("  ERROR:", e)
                log(img.name, "ERROR", str(e))
                failed.append(img.name)
                if "FailSafe" in type(e).__name__:
                    stopped = True
                    break
                dest = None

            if dest:
                ok_count += 1
                mark_done(img.name)          # remembered for the next start
                log(img.name, "OK", dest.name)
            elif img.name not in failed:
                failed.append(img.name)
                log(img.name, "FAILED", "see terminal output")

            # Back to the empty editor for the next image
            if i < len(pending):
                if not workflow.reset_editor():
                    print("Could not reset the editor. Stopping the batch.")
                    log(img.name, "STOP", "reset failed")
                    stopped = True
                    break
    except KeyboardInterrupt:
        print("\nStopped with Ctrl+C.")
        stopped = True
    finally:
        workflow.close_firefly()     # runs even if the batch stops early

    left = len([p for p in all_images if p.name not in load_done()])
    print(f"\n{'STOPPED' if stopped else 'DONE'}. "
          f"OK this run: {ok_count}   Failed: {len(failed)}   "
          f"Still to do: {left}")
    for name in failed:
        print("  failed:", name)
    if left:
        print("Run the same command again to continue.")


main()