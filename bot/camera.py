import time
import pyautogui

def zoom_in():
    """Zoom in quickly by scrolling the mouse wheel."""
    pyautogui.scroll(500)  # Adjust this value to control how much to zoom in at once
    print("Zoomed in fully using scroll wheel.")

def check_and_zoom_in(steps):
    """Zoom in using scroll based on the number of steps provided."""
    print(f"Attempting to zoom in with {steps} steps.")  # Log the number of steps
    for _ in range(steps):  # Number of scroll steps
        pyautogui.scroll(200)  # Adjust this value for faster zooming
        time.sleep(0.05)  # Short sleep to avoid overwhelming the input
    print("Zoomed in fully using scroll wheel.")
