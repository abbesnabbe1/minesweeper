#INIT
import time
import pyautogui
from PIL import Image
import numpy as np
from PIL import ImageDraw

field_width = 0
field_height = 0
rows = 0
cols = 0
top_left = (0, 0)

box_width = 0
box_height = 0

cur_screenshot = None

def init_logic(field_width_in, field_height_in, rows_in, cols_in, top_left_in):
    global field_width, field_height, rows, cols, top_left
    field_width = field_width_in-2
    field_height = field_height_in-2
    rows = rows_in
    cols = cols_in
    top_left = top_left_in[0]+2, top_left_in[1]+2

    global box_width, box_height
    box_width = (field_width)/cols
    box_height = (field_height)/rows

def update_screen():
    global cur_screenshot
    cur_screenshot = pyautogui.screenshot(region=(top_left[0], top_left[1], field_width, field_height))

def click_all_corners():
    click_box_number(0, 0)
    click_box_number(cols-1, 0)
    click_box_number(0, rows-1)
    click_box_number(cols-1, rows-1)

def coords_to_box_number(x, y):
    global field_width, field_height, top_left
    x -= top_left[0]
    y -= top_left[1]
    return x//(box_width), y//(box_height)

def box_number_to_coords(x, y):
    global field_width, field_height, top_left
    x = (top_left[0] + x*box_width + box_width/2) -1 #Small adjustment to fix centering
    y = (top_left[1] + y*box_height + box_height/2) -1
    return x,y

def click_box_number(x,y):
    x,y = box_number_to_coords(x,y)
    pyautogui.click(x, y)

def get_nearby_boxes(x,y):
    x,y = box_number_to_coords(x,y)
    x -= top_left[0]
    y -= top_left[1]
    test = cur_screenshot.crop((x-(box_width*1.5), y-(box_height*1.5), x+(1.5*box_width), y+(1.5*box_height)))
    print(np.array(test))
    test.save("test.png")

#Empty = (189x3), Flag = (0x3), 1 = (0,0,255), 2 = (0,123,0), 3 = (255,0,0), 
#4 = (0,0,123) 5 = (123,0,0), 6 = (0,123,123), 7 = ?sus lets just hope it wont appear, 8 = (123,123,123)
def get_box_item(x,y):
    x,y = box_number_to_coords(x,y)
    x -= top_left[0]
    y -= top_left[1]
    #print(np.array(test))
    color = (cur_screenshot.getpixel((x+4,y+5)))
    if color == (189,189,189):
        return -1
    elif color == (0,0,0):
        return 0
    elif color == (0,0,255):
        return 1
    elif color == (0,123,0):
        return 2
    elif color == (255,0,0):
        return 3
    elif color == (0,0,123):
        return 4
    elif color == (123,0,0):
        return 5
    elif color == (0,123,123):
        return 6
    elif color == (123,123,123):
        return 8

#
#  DEBUG FUNCTIONS
#
def size_test():
    copy = cur_screenshot.copy()
    draw = ImageDraw.Draw(copy)
    purple = (128, 0, 128)  # RGB color for purple

    for i in range(cols):
        for j in range(rows):
            # Calculate the coordinates of the center of the box
            x, y = box_number_to_coords(i, j)
            x -= top_left[0]
            y -= top_left[1]

            # Draw a 3x3 purple square at the center of the box
            draw.rectangle([(x, y), (x+1, y+1)], fill=purple)

    copy.save("screenshot_with_squares.png")

def sweep_box(x,y):
    #need to handle edge cases when we are at the edge of the board
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            if j #CONTINUE HERE!