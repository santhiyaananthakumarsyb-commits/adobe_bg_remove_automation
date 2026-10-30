# Firefly Background Remover Automation

Python tool that automates background removal in Adobe Firefly's image
editor (Chrome, Windows) using screen automation. It uses OpenCV template
matching to find buttons and PyAutoGUI to click them, then processes a
whole folder of images one by one.

> **Check before using:** automating a web service may be restricted by its
> terms of use. Confirm that Adobe allows this for your account.

## What it does

For each image in the input folder:

1. Opens Firefly in a new Chrome tab
2. Upload: pastes the full image path into the Windows Open dialog
3. Remove background, then Apply
4. Download, then renames the file to `<input name>.png` and moves it to the output folder
5. Edit new (reset), then the next image
6. Closes the Firefly tab when finished

Features: resume after a stop, per-image logging, skip-on-failure,
custom input/output folders from the command line, emergency stop.

## Requirements

- Windows 10/11
- Python 3.12
- Google Chrome, **maximized**, zoom **100%**, logged in to Adobe Firefly
- Screen **1366 x 768** (the templates were captured at this size)
- Chrome saves downloads to `C:\Users\<you>\Downloads` with no "Save as" prompt

## Setup

```powershell
git clone <your-repo-url>
cd bg_remover
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python check_setup.py
```

`check_setup.py` prints library versions and the screen size.

## Usage

Put images in `input/` (`.png .jpg .jpeg .webp .jfif`), then:

```powershell
# Default folders (set in src/config.py)
python src/run_batch.py

# Custom folders (quote paths that contain spaces)
python src/run_batch.py --input "D:\Work\bags" --output "D:\Work\bags_done"

# Start again from image 1
python src/run_batch.py --fresh

# Process only the next 2 images (for testing)
python src/run_batch.py 2
```

After starting, switch to Chrome (any normal page) within 5 seconds.
**Do not touch the mouse, keyboard or browser tabs while it runs.**

### Stop and resume

| Method | Effect |
|---|---|
| Move mouse to the **top-left corner** | Stops immediately |
| `New-Item logs\STOP` (second terminal) | Stops after the current image |
| `Ctrl+C` in the terminal | Only works if the terminal has focus |

Finished images are remembered in `logs/`. Run the same command again to
continue where it stopped. An interrupted image is not marked done and
runs again. Use `--fresh` to start over.

Output files are never overwritten: if `bag1.png` exists, the next one is
saved as `bag1_1.png`.

## Project structure

```
bg_remover/
├── check_setup.py          verify the environment
├── requirements.txt
├── input/                  images to process
├── output/                 finished PNGs (transparent background)
├── templates/              button images used for matching
├── logs/                   batch_log.csv, progress files (not in git)
├── src/
│   ├── config.py           default input/output folders
│   ├── image_list.py       lists supported images
│   ├── detector.py         OpenCV template matching, wait and click
│   ├── workflow.py         the Firefly steps as functions
│   ├── run_batch.py        folder loop, resume, stop, logging
│   ├── calibrate.py        saves a reference screenshot
│   └── capture_template.py saves a button crop as a template
└── tests/                  small checks for each step
```

## Templates

`templates/` holds cropped button images: `upload`, `remove_background`,
`apply`, `download`, `edit_new`. If Adobe changes the interface, or your
screen differs, recapture them:

```powershell
python src/capture_template.py <name>     # hover the button for 6 seconds
python tests/test_match.py <name>         # expect confidence above 0.90
```

Capture each template in the screen state where it is used (for example
`remove_background` with an image loaded, `apply` during the preview).

## Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| A button is "not found" | Layout changed. Check Chrome zoom 100%, maximized, then recapture that template |
| "All images are already done" | Progress is saved. Use `--fresh` |
| `Firefly did not load` | No internet, not logged in, or a popup is covering the page |
| Image skipped and logged FAILED | See `logs/batch_log.csv`. A limit or error message in Firefly stops that image |
| `No space left on device` | Free disk space or create the project on another drive |

## Known limits

- Tested only on Windows, Chrome, 1366 x 768, 100% scaling
- Firefly limit messages, login screens and unexpected popups are not handled; the image fails and is skipped
- Screen automation is sensitive to layout changes


