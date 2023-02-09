import time

import numpy as np
import cv2
from PIL import ImageGrab
from pynput.keyboard import Key,Controller as KeyboardController
from pynput.mouse import Button,Controller as MouseController
import mouse, keyboard
import csv
from win32gui import GetWindowText, GetForegroundWindow
from win32api import GetSystemMetrics
# Keyboard and mouse controller
keyboard_cont = KeyboardController()
mouse_cont = MouseController()

# Windows size
window_pos = [10, 30, 1920, 1040]
n = 0
count = 1


# Main function
def start_grab(n,count):
    print("start")
    # Button name
    name_button = ["w", "a", "s", "d","shift", "ctrl","space", "e", "q",
                   None,None,None,None,None,None,
                   "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "esc"]
    # Markup list
    key_list = [0] * 26
    mine_wind = ""
    # Cursor position
    x_pos = GetSystemMetrics(0)/2
    y_pos = 0
    with open("Markup.csv", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")

        while True:
            if "Minecraft" in GetWindowText(GetForegroundWindow()):
                if y_pos >= GetSystemMetrics(1)/2 + 3 or y_pos <= GetSystemMetrics(1)/2 - 10:
                    y_pos = mouse_cont.position[1]
                    print(x_pos,y_pos)
                    continue

                # Capture Minecraft windows
                img = ImageGrab.grab(window_pos)

                # Mouse movement control
                if mouse_cont.position[0] > x_pos + 15:
                    key_list[10] = 1
                elif mouse_cont.position[0] < x_pos - 15:
                    key_list[11] = 1
                    #print("left")
                if mouse_cont.position[1] > y_pos + 10:
                    key_list[12] = 1
                    #print("down")
                elif mouse_cont.position[1] < y_pos - 10:
                    #print("up")
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
                    key_list[25] = f"{count}.jpg"
                    #print(key_list)
                    file_writer.writerow(key_list)
                    w_file.flush()
                    count += 1
                    n = 0
                    key_list = [0] * 26
                else:
                    n += 1
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    cv2.destroyAllWindows()

start_grab(n,count)
def show_mouse_pos():
    while True:
        print(mouse_cont.position)

# 683 384
def get_active_window():
    while True:
        print(type(GetWindowText(GetForegroundWindow())))

def get_windows():
    print(GetSystemMetrics(0)/2,GetSystemMetrics(1)/2)

def create_csv():
    output = ["Foo", "Bar"]

    f = open("filename.csv", "a")
    w = csv.writer(f, delimiter=",", lineterminator="\r")
    w.writerow(output)
    w.writerow(output)
    w.writerow(output)
    f.close()

#create_csv()
#show_mouse_pos()
#get_windows()
#get_active_window()
