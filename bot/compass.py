import time
import pyautogui
import logging

def click_compass(compass_position):
    """Clicks the compass to reset the camera orientation."""
    pyautogui.click(*compass_position)
    logging.info(f"Clicked compass at: {compass_position}")
    time.sleep(1)  # Allow some time for the camera to adjust
