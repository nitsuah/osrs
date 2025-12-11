import logging
import time
import winsound
import pyautogui
import keyboard
import random
from typing import Tuple
from bot.config import load_config
from bot.skills.screen_processing import capture_screen, capture_and_process_chat, save_screenshot
from bot.skills.question_handler import load_question_responses, lookup_response
from bot.skills.actions import thieve_from_stall

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration
config = load_config("config.ini")

# Debugging line to logging.info the raw value
logging.info("Chat region raw value: %s", config["coordinates"]["chat_region"])

# Strip any comments and handle leading/trailing whitespace
raw_chat_region = config["coordinates"]["chat_region"].split('#')[0].strip()
chat_region: Tuple[int, int, int, int] = tuple(map(int, raw_chat_region.split(',')))

RUNNING = True
PAUSE_THIEVING = False
CLICK_COUNTER = 0

question_responses = load_question_responses()


def respond_to_question(question: str, chat_image) -> None:
    """Respond to a detected question in chat.

    Args:
        question: The normalized question text.
        chat_image: The image array of the chat region for screenshots.
    """
    response = lookup_response(question, question_responses)
    logging.info("Detected question: '%s'", question)
    logging.info("Responding with: '%s'", response)

    if response == "bald":
        winsound.Beep(500, 500)
        save_screenshot(chat_image)
        input("Press Enter to continue...")
    else:
        time.sleep(0.5)
        pyautogui.press('space')
        time.sleep(1)
        pyautogui.typewrite(response)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)


def handle_user_input() -> None:
    global PAUSE_THIEVING
    if keyboard.is_pressed('f1'):
        winsound.Beep(1000, 500)
        PAUSE_THIEVING = not PAUSE_THIEVING
        time.sleep(1)


def Theft() -> None:
    """Main loop for thieving automation."""
    logging.info("Starting the Thieving bot...")
    global CLICK_COUNTER
    while RUNNING:
        if PAUSE_THIEVING:
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
            logging.info("Continue thieving...")
            continue
            # maybe need to pause unpause thieving in this loop?

        # Update CLICK_COUNTER with the returned value from thieve_from_stall
        CLICK_COUNTER = thieve_from_stall(chat_text, CLICK_COUNTER)
        time.sleep(random.uniform(0.5, 0.8))


if __name__ == "__main__":
    Theft()
