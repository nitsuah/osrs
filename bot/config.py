import configparser
import os


def load_config(filename: str = "config.ini") -> configparser.ConfigParser:
    """Load and return the bot configuration from an INI file."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), filename)
    config.read(config_path)
    return config


config = load_config()
