# EVONY-Bot

## Description

This bot is designed to automate the "Cultivate Gold" process in a game, with an intelligent auto-pausing feature. It interacts with the game interface, making decisions based on recognized numbers and arrows, and can automatically pause when it detects specific patterns.

## Features

- Automatic clicking of "Cultivate Gold" button
- Image recognition to capture and interpret numbers and arrows
- Decision making based on the sum of recognized numbers
- Manual start/pause/stop controls
- Automatic pausing when [0, 0, 0, 0] pattern is detected
- Tracking of confirmations, cancellations, and points gained

## Technical Details

### Tesseract OCR

This bot utilizes Tesseract OCR (Optical Character Recognition) for recognizing numbers in the captured game images. Tesseract is an open-source OCR engine that can recognize and "read" text in images.

In our bot:
- Tesseract is used to convert the captured image of numbers and arrows into machine-readable text.
- We configure Tesseract to specifically look for digits, improving accuracy for our use case.
- The `pytesseract` library is used as a Python wrapper for Tesseract.

Installation:
1. Install Tesseract OCR on your system. On Windows, you can download it from the [official GitHub repository](https://github.com/UB-Mannheim/tesseract/wiki).
2. Install the Python wrapper:
   ```
   pip install pytesseract
   ```
3. Ensure the Tesseract executable is in your system PATH or specify its location in your script.

Usage in the bot:
```python
import pytesseract

# If needed, specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Using Tesseract to recognize text in an image
text = pytesseract.image_to_string(image, config='--psm 6 outputbase digits')
```

### OpenCV (cv2)

OpenCV (Open Source Computer Vision Library) is used for image processing tasks in the bot. It's crucial for capturing and preprocessing the game screen before passing it to Tesseract for text recognition.

Key uses of OpenCV in the bot:
1. Screen Capture: Capturing specific regions of the game screen.
2. Image Preprocessing: Enhancing the captured image to improve OCR accuracy.
3. Arrow Detection: Identifying up or down arrows next to numbers.

Installation:
```
pip install opencv-python
```

Usage examples in the bot:
```python
import cv2
import numpy as np

# Capture screen region
screenshot = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

# Preprocess image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Arrow detection (simplified example)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    # Analyze contour shape to determine if it's an up or down arrow
    # ...
```

These technologies work together to enable the bot to accurately read and interpret the game screen, allowing it to make decisions based on the numbers and arrows it recognizes.

## Requirements

- Python 3.x
- Required Python libraries:
  - `keyboard` for key press detection
  - `time` for managing delays
  - (Add any other libraries used for image capture and recognition)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ctedescojr/EVONY-Bot
   ```
2. Navigate to the project directory:
   ```
   cd EVONY_Bot
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate your virtual environment:
   
   Windows:
   ```
   venv/Scripts/activate
   ```
   Linux:
   ```
   source venv/bin/activate
   ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python bot.py
   ```
2. Use the following controls:
   - Press 's' to start the bot
   - Press 'p' to pause the bot
   - Press 'q' to quit the bot

## How It Works

1. The bot clicks the "Cultivate Gold" button.
2. It captures and recognizes numbers and arrows in a specific area of the screen.
3. If the recognized pattern is [0, 0, 0, 0], the bot automatically pauses.
4. Otherwise, it calculates the sum of the numbers:
   - If the sum is non-negative, it clicks "Confirm" and adds to the points.
   - If the sum is negative, it clicks "Cancel".
5. The process repeats until manually paused or stopped.

## Customization

You may need to adjust the following parameters based on your screen resolution and game layout:
- Coordinates for button clicks
   - Use utils/mouse.py script to map your mouse coordinates
- Capture area for number recognition
   - Use utils/screenshot.py to test the screenshot area

## Disclaimer

This bot is for educational purposes only. Please ensure you comply with the terms of service of the game you're using it with.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/auto-pausing-cultivation-bot/issues) if you want to contribute.

