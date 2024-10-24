import os
import random
import time
import logging
import subprocess
import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import pytesseract
import configparser

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Construct the path to the config file in the parent directory
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')

# Read the configuration
if not os.path.exists(config_path):
    print(f"Error: Config file not found at {config_path}")
    exit(1)

config.read(config_path)

# Configure logging
log_file = config.get('logging', 'log_file')
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Specify the Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = config.get('tesseract', 'path')

# Read coordinates from config
inventory_icon = tuple(map(int, config.get('coordinates', 'inventory_icon').split(',')))
inventory_slots = [
    tuple(map(int, config.get('coordinates', 'inventory_slot_1').split(','))),
    tuple(map(int, config.get('coordinates', 'inventory_slot_2').split(',')))
]
stall_position = tuple(map(int, config.get('coordinates', 'stall_position').split(',')))
chat_region = tuple(map(int, config.get('coordinates', 'chat_region').split(',')))

running = True
click_counter = 0
check_chat_threshold = 15
screenshot_directory = ".//bot//questions"

# Create the screenshot directory if it doesn't exist
os.makedirs(screenshot_directory, exist_ok=True)

def log_thieving_action(action):
    """Log a thieving action."""
    logging.info(action)

def click_with_variance(x, y, variance=5):
    """Click on the given coordinates with some variance."""
    x += random.randint(-variance, variance)
    y += random.randint(-variance, variance)
    pyautogui.click(x, y)

def capture_screen():
    """Capture the screen and return as a NumPy array."""
    screen = ImageGrab.grab()
    screen_np = np.array(screen)
    return cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)

def capture_and_process_chat(screen_np):
    """Capture the chat region and process it with OCR."""
    chat_image = screen_np[chat_region[0]:chat_region[1], chat_region[2]:chat_region[3]]
    chat_text = pytesseract.image_to_string(chat_image)
    return chat_text

def save_screenshot(chat_image):
    """Save a screenshot of the chat region."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_directory, f"chat_screenshot_{timestamp}.png")
    cv2.imwrite(filename, chat_image)
    print(f"Saved screenshot: {filename}")

def check_tesseract_version():
    """Check if Tesseract is installed and available."""
    try:
        version_output = subprocess.check_output([pytesseract.pytesseract.tesseract_cmd, '--version'])
        print(version_output.decode())
        return True
    except Exception as e:
        print(f"Error checking Tesseract version: {e}")
        return False

def thieve_from_stall(chat_text):
    """Determine actions based on the chat messages."""
    if "your inventory is full" in chat_text.lower():
        click_with_variance(*inventory_slots[0])  # Click first slot
        time.sleep(0.5)
        log_thieving_action("Clicked first inventory slot due to full inventory.")
        return True

    elif "you need to empty your coin pouch" in chat_text.lower():
        click_with_variance(*inventory_slots[0])  # Click first slot
        time.sleep(0.5)
        log_thieving_action("Clicked first inventory slot due to coin pouch being full.")
        return True

    # If nothing relevant found, attempt to thieve
    click_with_variance(*stall_position)  # Click the stall to thieve
    log_thieving_action("Attempted to thieve from stall.")
    return False

def main():
    global click_counter  # Declare click_counter as global

    if not check_tesseract_version():
        print("Exiting due to Tesseract installation issue.")
        return

    # Find and click the compass using coordinates from config
    pyautogui.click(*stall_position)
    time.sleep(3)  # Hold the up arrow or perform an action

    # Click the first inventory slot to reset
    click_with_variance(*inventory_slots[0])
    time.sleep(0.5)

    while running:  # Main loop
        click_with_variance(*stall_position)  # Click stall to thieve
        click_counter += 1

        # Check chat every 15 clicks
        if click_counter >= check_chat_threshold or random.randint(1, 10) == 1:
            screen_np = capture_screen()  # Capture the screen to check for chat
            chat_text = capture_and_process_chat(screen_np)

            # Save a screenshot of the chat area
            if "you may be teleported away" in chat_text.lower():
                save_screenshot(screen_np[chat_region[0]:chat_region[1], chat_region[2]:chat_region[3]])
            thieve_from_stall(chat_text)
            click_counter = 0  # Reset click counter

        time.sleep(0.5)  # Delay between loops to prevent spamming

if __name__ == "__main__":
    main()