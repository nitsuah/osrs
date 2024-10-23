import pyautogui
import time

def thieve_from_stall(coordinates):
    pyautogui.click(coordinates[0], coordinates[1])
    time.sleep(1)
    # Add more thieving logic here if needed