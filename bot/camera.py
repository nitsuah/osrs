import time
import logging
import pyautogui
import keyboard


def check_and_zoom_in(steps: int) -> None:
    """Zoom in using scroll based on the number of steps provided."""
    logging.info("Attempting to zoom in with %s steps.", steps)
    for _ in range(steps):
        pyautogui.scroll(200)
        time.sleep(0.05)
    logging.info("Zoomed in and tilted up fully.")
    hold_up_arrow(2)

def hold_up_arrow(duration: int) -> None:
    """Holds the up arrow key for a specified duration."""
    keyboard.press('up')
    time.sleep(duration)
    keyboard.release('up')
    logging.info("Held the up arrow key for %s seconds.", duration)
