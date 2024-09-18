import pyautogui
import time

print("Press Ctrl-C to stop the program.")

try:
    while True:
        x, y = pyautogui.position()  # Get the current cursor position
        positionStr = f"X: {x} Y: {y}"
        print(positionStr, end="")
        print("\b" * len(positionStr), end="", flush=True)
        time.sleep(0.1)  # Update the position every 0.1 seconds
except KeyboardInterrupt:
    print("\nTerminated.")
