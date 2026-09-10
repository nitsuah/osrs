import logging
import time
import winsound
import random
import keyboard
from bot.config import load_config
from bot.checkpoint import CheckpointLogger
from bot.health import StuckStateMonitor
from bot.skills.screen_processing import capture_screen, capture_and_process_chat
# from bot.skills.question_handler import correct_text
from bot.skills.actions import fish_from_spot
from bot.skills.thieving import respond_to_question

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration
config = load_config("config.ini")

# Debugging line to logging.info the raw value
logging.info("Chat region raw value: %s", config["coordinates"]["chat_region"])

# Strip any comments and handle leading/trailing whitespace
raw_chat_region = config["coordinates"]["chat_region"].split('#')[0].strip()
chat_region = tuple(map(int, raw_chat_region.split(',')))

RUNNING = True
PAUSE_FISHING = False
CLICK_COUNTER = 0

health_monitor = StuckStateMonitor("fishing")
checkpoint_logger = CheckpointLogger("fishing")


def handle_user_input() -> None:
    global PAUSE_FISHING
    if keyboard.is_pressed('f1'):
        winsound.Beep(1000, 500)
        PAUSE_FISHING = not PAUSE_FISHING
        time.sleep(1)


def Fish() -> None:
    logging.info("Starting the Fishing bot...")

    global CLICK_COUNTER
    try:
        while RUNNING:
            checkpoint_logger.checkpoint(health_monitor)

            if PAUSE_FISHING:
                time.sleep(1)
                handle_user_input()
                continue

            handle_user_input()

            if health_monitor.is_stuck():
                health_monitor.recover()
                # Give the environment a beat before retrying rather than
                # immediately hammering the same capture path that was just
                # declared stuck in this same iteration.
                time.sleep(1)
                continue

            screen_np = capture_screen()
            if screen_np is None:
                health_monitor.record_capture_failure()
                time.sleep(0.5)
                continue
            # Pass the chat region to the capture function
            chat_text, chat_image, ocr_ok = capture_and_process_chat(screen_np, chat_region)
            if not ocr_ok:
                health_monitor.record_capture_failure()
                time.sleep(0.5)
                continue
            health_monitor.record_frame(chat_text)
            # Check if a question prompt needs a response
            if "teleported" in chat_text.lower():
                logging.info("Question prompt detected.")
                if ":" in chat_text:
                    question = chat_text.split(":", 1)[1].strip()
                else:
                    question = chat_text.strip()  # Fallback if no colon is found
                logging.info("Responding to question...")
                respond_to_question(question, chat_image)
                checkpoint_logger.record_action("respond_to_question")
                health_monitor.record_activity()
                time.sleep(random.uniform(0.5, 0.8))
                logging.info("Continue fishing...")
                continue
                # maybe need to pause unpause thieving in this loop?

            # Update CLICK_COUNTER with the returned value from fish_from_spot
            CLICK_COUNTER = fish_from_spot(chat_text, CLICK_COUNTER)
            checkpoint_logger.record_action("fish_from_spot")
            health_monitor.record_activity()
            time.sleep(60)  # Sleep for 60 seconds before checking again
    except Exception as exc:
        checkpoint_logger.summarize_failure(exc, health_monitor)
        raise


if __name__ == "__main__":
    Fish()
