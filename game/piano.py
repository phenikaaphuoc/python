import keyboard
import win32api,win32con
import time
import pyautogui
import numpy
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
pyautogui.displayMousePosition()
# click(40,1027)
height = 1055

width = 1006,1178,1340,1522
oke = 0
while keyboard.is_pressed("q")==False:
    if keyboard.is_pressed("a"):
        oke = 1
    if oke:
        for w in width:
            print(pyautogui.pixel(w,height))
            if pyautogui.pixel(w,height)[0]==0:
                click(w,height)
                print("oke")