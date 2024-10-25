import os
import random
import time
import json
import configparser
import logging
import subprocess
import winsound
import keyboard
import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import pytesseract
from textblob import TextBlob

# Create a ConfigParser instance to read configuration
config = configparser.ConfigParser()

# Path to the config file in the parent directory
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')

# Read the configuration, exit if not found
if not os.path.exists(config_path):
    print(f"Error: Config file not found at {config_path}")
    exit(1)

config.read(config_path)

# Configure logging
log_file = config.get('logging', 'log_file')
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Specify the Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = config.get('tesseract', 'path')

# Read coordinates from config
inventory_icon = tuple(map(int, config.get('coordinates', 'inventory_icon').split(',')))
inventory_slots = [
    tuple(map(int, config.get('coordinates', 'inventory_slot_1').split(','))),
    tuple(map(int, config.get('coordinates', 'inventory_slot_2').split(','))),
]
stall_position = tuple(map(int, config.get('coordinates', 'stall_position').split(',')))
chat_region = tuple(map(int, config.get('coordinates', 'chat_region').split(',')))

# Global flags
RUNNING = True
CLICK_COUNTER = 0
CHECK_CHAT_THRESHOLD = 20
SCREENSHOT_DIRECTORY = ".//bot//questions"
PAUSE_THIEVING = False  # Pause functionality
IS_INVENTORY_FULL = False  # Track inventory status

# Create the screenshot directory if it doesn't exist
os.makedirs(SCREENSHOT_DIRECTORY, exist_ok=True)

# Load question-response pairs from JSON file
questions_file_path = os.path.join(os.path.dirname(__file__), 'questions.json')

def load_question_responses():
    """Load question-response pairs from a JSON file."""
    question_response_dict = {}
    try:
        if os.path.exists(questions_file_path):
            with open(questions_file_path, 'r', encoding='utf-8') as file:
                logging.info("Loading questions from %s", questions_file_path)
                question_response_dict = json.load(file)
                logging.info("Loaded %d question-response pairs.", len(question_response_dict))
        else:
            logging.error("Questions file not found at %s", questions_file_path)
    except FileNotFoundError:
        logging.error("Questions file not found at %s", questions_file_path)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from questions file.")
    return question_response_dict

# Load the question-response dictionary
question_responses = load_question_responses()

def log_thieving_action(action):
    """Log actions taken during thieving."""
    logging.info(action)

def click_with_variance(x, y, variance=5):
    """Click at the specified coordinates with a random variance."""
    x += random.randint(-variance, variance)
    y += random.randint(-variance, variance)
    logging.debug("Clicking at (%d, %d) with variance of %d", x, y, variance)
    pyautogui.click(x, y)

def capture_screen():
    """Capture the screen and return it as a NumPy array."""
    try:
        screen = ImageGrab.grab()
        screen_np = np.array(screen)
        logging.info("Screen captured successfully.")
        return cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
    except OSError as e:
        logging.error("Error capturing screen: %s", e)
        return None

def capture_and_process_chat(screen_np):
    """Extract chat text from the captured screen image."""
    if screen_np is None:
        logging.warning("No screen image to process.")
        return ""

    chat_image = screen_np[chat_region[0]:chat_region[1], chat_region[2]:chat_region[3]]

    if chat_image.size == 0:
        logging.warning("Captured chat image is empty.")
        return ""

    chat_text = pytesseract.image_to_string(chat_image)
    logging.info("Extracted chat text: '%s'", chat_text)
    return chat_text, chat_image  # Return chat text and image

def save_screenshot(chat_image):
    """Save a screenshot of the chat region."""
    try:
        screenshot_path = os.path.join(SCREENSHOT_DIRECTORY, f"question_{time.strftime('%Y%m%d_%H%M%S')}.png")
        cv2.imwrite(screenshot_path, chat_image)  # Save the screenshot
        logging.info("Saved screenshot: %s", screenshot_path)
    except IOError as e:
        logging.error("Error saving screenshot: %s", e)

def extract_question(chat_text, chat_image):
    """Extract the question from the chat text."""
    if "you may be teleported away" in chat_text.lower():
        start_index = chat_text.find(":") + 1
        question = chat_text[start_index:].strip()
        logging.info("Extracted question: '%s'", question)
        return question
    return None

def clean_question(question):
    """Clean the extracted question for processing."""
    cleaned_question = question.lower().replace("click here to continue", "").strip()
    logging.info("Cleaned question: '%s'", cleaned_question)
    return cleaned_question

def correct_text(text):
    """Correct the extracted text using TextBlob."""
    blob = TextBlob(text)
    corrected = str(blob.correct())
    logging.info("Corrected text: '%s'", corrected)
    return corrected

