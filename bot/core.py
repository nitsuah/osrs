import configparser
import os
import logging

from bot.camera import check_and_zoom_in
from bot.compass import click_compass
from bot.skills.thieving import Theft


def load_config(filename: str) -> configparser.ConfigParser:
    """Load configuration from a file relative to this module."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), filename)
    config.read(config_path)
    return config


if __name__ == "__main__":
    logging.info("Current working directory: %s", os.getcwd())
    try:
        config = load_config("config.ini")
        logging.info("Loaded config sections: %s", config.sections())

        compass_coordinates = tuple(map(int, config['coordinates']['compass_position'].split(',')))
        click_compass(compass_coordinates)

        check_and_zoom_in(int(config['constants']['zoom_steps']))

        Theft()
    except Exception as e:
        logging.info("Error: %s", e)
