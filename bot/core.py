import configparser
import os
import logging
from bot.camera import check_and_zoom_in  # Import the zoom function
from bot.compass import click_compass
from bot.skills.thieving import Theft  # Import main function from thieving
from bot.skills.fishing import Fish  # Import main function from fishing

def load_config(filename):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), filename)  # Adjust path as necessary
    config.read(config_path)
    return config

if __name__ == "__main__":
    logging.info("Current working directory: %s", os.getcwd())  # Debugging output
    try:
        config = load_config("config.ini")
        logging.info("Loaded config sections: %s", config.sections())  # Debugging output

        # Load compass coordinates from the coordinates section
        compass_coordinates = tuple(map(int, config['coordinates']['compass_position'].split(',')))
        # Click the compass first
        click_compass(compass_coordinates)

        # Now zoom the camera
        check_and_zoom_in(int(config['constants']['zoom_steps']))  # Pass the zoom steps

        # Start the main fishing loop
        Fish()
        # Start the main thieving loop
        # Theft()
    except Exception as e:
        logging.info(f"Error: {e}")
