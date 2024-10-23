import pyautogui
import time

def zoom_camera(steps):
    for _ in range(steps):
        pyautogui.scroll(-1)  # Zoom in
        time.sleep(0.1)
