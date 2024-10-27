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
os.makedirs(SCREENSHOT_DIRECTORY, exist_ok=True)

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
    x1, y1, x2, y2 = chat_region
    # logging.info(f"Captured and processed chat region: {chat_region}")
    chat_image = screen_np[y1:y2, x1:x2]  # Capture the chat region
    chat_text = pytesseract.image_to_string(chat_image)
    return chat_text, chat_image

def save_screenshot(chat_image):
    try:
        screenshot_path = os.path.join(SCREENSHOT_DIRECTORY, f"question_{time.strftime('%Y%m%d_%H%M%S')}.png")
        cv2.imwrite(screenshot_path, chat_image)
        logging.info("Saved screenshot: %s", screenshot_path)
    except IOError as e:
        logging.error("Error saving screenshot: %s", e)
