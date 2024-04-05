import cv2
import numpy as np
import pyautogui
board_color = [189, 189, 189]

#Used to find the game boarder
def find_game_board_coords():
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR) #cv2 uses BGR instead of RGB which we screenshot in
    x, y, w, h = find_biggest_contour(screenshot, board_color)
    return x, y, w, h

#Takes in color and an image. Returns ALL countours
def find_all_contour(image, color=board_color):
    lower_bound = np.array([color[2]-1, color[1]-1, color[0]-1]) #Converts our RGB to BGR
    upper_bound = np.array([color[2]+1, color[1]+1, color[0]+1])

    mask = cv2.inRange(image, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

#
def find_biggest_contour(image, color):
    lower_bound = np.array([color[2]-1, color[1]-1, color[0]-1]) #Converts our RGB to BGR
    upper_bound = np.array([color[2]+1, color[1]+1, color[0]+1])

    mask = cv2.inRange(image, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = None
    biggest_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > biggest_area:
            biggest_area = area
            biggest_contour = contour
    x, y, w, h = cv2.boundingRect(biggest_contour)
    return x, y, w, h

