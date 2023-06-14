import pyautogui, sys

print("Press Ctrl-C to quit.")

try:
    while True:
        x, y = pyautogui.position()
        #positionStr = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
        r,g,b = pyautogui.pixel(x, y)
        ColorStr = "R: " + str(r).rjust(4) + " G: " + str(g).rjust(4) + " B: " + str(b).rjust(4)
        #print(positionStr, end="") # positionStr
        #print("\b" * len(positionStr), end="", flush=True)
        print(ColorStr, end="") # positionStr
        print("\b" * len(ColorStr), end="", flush=True)
except KeyboardInterrupt:
    print("\n")
