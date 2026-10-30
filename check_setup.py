import sys
import cv2
import numpy as np
import pyautogui
from PIL import Image

print("Python:", sys.version.split()[0])
print("OpenCV:", cv2.__version__)
print("NumPy:", np.__version__)
print("PyAutoGUI:", pyautogui.__version__)
print("Screen size:", pyautogui.size())
print("Mouse position:", pyautogui.position())