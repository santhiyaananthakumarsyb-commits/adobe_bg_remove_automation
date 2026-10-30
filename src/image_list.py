"""
image_list.py
-------------
PURPOSE:
    Returns the list of images in the input folder, sorted by name.
    The batch loop (Milestone 8) takes these one by one.

HOW TO USE:
    from image_list import get_images
    for path in get_images():
        ...
"""
from pathlib import Path
from config import INPUT_DIR

EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".jfif"}


def get_images(folder=INPUT_DIR):
    """Return full paths of all supported images in the folder."""
    return [p.resolve() for p in sorted(Path(folder).iterdir())
            if p.suffix.lower() in EXTENSIONS]