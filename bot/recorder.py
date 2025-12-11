from pynput import mouse, keyboard
import time
import csv


# Define a filename to save the recorded actions
FILENAME = "mouse_clicks.csv"

# Initialize list to store recorded clicks
click_data = []


# Mouse click listener
def on_click(x, y, button, pressed):
    if pressed:
        timestamp = time.time()
        click_data.append([timestamp, x, y, button])
        print(f"Mouse clicked at ({x}, {y}) with {button} at {timestamp}")


# Keyboard listener for stopping
def on_press(key):
    try:
        if key.char == 'q':  # Press 'q' to stop the recording
            print("Recording stopped.")
            return False
    except AttributeError:
        pass


# Save recorded clicks to a CSV file
def save_clicks():
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X", "Y", "Button"])
        writer.writerows(click_data)
    print(f"Recorded actions saved to {FILENAME}")


# Main function to start the listeners
def record_mouse_clicks():
    # Start the mouse listener
    with mouse.Listener(on_click=on_click) as mouse_listener, \
            keyboard.Listener(on_press=on_press) as keyboard_listener:

        print("Recording started. Press 'q' to stop.")
        mouse_listener.join()  # Wait for 'q' to stop recording
        keyboard_listener.join()

    save_clicks()


if __name__ == "__main__":
    record_mouse_clicks()
