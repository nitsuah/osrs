import random
import time
import pyautogui
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

def thieve_from_stall(chat_text):
    if "your inventory is full" in chat_text.lower():
        click_with_variance(*inventory_slots[0], variance=0)
        return True
    click_with_variance(*stall_position)
    return False
