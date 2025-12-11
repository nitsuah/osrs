import time
import pyautogui
import logging


def click_compass(compass_position: tuple[int, int]) -> None:
    """Click the compass to reset the camera orientation."""
    pyautogui.click(*compass_position)
    logging.info("Clicked compass at: %s", compass_position)
    time.sleep(1)
