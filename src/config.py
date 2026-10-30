"""
config.py
---------
PURPOSE:
    One place for the input and output folder paths.
    If your senior gives different folders, change ONLY this file.

HOW TO CHANGE:
    Example:  INPUT_DIR = Path(r"D:\Work\bag_images")
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "input"     # images to process
OUTPUT_DIR = PROJECT_ROOT / "output"   # finished images

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)