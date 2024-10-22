import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import pytesseract

# Specify the Tesseract OCR path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen():
    """Capture the full screen and return it as a numpy array."""
    img = ImageGrab.grab()  # Fullscreen capture
    return np.array(img)

def get_minimap_region(screen_np, screen_width, screen_height):
    """Extract the minimap region from the full screen image."""
    # Assuming the minimap is in the top-right corner of the screen
    minimap_region = screen_np[0:250, screen_width-250:screen_width]  # Adjust values as needed
    return minimap_region

def find_and_click_compass(screen_width):
    """Click the compass directly using known coordinates."""
    compass_x, compass_y = 1740, 44  # Compass position on your screen
    # Click the compass to set the camera to north
    pyautogui.click(compass_x, compass_y)
    print(f"Clicked compass at: {compass_x}, {compass_y}")

def capture_and_process_chat(screen_np, screen_width, screen_height):
    """Capture the chat region and extract any text using OCR."""
    chat_width = int(screen_width * 0.2)  # 20% of the screen width
    chat_height = int(screen_height * 0.3)  # 30% of the screen height
    chat_region = screen_np[screen_height - chat_height:screen_height, 0:chat_width]

    # Convert chat region to grayscale for OCR
    gray_chat_region = cv2.cvtColor(chat_region, cv2.COLOR_BGR2GRAY)

    # Use Tesseract OCR to detect text
    chat_text = pytesseract.image_to_string(gray_chat_region)
    print("Chat Text:", chat_text)

def main():
    # Screen resolution (adjust based on your monitor setup)
    screen_width, screen_height = pyautogui.size()  # This will give you the resolution dynamically

    # Capture the entire screen
    screen_np = capture_screen()

    # Detect the compass in the minimap and click it to set the camera to north
    find_and_click_compass(screen_width)

    # Process the chat region (optional)
    capture_and_process_chat(screen_np, screen_width, screen_height)

    # Display the entire screen for verification
    cv2.imshow("Full Screen Capture", screen_np)
    cv2.waitKey(0)  # Wait for a key press to close the window

if __name__ == "__main__":
    main()

