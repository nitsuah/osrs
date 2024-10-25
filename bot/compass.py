import time
import pyautogui

def click_compass(compass_position):
    """Clicks the compass to reset the camera orientation."""
    pyautogui.click(*compass_position)
    print(f"Clicked compass at: {compass_position}")
    time.sleep(1)  # Allow some time for the camera to adjust
