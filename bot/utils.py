import configparser

def load_config(filename):
    """Load configuration from the specified INI file."""
    config = configparser.ConfigParser()
    config.read(filename)

    # Check for 'DEFAULT' section
    if 'DEFAULT' not in config:
        raise KeyError("Missing 'DEFAULT' section in the configuration file.")
    
    # Print the available keys for debugging
    print("Available keys in 'DEFAULT' section:", config['DEFAULT'])

    # Retrieve and validate configuration values
    try:
        zoom_steps = int(config['DEFAULT']['zoom_steps'])
        compass_coordinates = tuple(map(int, config['DEFAULT']['compass_coordinates'].strip("()").split(",")))
        thieve_coordinates = tuple(map(int, config['DEFAULT']['thieve_coordinates'].strip("()").split(",")))
    except KeyError as e:
        raise KeyError(f"Missing key in configuration file: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid value in configuration file: {e}")

    return {
        'zoom_steps': zoom_steps,
        'compass_coordinates': compass_coordinates,
        'thieve_coordinates': thieve_coordinates
    }
