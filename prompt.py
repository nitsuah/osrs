import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import pytesseract
import time
import os
import csv

# Specify the Tesseract OCR path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordinates for logout/login
LOGOUT_COORDS = (1874, 33)
CONFIRM_LOGOUT_COORDS = (1764, 907)
LOGIN_COORDS = (950, 320)

# Coordinates for clicking the stall (where the question appears)
STALL_COORDS = (960, 604)  # Replace with actual stall coordinates

# Directory to save screenshots
screenshot_directory = "questions"
if not os.path.exists(screenshot_directory):
    os.makedirs(screenshot_directory)

# File to store unique questions
questions_file = "unique_questions.csv"

# Load existing questions if they exist
if os.path.exists(questions_file):
    with open(questions_file, newline='', encoding='utf-8') as f:
        existing_questions = {row[0] for row in csv.reader(f)}
else:
    existing_questions = set()

def capture_screen():
    """Capture the full screen and return it as a numpy array."""
    img = ImageGrab.grab()  # Fullscreen capture
    return np.array(img)

def capture_and_process_chat(screen_np):
    """Capture the chat region and extract any text using OCR."""
    chat_region = screen_np[869:985, 0:495]  # Adjust coordinates as needed
    gray_chat_region = cv2.cvtColor(chat_region, cv2.COLOR_BGR2GRAY)
    chat_text = pytesseract.image_to_string(gray_chat_region)
    print("Chat Text:", chat_text)

    # Check for the anti-bot prompt
    if "please answer this question" in chat_text.lower():
        question = extract_question(chat_text)
        if question:
            save_question_image(screen_np)
            return question

    return None

def extract_question(chat_text):
    """Extract the question from the chat text."""
    start_index = chat_text.find(":") + 1  # Find where the question starts
    question = chat_text[start_index:].strip()  # Extract the question
    return question

def save_question_image(screen_np):
    """Save a screenshot of the full screen when the question is asked."""
    screenshot_path = os.path.join(screenshot_directory, f"question_{time.strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(screenshot_path, screen_np)  # Save the screenshot
    print(f"Saved screenshot: {screenshot_path}")

def log_out():
    """Automate the logout process."""
    print("Logging out...")
    pyautogui.click(*LOGOUT_COORDS)  # Click the logout button
    time.sleep(1)  # Wait for any logout menu to appear
    pyautogui.click(*CONFIRM_LOGOUT_COORDS)  # Confirm logout
    time.sleep(10)  # Wait for the game to fully log out

def log_in():
    """Automate the login process."""
    print("Logging back in...")
    pyautogui.click(*LOGIN_COORDS)  # Click the login button
    time.sleep(10)  # Wait for the game to fully log in
    click_stall()

def click_stall():
    """Click on the stall to display the question."""
    print("Clicking the stall to display the question...")
    pyautogui.click(*STALL_COORDS)  # Click on the stall coordinates
    time.sleep(2)  # Wait for the question to appear before scanning

def save_question_to_file(question):
    """Save the question to a CSV file if it's not already saved."""
    if question not in existing_questions:
        with open(questions_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([question])
        existing_questions.add(question)
        print(f"New question saved: {question}")

def main():
    questions = []  # To store questions we detect

    while True:
        log_in() # Login first
        time.sleep(1)  # Wait for the game to fully log in
        screen_np = capture_screen()  # Capture the screen
        question = capture_and_process_chat(screen_np)  # Process chat and get the question

        if question:
            print(f"Detected Question: {question}")
            if question not in existing_questions:
                questions.append(question)  # Store the question locally
                save_question_to_file(question)  # Save the question to the file
            log_out()  # Log out of the game
            time.sleep(10)  # Wait for a few seconds before logging back in
            log_in()  # Log back in to get another question

        time.sleep(5)  # Small delay before checking for another question

if __name__ == "__main__":
    main()
