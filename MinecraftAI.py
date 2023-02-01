import keras.layers
import numpy as np
import cv2
from PIL import ImageGrab
import pyautogui
import time
import win32gui
import win32con
from pynput.keyboard import Key,Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button

print('start')

# Function with keyboard event exapmles
def key_mouse():
    monitor_size = pyautogui.size()
    print(monitor_size)
    player_center = pyautogui.position()
    print(player_center[0])
    current_mouse_pos = list(player_center)
    keyboard = KeyboardController()
    mouse = MouseController()
    #keyboard.tap("w")
    #keyboard.touch("w",is_press = True)
    keyboard.press("w")
    keyboard.press(Key.ctrl)

# Function for getting screen sizes

def GetWindowSize():

    # Get full window name with Minecraft into window name
    mine_wind = ""
    for i in pyautogui.getAllWindows():
        if "Minecraft" in i.title:
            mine_wind = i.title

    # Find window with name Minecraft
    window = win32gui.FindWindow(None,mine_wind)

    # Show window
    win32gui.ShowWindow(window,win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(window)

    # Change window size
    window_size = [0,0,1920,1040]
    win32gui.MoveWindow(window,window_size[0],window_size[1],window_size[2],window_size[3],True)
    # Window size for grabbing
    window_size = [10, 30, 1920, 1040]
    return window_size

wind_size = GetWindowSize()

time.sleep(2)

# Import model
model = keras.models.load_model("firstMinecraftAIV3.h5")

# Create mouse and keyboard controllers
keyboard = KeyboardController()
mouse = MouseController()

# Release all buttons and keys
name_button = ["w", "a", "s", "d", "e", "q",
                   "1", "2", "3", "4", "5", "6", "7", "8", "9","left",
                    "shift", "ctrl","esc"]

for i in name_button:
    print('start',i)
    if i == "shift":
        keyboard.release(Key.shift)
    elif i == "ctrl":
        keyboard.release(Key.ctrl)
    elif i == "left":
        mouse.release(Button.left)
    elif i == "esc":
        keyboard.release(Key.esc)
    else:
        keyboard.release(i)

# Function for using prediction results
def Mine_AI(pred,check_list):

    name_button = ["w", "a", "s", "d", "shift", "ctrl", "space", "e", "q",
                   "move_up", "move_right", "move_left", "move_down", "left", "right",
                   "1", "2", "3", "4", "5", "6", "7", "8", "9", "esc"]

    for i in range(len(pred[0])):
        if pred[0][i] > 0.2:
            if name_button[i] == "shift" :
                print("Shift")
                keyboard.press(Key.shift)
                check_list[i] = 1
            elif name_button[i] == "ctrl":
                print("ctrl")
                keyboard.press(Key.ctrl)
                keyboard.release(Key.ctrl)
                check_list[i] = 0
            elif name_button[i] == "move_up":
                print("up")
                check_list[i] = 2
                pyautogui.move(0, -100)
            elif name_button[i] == "move_down":
                print("down")
                check_list[i] = 2
                pyautogui.move(0, 100)
            elif name_button[i] == "move_right":
                print("right")
                check_list[i] = 2
                pyautogui.move(100, 0)
            elif name_button[i] == "move_left":
                print("left")
                check_list[i] = 2
                pyautogui.move(-100, 0)
            elif name_button[i] == "left":
                print("mouseleft")
                mouse.press(Button.left)
            elif name_button[i] == "right":
                mouse.click(Button.left)
                check_list[i] = 0
                print("mouseright")
                #mouse.press(Button.right)
            elif name_button[i] == "space":
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                check_list[i] = 0
            elif name_button[i] == "esc":
                keyboard.press(Key.esc)
                check_list[i] = 1
            else:
                print(name_button[i])
                keyboard.press(name_button[i])
                check_list[i] = 1

        # Release buttons and keys
        elif check_list[i] == 1:
            if name_button[i] == "left":
                mouse.release(Button.left)
                check_list[i] = 0
            elif name_button[i] == "shift":
                print("stop - Shift")
                keyboard.release(Key.shift)
                check_list[i] = 0
            else:
                print(f"yes - {name_button[i]}")
                keyboard.release(name_button[i])
                check_list[i] = 0

# Capturing the game window
def grab_monitor(window_pos):
    image_list = [1]
    check_list = [0] * 25
    while True:
        # Capture Minecraft windows
        img = ImageGrab.grab(window_pos)

        # Change the image color to the rgb
        img = np.array(img)[:,:,::-1]
        # Resize image
        img = cv2.resize(img, (400, 200))

        image_list[0] = img
        image = np.array(image_list)

        result = model.predict(image)
        Mine_AI(result,check_list)
        print(result)

        # Show the capture window
        #cv2.imshow("screen",img)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

grab_monitor(wind_size)

# Model pattern
def CNNmodel():
    model = keras.Sequential()
    # ---Trying change the filter size---
    model.add(keras.layers.Conv2D(32,(60,60),padding = "same",activation = "relu",input_shape=(382,162,3)))
    model.add(keras.layers.MaxPooling2D((2,2),strides = 2))
    # ---Trying change the filter size and numbers of the filters---
    model.add(keras.layers.Conv2D(64,(60,60), padding="same", activation="relu"))
    model.add(keras.layers.MaxPooling2D((2, 2), strides=2))
    # Size of the exit vector - 15x15x64
    model.add(keras.layers.Flatten())

    # ---Trying change number of the neurons---

    model.add(keras.layers.Dense(128,activation = "relu"))
    model.add(keras.layers.Dense(25,activation = "sigmoid"))

    print(model.summary())