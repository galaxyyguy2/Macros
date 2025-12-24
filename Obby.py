from pynput import keyboard
from PIL import ImageGrab
import pydirectinput
import numpy as np
import threading
import time
import cv2
import sys
import os
import functools
import ctypes
import pygetwindow as gw
import win32gui, win32con, win32api
from pywinauto import Application

try:
    from ahk import AHK
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    bundled_ahk = os.path.join(base_path, 'AutoHotkey.exe')
    installed_ahk = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"

    ahk_exe_path = bundled_ahk if os.path.exists(bundled_ahk) else installed_ahk
    ahk = AHK(executable_path=ahk_exe_path)
except Exception as e:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"AutoHotkey could not be loaded from either bundled or installed path.\n\nError: {e}",
        "AutoHotkey Error",
        0x10
    )
    sys.exit()

# auto res
res_info = 0
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if screen_width == 2560 and screen_height == 1440:
    res_info = 2560
    temp = (0, 0)
    reconnectui = (1408, 758), (61, 59, 57)
    reconnectbutton = 1396, 823
    tpmenu = (2337, 137), (71, 61, 245)
    bgsiplay = (1406, 708), (218, 205, 179)
    bgsiplay2 = (1406, 708)
    bgsiplay3 = (1603, 623), (233, 166, 28)
    bgsiplay4 = (1603, 623)
    tpbut = (1273, 1362)
    upbut = (1711, 442)
    island = (932, 1087)
elif screen_width == 1920 and screen_height == 1080:
    res_info = 1920
    temp = (0, 0)
    reconnectui = (1090, 581), (61, 59, 57)
    reconnectbutton = (1121, 638)
    tpmenu = (1745, 134), (74, 41, 222)
    bgsiplay = (1067, 541), (15, 245, 140)
    bgsiplay2 = (1067, 541)
    bgsiplay3 = (1234, 457), (233, 166, 28)
    bgsiplay4 = (1234, 457)
    tpbut = (964, 1012)
    upbut = (1325, 301)
    island = (663, 857)
else:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Please either use 2560x1440 or 1920x1080 resolution and set your scale to 100% for this macro to work.\nCurrent resolution: {screen_width}x{screen_height}",
        "Invalid resolution",
        0x10
    )
    sys.exit()

print = functools.partial(print, flush=True)

def auto_reconnect(): # not used cause its just so i remember the thing
    if detect_color(*reconnectui):
        move(*reconnectbutton)

def reconnectbuttons(): # not used cause its just not working
    if detect_color(*bgsiplay):
        move(*bgsiplay2)
    if not detect_color(*bgsiplay):
        print("man idk i didnt detect shit")
    time.sleep(5)
    if detect_color(*bgsiplay3):
        move(*bgsiplay4)
    if not detect_color(*bgsiplay3):
        print("man idk i didnt detect shit")
    time.sleep(10)

def reconnectbuttonssimpler():
    move(*bgsiplay2)
    time.sleep(7.5)
    move(*bgsiplay4)
    time.sleep(10)
    pressedplay = True

# coord recalculation
def convert(original_coords, original_resolution=(2560, 1440)):
    global user_width, user_height
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    user_width = root.winfo_screenwidth()
    user_height = root.winfo_screenheight()
    new_x = int(original_coords[0] * (user_width / original_resolution[0]))
    new_y = int(original_coords[1] * (user_height / original_resolution[1]))
    return new_x, new_y

# global names
TIME_switch = keyboard.Key.f1
ON_switch = keyboard.Key.f2
OFF_switch = keyboard.Key.f3

# others
running_flag = False    
total_time = ""


# function to format elapsed time into hh:mm:ss
def format_time_ignore(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# function to update session time in the background
def update_session_time_ignore():
    global total_time
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        total_time = format_time_ignore(elapsed_time)
        time.sleep(1)

# Start the session time update thread
session_time_thread = threading.Thread(target=update_session_time_ignore, daemon=True)
session_time_thread.start()

# clearing the cmd
def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def move(target_x, target_y):
    ahk.mouse_move(target_x, target_y)
    pydirectinput.click(target_x, target_y)

def nomove(x, y):
    ahk.mouse_move(x, y)

def detect_color(coords, target_color, tolerance=20):
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    bgr_color = img[coords[1], coords[0]]
    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    diff = np.abs(np.array(bgr_color, dtype=int) - np.array(target_color_bgr, dtype=int))
    return np.all(diff <= tolerance)

pressedplay = False

cls()
print('Obby Macro by galaxy_guy2')
print('')
print("Macro running correctly")
print("To start press F2, to stop press F3")
def action_loop():
    while True:
        if running_flag:
            if detect_color(*reconnectui):
                print("damnn u disconnected how unfortunate")
                move(*reconnectbutton)
                time.sleep(45)
                reconnectbuttonssimpler()
                if not pressedplay:
                    print("yeah idk i fucked something up man")
                else:
                    print("yooo i did it!! i pressed play!1!1!!")
                if not detect_color(*reconnectui):
                    print("damnn sweet u reconnected how fortunate")
            time.sleep(2)
            print("works")
            pydirectinput.press('m')
            time.sleep(5)
            for _ in range(11):
                move(*upbut)
                time.sleep(0.2)
            time.sleep(0.5)
            move(*island)
            time.sleep(0.5)
            move(*tpbut)
        else:
            time.sleep(0.4)

# on/off switch with f2 and f3 keys
def toggle_switch(key):
    global running_flag, total_time
    if key == ON_switch:
        running_flag = not running_flag
        if running_flag:
            print(f"Script started...".ljust(60), end="\r")
        if not running_flag:
            print(f"Script paused...".ljust(60), end="\r")
    elif key == OFF_switch:
        print(f"Script stopped".ljust(60), end="\r")
        elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_time.split(":"))))
        
        if elapsed_seconds >= 3600:
            message = (
                f"Hello!\n\n"
                f"You have been using this macro for {total_time} hour(s).\n\n"
                f"These macros take me a long time to make, so I'd be grateful if you left a tip :)"
            )
            result = ctypes.windll.user32.MessageBoxW(
                0,
                message,
                "Thank you!",
                0x1044
            )
            if result == 6:
                import webbrowser
                webbrowser.open("https://ko-fi.com/lisek_guy2/tip")
        
        sys.exit()
    elif key == TIME_switch:
        print(f"Time elapsed: {total_time}")

with keyboard.Listener(on_press=toggle_switch) as listener:
    action_thread = threading.Thread(target=action_loop)
    action_thread.daemon = True
    action_thread.start()
    listener.join()
