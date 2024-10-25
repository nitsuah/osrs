import configparser
import os
from bot.camera import check_and_zoom_in  # Import the zoom function
from bot.compass import click_compass
from bot.skills.thieving import main  # Import main function from thieving

def load_config(filename):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), filename)  # Adjust path as necessary
    config.read(config_path)
    return config

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())  # Debugging output
    try:
        config = load_config("config.ini")
        print("Loaded config sections:", config.sections())  # Debugging output

        # Load compass coordinates from the coordinates section
        compass_coordinates = tuple(map(int, config['coordinates']['compass_position'].split(',')))
        # Click the compass first
        click_compass(compass_coordinates)

        # Now zoom the camera
        check_and_zoom_in(int(config['constants']['zoom_steps']))  # Pass the zoom steps

        # Start the main thieving loop
        main()
    except Exception as e:
        print(f"Error: {e}")
