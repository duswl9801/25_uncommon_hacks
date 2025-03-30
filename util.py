import os
import time
import pyautogui as pgui

def captureandsendScreenshot():

    # capture full screen
    screenshot = pgui.screenshot()
    #dest = "C:/Users/ssun/Desktop/"
    dest = os.getcwd() + '\\screenshot\\'
    now_time = time.strftime('%Y_%m_%d_%H_%M_%S')
    screenshot = pgui.screenshot(dest + now_time + ".png")
    print(screenshot)

    return screenshot

