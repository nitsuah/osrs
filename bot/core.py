import time
import pyautogui
from bot.utils import load_config
from bot.camera import zoom_camera
from bot.compass import click_compass
from bot.skills.thieving import thieve_from_stall

if __name__ == "__main__":
    try:
        config = load_config("config.ini")
        zoom_camera(config['zoom_steps'])
        click_compass(config['compass_coordinates'])
        thieve_from_stall(config['thieve_coordinates'])
    except Exception as e:
        print(f"Error: {e}")
