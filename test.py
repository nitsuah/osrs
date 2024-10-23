import winsound
import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import pytesseract
import subprocess
import random
import time
import keyboard
import os  # Import os for directory handling

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
check_chat_threshold = 15  # Check chat after every 15 clicks
screenshot_directory = "questions"  # Directory to store screenshots

# Create the screenshot directory if it doesn't exist
os.makedirs(screenshot_directory, exist_ok=True)

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
    for _ in range(50):  # Number of scroll steps
        pyautogui.scroll(200)  # Adjust this value for faster zooming
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

    # Check for the anti-bot prompt
    if "hello" in chat_text.lower() and "please answer this question" in chat_text.lower():
        question = extract_question(chat_text)
        if question:
            respond_to_question(question)

    return chat_text 

def extract_question(chat_text):
    """Extract the question from the chat text."""
    # Check for the specific prompt indicating a question is being asked
    if "you may be teleported away" in chat_text.lower():
        start_index = chat_text.find(":") + 1  # Find where the question starts
        question = chat_text[start_index:].strip()  # Extract the question
        return question
    return None

def respond_to_question(question):
    """Log the response to the given question and simulate typing it."""
    # For now, let's log what we would respond
    response = "bald"  # Example response, replace with logic as needed

    # Log the response
    print(f"Detected question: '{question}'")
    print(f"Would respond with: '{response}'")

    # Simulate pressing the space bar, typing the response, and pressing enter
    pyautogui.press('space')  # Press space to activate the chat input
    time.sleep(0.5)  # Brief pause to ensure the input is active

    # Simulate typing the response
    pyautogui.typewrite(response)
    # Play a sound to alert the user
    winsound.Beep(1000, 500)  # Frequency (Hz) and duration (ms)

    # Pause the script to wait for handler input
    input("Press Enter to continue...")

    # pyautogui.press('enter')  # Press enter to send the response
    # print("Simulated response sent.")

def save_screenshot(chat_region):
    """Save a screenshot of the chat region."""
    screenshot_path = os.path.join(screenshot_directory, f"question_{time.strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(screenshot_path, chat_region)  # Save the screenshot
    print(f"Saved screenshot: {screenshot_path}")

def click_with_variance(x, y):
    """Click at a given position with a small random variance.""" 
    variance = 5  # Change this value for more or less variance
    x += random.randint(-variance, variance)
    y += random.randint(-variance, variance)
    pyautogui.click(x, y)
    print(f"Clicked at: ({x}, {y})")

def thieve_from_stall(chat_text):
    """Determine actions based on the chat messages."""
    if "your inventory is full" in chat_text.lower():
        click_with_variance(*inventory_slots[0])  # Click first slot
        time.sleep(0.5)
        return True  # Action completed

    elif "you need to empty your coin pouch" in chat_text.lower():
        click_with_variance(*inventory_slots[0])  # Click first slot
        time.sleep(0.5)
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
    global click_counter
    global check_chat_threshold
    if not check_tesseract_version():
        print("Exiting due to Tesseract installation issue.")
        return

    screen_width, screen_height = pyautogui.size()

    find_and_click_compass()
    hold_up_arrow(duration=3)  # Hold up arrow after clicking the compass
    check_and_zoom_in()  # Ensure camera is zoomed in

    # Click the first inventory slot to reset
    click_with_variance(*inventory_slots[0])
    time.sleep(0.5)

    # Set up the keyboard listener for Shift + Space
    keyboard.add_hotkey('shift+space', toggle_running_state)

    while True:  # Main loop
        if running:  # Only run if the script is active
            click_with_variance(*stall_position)  # Click stall to thieve
            click_counter += 1  # Increment click counter

            # Check chat every 15 clicks or when a specific prompt is encountered
            if click_counter >= check_chat_threshold or random.randint(1, 10) == 1:
                screen_np = capture_screen()  # Capture the screen to check for chat
                chat_text = capture_and_process_chat(screen_np)  # Process chat with updated coordinates
                
                # If a question prompt is detected, save a screenshot of the chat area
                if "you may be teleported away" in chat_text.lower():
                    # Capture and save the chat region for later analysis
                    save_screenshot(screen_np[869:985, 0:495])  # Save screenshot of the chat region

                thieve_from_stall(chat_text)  # Perform action based on chat feedback
                click_counter = 0  # Reset click counter after checking chat

        time.sleep(0.5)  # Delay between loops to prevent spamming

if __name__ == "__main__":
    main()
