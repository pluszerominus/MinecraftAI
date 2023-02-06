import sys
import numpy as np
import cv2
from PIL import ImageGrab
import time
from pynput.keyboard import Key,Controller as KeyboardController
from pynput.mouse import Button,Controller as MouseController
import threading
import mouse,keyboard
import csv
print(threading.enumerate())

# Keyboard and mouse controller
keyboard_cont = KeyboardController()
mouse_cont = MouseController()

# Windows size
window_pos = [10, 30, 1920, 1040]
n = 0
count = 1

# Main function
def start_grab(n,count):
    # Button name
    name_button = ["w", "a", "s", "d","shift", "ctrl","space", "e", "q",
                   None,None,None,None,None,None,
                   "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "esc"]
    # Markup list
    key_list = [0] * 26

    # Cursor position
    x_pos = 960
    y_pos = 531
    with open("Markup.csv", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        while True:
            # Capture Minecraft windows
            img = ImageGrab.grab(window_pos)

            # Mouse movement control
            if mouse_cont.position[0] > x_pos + 1:
                key_list[10] = 1
            elif mouse_cont.position[0] < x_pos - 1:
                key_list[11] = 1
            if mouse_cont.position[1] > y_pos + 4:
                key_list[12] = 1
            elif mouse_cont.position[1] < y_pos - 4:
                key_list[9] = 1

            # Control mouse button
            if mouse.is_pressed(mouse.LEFT):
                key_list[13] = 1
            if mouse.is_pressed(mouse.RIGHT):
                key_list[14] = 1

            # Control keyboard key
            for i in range(len(name_button)):
                if name_button[i] != None:
                    if keyboard.is_pressed(name_button[i]):
                        key_list[i] = 1

            # Save image every 5 tick
            if n == 5:
                # Change the image color to the rgb
                img = np.array(img)[:, :, ::-1]
                # Resize image
                img = cv2.resize(img, (800, 400))
                # Show the capture window
                # cv2.imshow(f"screen{n}",img)
                # Save image
                path = f"Image\{count}.jpg"
                cv2.imwrite(path,img)
                print(key_list)
                file_writer.writerow(key_list)
                count += 1
                n = 0
                key_list = [0] * 26
            else:
                n += 1
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()

start_grab(0,count)

def show_mouse_pos():
    while True:
        print(mouse_cont.positin)