def lookup_response(question):
    """Look up the appropriate response for the cleaned question."""
    cleaned_question = clean_question(question)

    # Log the cleaned question for debugging
    logging.info("Looking up response for cleaned question: '%s'", cleaned_question)

    for entry in question_responses['questions']:
        # Check if the question matches or if the keyword is present in the cleaned question
        if cleaned_question.lower() == entry['question'].lower() or entry['keyword'].lower() in cleaned_question.lower():
            logging.info("Question matched: '%s' -> '%s'", cleaned_question, entry['answer'])
            return entry['answer']

    logging.info("No match found for question: '%s'", cleaned_question)
    return "bald"  # Return a default response if no match is found

def respond_to_question(question, chat_image):
    """Respond to the detected question in chat."""
    response = lookup_response(question)
    response = correct_text(response)

    print(f"Detected question: '{question}'")
    print(f"Responding with: '{response}'")

    if response == "bald":
        winsound.Beep(1000, 500)
        # Take a screenshot when a NEW question is detected
        save_screenshot(chat_image)
        input("Press Enter to continue...")
    else:
        winsound.Beep(1000, 500)
        pyautogui.press('space')
        time.sleep(0.5)
        pyautogui.typewrite(response)
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        log_thieving_action(f"Responded to question: '{question}' with: '{response}' successfully!")
    # Reset inventory state after responding
    global IS_INVENTORY_FULL
    IS_INVENTORY_FULL = False
    log_thieving_action("Restarting thieving...")

def check_tesseract_version():
    """Check the Tesseract version to ensure it's correctly installed."""
    try:
        version_output = subprocess.check_output([pytesseract.pytesseract.tesseract_cmd, '--version'])
        logging.info("Tesseract version: %s", version_output.decode().strip())
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Error checking Tesseract version: %s", e)
        return False

def thieve_from_stall(chat_text):
    """Attempt to thieve from the stall based on chat text."""
    global CLICK_COUNTER, IS_INVENTORY_FULL

    if "your inventory is full" in chat_text.lower() and not IS_INVENTORY_FULL:
        logging.info("Detected full inventory. Clearing the first slot.")
        click_with_variance(*inventory_slots[0], variance=0)  # No variance for inventory clicks
        time.sleep(0.5)
        log_thieving_action("Clicked the first inventory slot due to full inventory.")
        IS_INVENTORY_FULL = True
        return True

    elif "you need to empty your coin pouch" in chat_text.lower() and not IS_INVENTORY_FULL:
        logging.info("Detected full coin pouch. Clearing pouch.")
        click_with_variance(*inventory_slots[0], variance=0)  # No variance for inventory clicks
        time.sleep(0.5)
        log_thieving_action("Clicked the first inventory slot due to coin pouch being full.")
        IS_INVENTORY_FULL = True
        return True
    IS_INVENTORY_FULL = False  # Reset state if inventory is no longer full

    logging.info("Attempting to thieve from stall.")
    click_with_variance(*stall_position)
    log_thieving_action("Attempted to thieve from stall.")
    return False

def handle_user_input():
    """Main function to pause the thieving bot.""" 
    global PAUSE_THIEVING  # Access the global pause variable
    if keyboard.is_pressed('left shift'):  # Check for Left Ctrl key press
        print("Pause state toggled.")
        PAUSE_THIEVING = not PAUSE_THIEVING
        logging.info("Pause state toggled: %s", 'Paused' if PAUSE_THIEVING else 'Running')
        time.sleep(1)  # Add a short sleep to prevent rapid toggling

def main():
    """Main function to start the thieving bot.""" 
    global CLICK_COUNTER  # Declare CLICK_COUNTER as global

    logging.info("Thieving bot started.")

    # Check Tesseract version at the start
    if not check_tesseract_version():
        return  # Exit if Tesseract is not found

    while RUNNING:
        if PAUSE_THIEVING:
            print("Bot is paused. Waiting for unpause...")
            logging.info("Bot paused.")
            time.sleep(1)
            handle_user_input()  # Check for pause/unpause input
            continue

        handle_user_input()  # Check for pause/unpause input

        screen_np = capture_screen()  # Capture the screen
        if screen_np is None:
            continue  # Skip processing if screen capture failed

        chat_text, chat_image = capture_and_process_chat(screen_np)  # Extract chat text

        if not chat_text:
            continue  # Skip if no text was extracted

        if "you may be teleported away" in chat_text.lower():
            question = extract_question(chat_text, chat_image)
            if question:
                respond_to_question(question, chat_image)
        thieve_from_stall(chat_text)  # Handle thieving actions
        CLICK_COUNTER += 1

        # Rest between actions to avoid bot-like behavior
        time.sleep(random.uniform(0.5, 1.0))

if __name__ == "__main__":
    main()
