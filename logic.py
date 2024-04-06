#INIT
import time
import pyautogui
from PIL import Image
import numpy as np

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
    field_width = field_width_in
    field_height = field_height_in
    rows = rows_in
    cols = cols_in
    top_left = top_left_in

    global box_width, box_height
    box_width = field_width/cols
    box_height = field_height/rows

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
    print(box_width, box_height)
    return x//(box_width), y//(box_height)

def box_number_to_coords(x, y):
    global field_width, field_height, top_left
    x = top_left[0] + x*box_width + box_width/2
    y = top_left[1] + y*box_height + box_height/2
    return x,y

def click_box_number(x,y):
    x,y = box_number_to_coords(x,y)
    pyautogui.click(x, y)

def get_color_of_box(x,y):
    x,y = box_number_to_coords(x,y)
    x -= top_left[0]
    y -= top_left[1]
    tx = x + top_left[0]
    ty = y + top_left[1]
    test = pyautogui.screenshot(region=(tx-3, ty-3, 6, 6))
    print(np.array(test))
    test.save("test.png")
    color = cur_screenshot.getpixel((x, y))
    return color