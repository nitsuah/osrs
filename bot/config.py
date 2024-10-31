import configparser
import os
import logging

def load_config(filename="config.ini"):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), filename)
    config.read(config_path)
    return config

config = load_config()
