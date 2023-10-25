import cv2
import numpy as np
import pyautogui
import pygetwindow
import keyboard
class Capture:
    def __init__(self,window_title):
        self.window_title = window_title
    def take_screenshot(self):
        try:
            # Find the window by its title
            window = pygetwindow.getWindowsWithTitle(self)[0]
            x, y, width, height = window.left, window.top, window.width, window.height

            margin = [15,15,30,30] #top left width height
            # Capture the screenshot
            screenshot = pyautogui.screenshot(region=(x + margin[0], y + margin[1], width - margin[2], height - margin[3]))

            return np.array(screenshot)

        except IndexError:

            print("Window not found.")
            return np.ones((228,228,1))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return np.ones((228,228,1))


    while True:
        screen = take_screenshot(window_title)
        screen = cv2.resize(screen,(500,500))
        cv2.imshow("hi",screen)
        if cv2.waitKey(10) & keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            break
