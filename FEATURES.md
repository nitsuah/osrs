# OSRS Bot Features

## Automation Core

### 🎯 Skill Automation

- **Thieving Bot**: Automates stealing from stalls with inventory management, rare item detection (Onyx), and chat monitoring
- **Fishing Bot**: Automates fishing from spots with 60-second intervals and inventory full detection
- **Click Variance**: Randomized click positions (±5 pixels) to mimic human interaction patterns
- **Pause/Resume Control**: F1 key toggles bot activity with audio feedback

### 👁️ Computer Vision & OCR

- **Screen Capture**: Real-time screen capture using PIL ImageGrab with NumPy processing
- **Chat Region Parsing**: Extracts and processes chat text from configurable screen regions
- **Tesseract OCR Integration**: Text recognition for detecting game prompts and questions
- **Screenshot Saving**: Captures chat images for debugging unknown questions

## Intelligence Systems

### 🤖 Anti-Detection

- **Question Handler**: Detects and responds to in-game anti-bot questions using keyword matching
- **Response Database**: JSON-based question/answer library for automated responses
- **Text Correction**: TextBlob integration for spell-checking OCR output (in development)
- **Human-like Timing**: Random delays (0.5-0.8s) between actions to avoid detection patterns

### ⚙️ Game State Management

- **Compass Reset**: Automatically clicks compass to reset camera orientation to North
- **Camera Control**: Zooms in with configurable scroll steps and tilts camera upward
- **Inventory Detection**: Monitors chat for "inventory is full" messages
- **Teleport Detection**: Recognizes when player is teleported and halts automation

## Configuration & Utilities

### 📐 Configuration System

- **INI-based Config**: Centralized configuration for coordinates, constants, and settings
- **Chat Region Definition**: Customizable screen regions for OCR parsing
- **Zoom Steps**: Configurable camera zoom increments
- **Coordinate Management**: Stores click positions for compass, stalls, and fishing spots

### 🛠️ Development Tools

- **Mouse Click Recorder**: Records and saves click coordinates for configuration setup
- **Logging System**: Comprehensive logging for debugging bot behavior
- **Modular Architecture**: Separated concerns (skills, vision, config, actions)
