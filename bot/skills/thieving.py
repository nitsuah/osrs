import pyautogui
import time

def thieve_from_stall(coordinates):
    """Thieve from the stall at the specified coordinates."""
    pyautogui.click(coordinates[0], coordinates[1])
    time.sleep(1)
