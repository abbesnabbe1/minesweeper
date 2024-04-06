#INIT
import time
import pyautogui


field_width = 0
field_height = 0
rows = 0
cols = 0
top_left = (0, 0)

box_width = 0
box_height = 0

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

def click_all_corners():
    click_box_tuple(0, 0)
    click_box_tuple(cols-1, 0)
    click_box_tuple(0, rows-1)
    click_box_tuple(cols-1, rows-1)

def get_box_tuple(x, y):
    global field_width, field_height, top_left
    x -= top_left[0]
    y -= top_left[1]
    print(box_width, box_height)
    return x//(box_width), y//(box_height)

def click_box_tuple(x,y):
    global field_width, field_height, top_left
    x = top_left[0] + x*box_width + box_width/2
    y = top_left[1] + y*box_height + box_height/2
    pyautogui.click(x, y)
