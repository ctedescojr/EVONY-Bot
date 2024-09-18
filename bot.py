import pyautogui
import time
import cv2
import numpy as np
import pytesseract
import keyboard
from PIL import Image, ImageDraw, ImageFont

# Tesseract's PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def click_button(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


def capture_area(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


capture_count = 0


def save_capture(img):
    global capture_count
    capture_count += 1
    filename = f"capture{capture_count}.png"
    cv2.imwrite(filename, img)
    print(f"Image saved as {filename}")


def recognize_number_and_arrow(img):
    # Convert to HSV for easier color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color ranges for red and green
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])

    # Create masks for red and green colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Combine masks
    combined_mask = cv2.bitwise_or(mask_red, mask_green)

    numbers_and_arrows = []
    height, width = img.shape[:2]
    expected_height = height // 4  # Expecting 4 lines in the image

    for i in range(4):  # Processing 4 lines
        y_start = i * expected_height
        y_end = (i + 1) * expected_height
        line_img = img[y_start:y_end, :]

        # Check if the line contains any colored pixels
        if np.sum(combined_mask[y_start:y_end, :]) > 0:
            is_red = np.sum(mask_red[y_start:y_end, :]) > np.sum(
                mask_green[y_start:y_end, :]
            )

            # Specific preprocessing for green
            if not is_red:
                number = process_green_number(line_img)
            else:
                # Use Tesseract to recognize the number
                number = pytesseract.image_to_string(
                    line_img,
                    config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789",
                )
            if number.strip():
                value = int(number)
                if is_red:
                    value = -value
                numbers_and_arrows.append(value)
            else:
                # If no number is recognized, try again with a different configuration
                number = pytesseract.image_to_string(
                    line_img,
                    config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789",
                )
                if number.strip():
                    value = int(number)
                    if is_red:
                        value = -value
                    numbers_and_arrows.append(value)
                else:
                    numbers_and_arrows.append(0)  # If still not recognized, assume 0
        else:
            # If no colored pixels, assume it's an empty space
            numbers_and_arrows.append(0)

    return numbers_and_arrows


def process_green_number(img):
    # Extract the green channel
    _, green, _ = cv2.split(img)

    # Increase contrast
    green = cv2.addWeighted(green, 2, np.zeros(green.shape, green.dtype), 0, 0)

    # Binarization
    _, binary = cv2.threshold(green, 200, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # If contours are found, it's likely a number
        # Use Tesseract to recognize the number
        number = pytesseract.image_to_string(
            binary, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789"
        )
        return (
            number.strip() if number.strip() else "1"
        )  # If not recognized, assume it's 1
    else:
        # If no contours are found, it's likely an empty space
        return None


def main_loop():
    confirm = 0
    cancel = 0
    points_gained = 0
    interaction = 1
    running = False
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
            # Click the "Cultivate Gold" button
            click_button(
                2130, 1980
            )  # Approximate coordinates of the "Cultivate Gold" button
            time.sleep(1)

            # Capture the area where the numbers with arrows appear
            img_numbers = capture_area(
                2335, 440, 25, 310
            )  # Adjusted coordinates to capture all possible numbers

            numbers_and_arrows = recognize_number_and_arrow(img_numbers)
            # Save the capture
            # save_capture(img_numbers)
            print(f"Numbers: {numbers_and_arrows}")

            # Check if numbers_and_arrows is [0, 0, 0, 0]
            if numbers_and_arrows == [0, 0, 0, 0]:
                print("Detected [0, 0, 0, 0]. Pausing the bot.")
                print("Waiting connection...")
                time.sleep(6)
                print("Bot restarted.")
                continue

            total = sum(numbers_and_arrows)
            print(f"Sum: {total}")
            if total >= 0:
                # Click the "Confirm" button
                click_button(2130, 1980)  # Coordinates of the "Confirm" button
                confirm += 1
                points_gained += total
                print(f"Confirmed: {confirm}")
            else:
                # Click the "Cancel" button
                click_button(1600, 1980)  # Coordinates of the "Cancel" button
                cancel += 1
                print(f"Cancelled: {cancel}")
            numbers_and_arrows = []
            total = 0
            print(f"Points gained: {points_gained}")
            interaction += 1
            time.sleep(1)
        time.sleep(0.1)  # Small pause to avoid overloading the loop


# Start the bot
main_loop()
