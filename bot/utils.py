import configparser

def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    
    # Convert zoom_steps to an integer
    zoom_steps = int(config['DEFAULT']['zoom_steps'])
    
    # Convert compass_coordinates and thieve_coordinates to tuples of integers
    compass_coordinates = tuple(map(int, config['DEFAULT']['compass_coordinates'].strip("()").split(",")))
    thieve_coordinates = tuple(map(int, config['DEFAULT']['thieve_coordinates'].strip("()").split(",")))

    return {
        'zoom_steps': zoom_steps,
        'compass_coordinates': compass_coordinates,
        'thieve_coordinates': thieve_coordinates
    }