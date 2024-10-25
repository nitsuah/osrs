import time
import pyautogui
import keyboard


def check_and_zoom_in(steps):
    """Zoom in using scroll based on the number of steps provided."""
    print(f"Attempting to zoom in with {steps} steps.")  # Log the number of steps
    for _ in range(steps):  # Number of scroll steps
        pyautogui.scroll(200)  # Adjust this value for faster zooming
        time.sleep(0.05)  # Short sleep to avoid overwhelming the input
    print("Zoomed in and tilted up fully.")
    hold_up_arrow(2)  # Hold the up arrow key for 3 seconds

def hold_up_arrow(duration):
    """Holds the up arrow key for a specified duration.""" 
    keyboard.press('up')  # Use string representation for the key
    time.sleep(duration)
    keyboard.release('up')
    print(f"Held the up arrow key for {duration} seconds.")
