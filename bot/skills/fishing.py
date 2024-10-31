import logging
import time
import winsound
import random
import keyboard
import pyautogui
from bot.config import load_config
from bot.skills.screen_processing import capture_screen, capture_and_process_chat, save_screenshot
from bot.skills.question_handler import load_question_responses, lookup_response, correct_text
from bot.skills.actions import fish_from_spot, click_with_variance
from bot.skills.thieving import respond_to_question

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration
config = load_config("config.ini")

# Debugging line to logging.info the raw value
logging.info("Chat region raw value: %s", config["coordinates"]["chat_region"])

# Strip any comments and handle leading/trailing whitespace
raw_chat_region = config["coordinates"]["chat_region"].split('#')[0].strip()
chat_region = tuple(map(int, raw_chat_region.split(',')))  # (x1, y1, x2, y2)

RUNNING = True
PAUSE_FISHING = False
CLICK_COUNTER = 0

def handle_user_input():
    global PAUSE_FISHING
    if keyboard.is_pressed('f1'):
        winsound.Beep(1000, 500)
        PAUSE_FISHING = not PAUSE_FISHING
        time.sleep(1)


def Fish():
    logging.info("Starting the Fishing bot...")

    global CLICK_COUNTER
    while RUNNING:
        if PAUSE_FISHING:
            time.sleep(1)
            handle_user_input()
            continue

        handle_user_input()

        screen_np = capture_screen()
        if screen_np is None:
            continue
        # Pass the chat region to the capture function
        chat_text, chat_image = capture_and_process_chat(screen_np, chat_region)   
        # Check if a question prompt needs a response
        if "teleported" in chat_text.lower():
            logging.info("Question prompt detected.")
            if ":" in chat_text:
                question = chat_text.split(":", 1)[1].strip()
            else:
                question = chat_text.strip()  # Fallback if no colon is found
            logging.info("Responding to question...")
            respond_to_question(question, chat_image)
            time.sleep(random.uniform(0.5, 0.8))
            logging.info("Continue fishing...")
            continue
            # maybe need to pause unpause thieving in this loop?

        # Update CLICK_COUNTER with the returned value from fish_from_spot
        CLICK_COUNTER = fish_from_spot(chat_text, CLICK_COUNTER)
        time.sleep(60) # Sleep for 60 seconds before checking again

if __name__ == "__main__":
    Fish()
