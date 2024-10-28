import random
import time
import pyautogui
import logging
from bot.config import load_config

# Load configuration
config = load_config("config.ini")

# Extract inventory slots and stall position from the config
inventory_slots = [
    tuple(map(int, config['coordinates'][f'inventory_slot_{i+1}'].split(',')))
    for i in range(2)  # Adjust range if you have more slots
]
stall_position = tuple(map(int, config['coordinates']['stall_position'].split(',')))

def click_with_variance(x, y, variance=5):
    x += random.randint(-variance, variance)
    y += random.randint(-variance, variance)
    pyautogui.click(x, y)

def thieve_from_stall(chat_text, click_counter):
    # If the coin pouch is full, clear it by clicking the first slot
    if "empty your coin" in chat_text.lower() and click_counter > 15:
        click_with_variance(*inventory_slots[0], variance=0)  # Clears inventory slot
        time.sleep(random.uniform(0.1, 0.4))  # Add delay after clearing
        click_with_variance(*inventory_slots[0], variance=0)  # Confirms inventory slot is cleared
        time.sleep(random.uniform(0.1, 0.4))  # Add delay after clearing
        logging.info("Cleared inventory slot and resuming thieving.")
        return 0  # Reset click counter
    elif "inventory" in chat_text.lower() and click_counter > 15:
        time.sleep(random.uniform(0.1, 0.4))  # Add delay before clearing
        pyautogui.typewrite("::empty")
        time.sleep(random.uniform(0.4, 0.5))  # Add delay after clearing
        pyautogui.press('enter')
        logging.info("Emptied inventory and resuming thieving.")
        return 0  # Reset click counter
    else:
        # Continue thieving
        click_with_variance(*stall_position)
        return click_counter + 1  # Increment counter if thieving
