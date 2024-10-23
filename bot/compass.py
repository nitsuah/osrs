import pyautogui
import time

def click_compass(coordinates):
    pyautogui.click(coordinates[0], coordinates[1])
    time.sleep(0.5)
