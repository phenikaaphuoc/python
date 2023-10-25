import cv2
import numpy as np
import pyautogui
import pygetwindow
import keyboard
class Capture:
    def __init__(self,window_title):
        self.window_title = window_title
    def take_screenshot(self,margin = [15,15,30,30] ):
        try:
            # Find the window by its title
            window = pygetwindow.getWindowsWithTitle(self)[0]
            x, y, width, height = window.left, window.top, window.width, window.height

            screenshot = pyautogui.screenshot(region=(x + margin[0], y + margin[1], width - margin[2], height - margin[3]))

            return np.array(screenshot)

        except IndexError:

            print("Window not found.")
            exit()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            exit()


