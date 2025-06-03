import pyautogui
import time


def capture_area(x, y, width, height, filename):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(filename)  # Save the image to disk
    return screenshot


# Example of using the modified function
def main():
    while True:
        # Assume you want to capture an area periodically
        print("Capturing the screen...")
        capture_area(1620, 1450, 500, 42, "capture2.png")  # Specify the filename
        print("Image saved as 'capture.png'")
        time.sleep(10)  # Wait 10 seconds before the next capture


if __name__ == "__main__":
    main()
