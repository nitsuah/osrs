import numpy as np
from PIL import ImageGrab
import cv2
import os
import time
import logging
import pytesseract
from bot.config import config

# Set up the Tesseract path
pytesseract.pytesseract.tesseract_cmd = config['tesseract']['path']

SCREENSHOT_DIRECTORY = ".//bot//questions"


def capture_screen():
    try:
        # Capture the screen using ImageGrab
        screen = ImageGrab.grab()
        screen_np = np.array(screen)
        # logging.info("Screen captured successfully.")
        return cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
    except Exception as e:
        logging.error("Error capturing screen: %s", e)
        return None


def capture_and_process_chat(screen_np, chat_region):
    """Crop the chat region and OCR it.

    Returns `("", chat_image)` (rather than raising) when Tesseract is
    missing/misconfigured or OCR otherwise fails, so a transient OCR error
    can't crash a long-running automation loop -- callers already treat an
    empty `chat_text` as "nothing detected this frame".
    """
    x1, y1, x2, y2 = chat_region
    chat_image = screen_np[y1:y2, x1:x2]  # Capture the chat region
    try:
        chat_text = pytesseract.image_to_string(chat_image)
    except Exception as e:
        logging.error("Error running OCR on chat region: %s", e)
        return "", chat_image
    return chat_text, chat_image


def save_screenshot(chat_image):
    """Save a chat-region screenshot for debugging unmatched questions.

    Directory creation happens lazily here (not at import time) and both
    the mkdir and the write are guarded: a read-only filesystem or missing
    permissions (e.g. the non-root Docker runtime user) should never crash
    an OCR-triggered import or the caller's loop -- it should just skip the
    debug screenshot and log why.
    """
    try:
        os.makedirs(SCREENSHOT_DIRECTORY, exist_ok=True)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"question_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIRECTORY, filename)
        cv2.imwrite(screenshot_path, chat_image)
        logging.info("Saved screenshot: %s", screenshot_path)
    except OSError as e:
        logging.error("Error saving screenshot: %s", e)
