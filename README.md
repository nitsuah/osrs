# OSRS Bot

A Python-based bot designed to automate tasks and interact intelligently with the Old School RuneScape (OSRS) game. This project leverages computer vision and natural language processing to handle in-game actions and queries to avoid bot detection.

---

## Dependencies

- Python 3.13
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract): Manually installed (required for text recognition)
- Additional Python packages (see `requirements.txt`):
  - `pyautogui`
  - `opencv-python`
  - `opencv-python-headless`
  - `pillow`
  - `numpy`
  - `pytesseract`
  - `keyboard`
  - `textblob`

## Setup

1. Clone the repository:
  - `git clone https://github.com/nitsuah/osrs.git`

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   .\venv\Scripts\activate    # Windows
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify Tesseract installation:
   - Ensure Tesseract is installed and added to your system's PATH.
   - Check its version by running: `tesseract --version`

## Features

### Core Functions

#### Utilities

- **Configuration**:
  - `load_config`: Loads the configuration from an INI file, checking for required sections and validating values. This is essential for setting up coordinates and other constants for the bot's operation. The function also logs available keys in the 'constants' and 'coordinates' sections for debugging.

- **Game State**:
  - `compass.py` - `find_and_click_compass`: Aligns the in-game compass to the default position of North.
  - `camera.py` - `check_and_zoom_in` / `hold_up_arrow`: Checks the camera angle and zooms in and tilts up as necessary.
  - `thieving.py` - `check_tesseract_version`: Checks the version of the installed Tesseract OCR.

#### Skill Automation

Modules for automating in-game tasks like fishing and thieving.

- **Fishing (`fishing.py`)**:
  - `fish_from_spot`: Automates fishing by interacting with a fishing spot and responding to inventory full prompts (from `actions.py`).
  
- **Thieving  (`thieving.py`)**:
  - `thieve_from_stall`: Automates thieving from stalls, including handling inventory prompts and stopping if certain items (like Onyx) are detected (from `actions.py`).

#### Vision and Input (`screen_processing.py`)

- **Screen Capture and Image Processing**:
  - `capture_screen`: Captures the full screen using `ImageGrab` and processes it into a NumPy array.
  - `capture_and_process_chat`: Captures and processes the chat region from the screen using OCR to extract text.
  - `save_screenshot`: Saves a screenshot of the chat region for later analysis.

- **Image Processing with OpenCV**:
  - Uses OpenCV (`cv2`) to handle image manipulation and perform region-based screen captures to focus on specific parts of the game, such as the chat window.

#### Chat Recognition

- Detects specific chat queries related to teleportation and responds accordingly using predefined responses.
- This utilizes the following custom functions in a specific order:
  - `capture_and_process_chat`: Captures and processes the chat region from the screen using OCR (imported from `screen_processing.py`).
  - `lookup_response`: Looks up appropriate responses for skill-related questions and prompts in the game using predefined answers.
  - `respond_to_question`: Responds to game prompts (in game) such as trivia about or actions in the game.

#### Clicking Actions (`actions.py`)

- **Clicking Utilities**:
  - `click_with_variance`: Simulates clicks with slight random variance to mimic human interaction with the game.
  
- **Skill Interaction**:
  - `thieve_from_stall`: Handles thieving interactions, including responding to inventory prompts or stopping the bot if certain items (like Onyx) are found.
  - `fish_from_spot`: Handles fishing spot interaction, including inventory management when the player's pouch is full.

#### Natural Language Processing

- **Question Handling** (`question_handler.py`):
  - `load_question_responses`: Loads predefined question and answer pairs from a JSON file (`questions.json`).
  - `clean_question`: Cleans up the question text by removing irrelevant parts like `"Click here to continue."`
  - `correct_text`: Uses the `TextBlob` library to correct misspelled or ungrammatical text extracted from the game. - FIXME: This function is not yet refined.

## Usage

To run the bot's core functionality:
`python bot/core.py`

To automate a specific skill:
`python bot/skills/fishing.py`

Project Layout
```plaintext
├── bot/
│   ├── core.py          # Main entry point
│   ├── skills/
│   │   ├── fishing.py  # Handles fishing automation
│   ├── screen_processing.py  # Captures and processes screen
│   ├── question_handler.py   # Handles NLP
```