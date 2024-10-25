import configparser
import os

def load_config(filename):
    """Load configuration from the specified INI file."""
    config = configparser.ConfigParser()
    config.read(filename)

    # Check for required sections
    if 'constants' not in config or 'coordinates' not in config:
        raise KeyError("Missing required sections in the configuration file.")
    
    # Print the available keys for debugging
    print("Available keys in 'constants' section:", list(config['constants'].keys()))
    print("Available keys in 'coordinates' section:", list(config['coordinates'].keys()))

    # Retrieve and validate configuration values
    try:
        zoom_steps = config.getint('constants', 'zoom_steps')
        compass_coordinates = tuple(map(int, config['coordinates']['compass_position'].strip("()").split(",")))
        thieve_coordinates = tuple(map(int, config['coordinates']['inventory_slot_1'].strip("()").split(",")))  # Update as needed
    except KeyError as e:
        raise KeyError(f"Missing key in configuration file: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid value in configuration file: {e}")

    return {
        'zoom_steps': zoom_steps,
        'compass_coordinates': compass_coordinates,
        'thieve_coordinates': thieve_coordinates  # Adjust this if needed
    }
