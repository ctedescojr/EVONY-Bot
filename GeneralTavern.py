import pyautogui
import time
import cv2
import numpy as np
import pytesseract
import keyboard
from PIL import Image, ImageDraw, ImageFont

# MARK: Coordinates
X_ACTION = 1600
Y_ACTION = 1980
X_CONFIRM = 2065
Y_CONFIRM = 1250
X_CANCEL = 1690
Y_CANCEL = 1250

# MARK: Wanted Generals
WANTED_GENERALS = [
    "martinus",
    "rei arthur",
    "minamoto no yoshitsune",
]  # Converted to lowercase for case-insensitive comparison

# Tesseract's PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def click_button(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


def capture_area(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    return screenshot


capture_count = 0


def save_capture(img):
    global capture_count
    capture_count += 1
    filename = f"capture{capture_count}.png"
    cv2.imwrite(filename, img)
    print(f"Image saved as {filename}")


def recognize_general(img):
    # Convert the PIL Image to a format OpenCV can use
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Preprocessing for OCR
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Dilate to make text thicker
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    # OCR
    general_name = pytesseract.image_to_string(
        dilate, lang="eng", config="--psm 7"
    )  # psm 7 for single text line
    general_name = general_name.strip().lower()  # Convert to lowercase
    return general_name


def recognize_cancel_button(img):
    # Convert the PIL Image to a format OpenCV can use
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Preprocessing for OCR
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # OCR
    text = pytesseract.image_to_string(thresh, lang="eng")
    text = text.strip().lower()

    # Check for keywords
    if "cancel" in text or "confirm" in text:
        return True
    return False


def main_loop():
    interaction = 1
    running = False
    intervention = False
    while True:
        if keyboard.is_pressed("s"):
            running = True
        elif keyboard.is_pressed("p"):
            running = False
        elif keyboard.is_pressed("q"):
            print("Bot stopping.")
            break

        if running:
            print(f"Interaction: {interaction}")
            # Click the "Refresh" button
            # click_button(
            #     X_ACTION, Y_ACTION
            # )  # Approximate coordinates of the "Refresh" button
            # time.sleep(0.5)

            # Capture the area where the general name appear
            img_general = capture_area(
                1620, 1450, 500, 42
            )  # Reverted to original coordinates to capture longer names

            # Caputre the area with orange general detected
            orange_general_detected_img = capture_area(1590, 1220, 200, 45)

            intervention = recognize_cancel_button(orange_general_detected_img)

            if intervention:
                print("Cancel/Confirm button detected. Handling intervention.")
                # If the cancel/confirm button is present, we need to decide whether to click confirm or cancel
                # Based on the existing logic, if the general is NOT the one we want, we click confirm to refresh.
                # If the general IS the one we want, we click cancel to stop.
                name = recognize_general(
                    img_general
                )  # Recognize general name even if intervention is true
                print(f"Recognized general name (lowercase): {name}")

                found_wanted_general = any(
                    general in name for general in WANTED_GENERALS
                )

                if not found_wanted_general:
                    print(
                        f"General: '{name}' does not contain any of the wanted generals. Clicking Confirm."
                    )
                    click_button(X_CONFIRM, Y_CONFIRM)
                else:
                    print(
                        f"General: '{name}' contains a wanted general. Clicking Cancel to stop."
                    )
                    click_button(X_CANCEL, Y_CANCEL)
                    break  # Stop the bot after finding the general and clicking cancel
            else:
                # No intervention button, proceed with general recognition
                name = recognize_general(img_general)
                print(f"Recognized general name (lowercase): {name}")

                # Check if name was caught
                if not name:  # Handles empty string or None
                    print("No name detected.")
                    print("Waiting connection...")
                    time.sleep(0.5)
                    print("Bot restarted")
                    click_button(
                        X_ACTION, Y_ACTION
                    )  # Approximate coordinates of the "Refresh" button
                    time.sleep(0.5)
                    continue

                found_wanted_general = any(
                    general in name for general in WANTED_GENERALS
                )

                if found_wanted_general:
                    print(f"General: '{name}' founded!")
                    break  # Found the general, stop the bot
                else:
                    print(
                        f"General: '{name}' does not contain any of the wanted generals. Continuing search."
                    )
                    click_button(
                        X_ACTION, Y_ACTION
                    )  # Approximate coordinates of the "Refresh" button
                    time.sleep(0.5)

            interaction += 1
            time.sleep(0.5)
        time.sleep(0.1)  # Small pause to avoid overloading the loop


# Start the bot
main_loop()
