import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import pytesseract
import subprocess
import random
import time
import keyboard  # Add this import

# Specify the Tesseract OCR path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordinates for inventory slots and inventory icon
inventory_icon = (1765, 717)
inventory_slots = [(1700 + i * 50, 757) for i in range(28)]  # Adjust x position based on slot spacing
stall_position = (960, 604)  # Position of the stall in front of the character
zoomed_in = False  # Variable to track zoom state

# Global variable to control the script's running state
running = True

# Counter for clicks
click_counter = 0
check_chat_threshold = 20  # Check chat after every 20 clicks

def check_tesseract_version():
    """Check if Tesseract is installed and verify its version."""
    try:
        output = subprocess.check_output([pytesseract.pytesseract.tesseract_cmd, '--version']).decode('utf-8')
        print("Tesseract installed:", output.strip())
        
        version_line = output.splitlines()[0]
        version_number = version_line.split()[1]
        major_version = int(version_number[1])  # Convert to int after removing 'v'
        
        if major_version < 4:
            print("Warning: Tesseract version is less than 4.0. Some features may not work.")
            return False
        return True
    except Exception as e:
        print("An error occurred while checking Tesseract version:", str(e))
        return False

def capture_screen():
    """Capture the full screen and return it as a numpy array."""
    img = ImageGrab.grab()  # Fullscreen capture
    return np.array(img)

def find_and_click_compass():
    """Click the compass directly using known coordinates."""
    compass_x, compass_y = 1740, 44
    pyautogui.click(compass_x, compass_y)
    print(f"Clicked compass at: {compass_x}, {compass_y}")

def hold_up_arrow(duration=3):
    """Hold the up arrow key for a specified duration."""
    pyautogui.keyDown('up')
    time.sleep(duration)
    pyautogui.keyUp('up')
    print(f"Held up arrow for {duration} seconds.")

def zoom_in():
    """Scroll to zoom in quickly."""
    for _ in range(20):  # Number of scroll steps
        pyautogui.scroll(100)  # Adjust this value for faster zooming
        time.sleep(0.05)  # Short sleep to avoid overwhelming the input
    print("Zoomed in fully using scroll wheel.")

def check_and_zoom_in():
    """Ensure the camera is fully zoomed in using the scroll wheel."""
    global zoomed_in
    if not zoomed_in:
        zoom_in()  # Call the zoom function
        zoomed_in = True  # Update zoom state

def capture_and_process_chat(screen_np):
    """Capture the chat region and extract any text using OCR."""
    chat_region = screen_np[869:985, 0:495]  # New chat coordinates (y1:y2, x1:x2)

    gray_chat_region = cv2.cvtColor(chat_region, cv2.COLOR_BGR2GRAY)
    chat_text = pytesseract.image_to_string(gray_chat_region)
    print("Chat Text:", chat_text)

    return chat_text

def click_with_variance(x, y):
    """Click at a given position with a small random variance."""
    variance = 5  # Change this value for more or less variance
    x += random.randint(-variance, variance)
    y += random.randint(-variance, variance)
    pyautogui.click(x, y)
    print(f"Clicked at: ({x}, {y})")

def thieve_from_stall(chat_text):
    """Determine actions based on the chat messages."""
    if "Your inventory is full" in chat_text:
        # Click on the first inventory slot to remove an item
        click_with_variance(*inventory_slots[0])  # Click first slot
        time.sleep(0.5)  # Wait a moment
        return True  # Action completed

    elif "You need to empty your coin pouch" in chat_text:
        # Click on the first inventory slot
        click_with_variance(*inventory_slots[0])  # Click first slot
        time.sleep(0.5)  # Wait a moment
        return True  # Action completed

    # If nothing relevant found, attempt to thieve
    click_with_variance(*stall_position)  # Click the stall to thieve
    print("Attempted to thieve from stall.")
    return False

def toggle_running_state():
    """Toggle the running state of the script."""
    global running
    running = not running  # Toggle running state
    if running:
        print("Script resumed.")
    else:
        print("Script paused.")

def main():
    global click_counter  # Declare click_counter as global
    if not check_tesseract_version():
        print("Exiting due to Tesseract installation issue.")
        return

    screen_width, screen_height = pyautogui.size()

    find_and_click_compass()
    hold_up_arrow(duration=3)  # Hold up arrow after clicking the compass
    check_and_zoom_in()  # Ensure camera is zoomed in

    # Set up the keyboard listener for Shift + Space
    keyboard.add_hotkey('shift+space', toggle_running_state)

    while True:  # Main loop
        if running:  # Only run if the script is active
            screen_np = capture_screen()
            click_with_variance(*stall_position)  # Click stall to thieve
            click_counter += 1  # Increment click counter

            # Check chat every 20 clicks
            if click_counter >= check_chat_threshold:
                chat_text = capture_and_process_chat(screen_np)  # Process chat with updated coordinates
                thieve_from_stall(chat_text)  # Perform action based on chat feedback
                click_counter = 0  # Reset click counter after checking chat

        time.sleep(0.5)  # Delay between loops to prevent spamming

if __name__ == "__main__":
    main()
