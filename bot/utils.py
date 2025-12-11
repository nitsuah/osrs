import configparser
import logging


def load_config(filename):
    """Load configuration from the specified INI file."""
    config = configparser.ConfigParser()
    config.read(filename)

    # Check for required sections
    if 'constants' not in config or 'coordinates' not in config:
        raise KeyError("Missing required sections in the configuration file.")

    # Log the available keys for debugging
    constants_keys = list(config['constants'].keys())
    coords_keys = list(config['coordinates'].keys())
    logging.info("Available keys in 'constants' section: %s", constants_keys)
    logging.info("Available keys in 'coordinates' section: %s", coords_keys)

    # Retrieve and validate configuration values
    try:
        zoom_steps = config.getint('constants', 'zoom_steps')
        compass_raw = config['coordinates']['compass_position']
        thieve_raw = config['coordinates']['inventory_slot_1']

        compass_coordinates = tuple(
            map(int, compass_raw.strip("()").split(","))
        )
        thieve_coordinates = tuple(
            map(int, thieve_raw.strip("()").split(","))
        )
    except KeyError as e:
        raise KeyError(f"Missing key in configuration file: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid value in configuration file: {e}")

    return {
        'zoom_steps': zoom_steps,
        'compass_coordinates': compass_coordinates,
        'thieve_coordinates': thieve_coordinates  # Adjust this if needed
    }
