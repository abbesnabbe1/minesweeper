#INIT
import time
import pyautogui
from PIL import Image
import numpy as np
from PIL import ImageDraw
import cv2
from image_location import *
import random

field_width = 0
field_height = 0
rows = 0
cols = 0
top_left = (0, 0)

box_width = 0
box_height = 0

finished_list = []
active_list = []
old_active_list = []
item_map = []

prev_screenshot = None
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

    global item_map #Init item map to ?
    item_map = [x[:] for x in [["?"] * cols] * rows]

def run_logic():
    click_box_number(0,0)
    update_screen()
    for i in range(50):
        print("loop")
        if (update_active() == False): #Nothing changed, we need to risk a random click!
            rand_x = random.randint(0, cols-1)
            rand_y = random.randint(0, rows-1)
            click_box_number(rand_x, rand_y)
            update_screen()

            if (pressed_bomb(rand_x, rand_y)):
                print("Game over!")
                break
        else:
            print("Active list: ", active_list)
            for box in active_list:
                print("looking at: ", box)
                
                #Skip flags and empty boxes
                if(item_map[int(box[0])][int(box[1])] == "flag" or item_map[int(box[0])][int(box[1])] == "empty"):
                    print("Skip")
                    continue
                
                neighbors = get_neighbors(box[0], box[1])
                neighbors_item = [x[0] for x in neighbors]

                print(neighbors_item.count("flag") + neighbors_item.count("?"))
                #Mine found!
                if(item_map[int(box[0])][int(box[1])] == (neighbors_item.count("flag") + neighbors_item.count("?"))):
                    print("Mine found!")
                    for neighbor in neighbors:
                        if neighbor[0] == "?":
                            flag_box_number(int(neighbor[1][0]), int(neighbor[1][1]))
                            item_map[int(neighbor[1][0])][int(neighbor[1][1])] = "flag"
                            time.sleep(0.1)

                #Reveal land!
                elif(item_map[int(box[0])][int(box[1])] == neighbors_item.count("flag")):
                    print("Reveal land!")
                    for neighbor in neighbors:
                        if neighbor[0] == "?":
                            click_box_number(int(neighbor[1][0]), int(neighbor[1][1]))
                            time.sleep(0.1)
            update_screen()
        
def update_active():
    global active_list, finished_list, old_active_list, item_map
    changed_boxes = get_changed_boxes()
    print("Changed boxes: ", changed_boxes)
    for box in changed_boxes:
        active_list.append(box)
    for box in active_list:
        item_map[int(box[0])][int(box[1])] = get_box_item(box[0], box[1])
    new_active_list = []
    for box in active_list:
        neighbors = get_neighbors(box[0], box[1])
        neighbors_item = [x[0] for x in neighbors]
        if neighbors_item.count("?") != 0:
            new_active_list.append(box)
        else:
            finished_list.append(box)
    active_list = new_active_list
    if old_active_list == active_list:
        return False
    else:
        old_active_list = active_list.copy()
        return True

def pressed_bomb(x,y):
    x_nr, y_nr = x, y
    x,y = box_number_to_coords(x,y)
    x -= top_left[0]
    y -= top_left[1]
    color = (cur_screenshot.getpixel((x+8,y+5)))
    if color == (255,0,0):
        return True
    else:
        return False

def update_screen():
    global cur_screenshot, prev_screenshot
    prev_screenshot = cur_screenshot
    cur_screenshot = pyautogui.screenshot(region=(top_left[0], top_left[1], field_width, field_height))

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

def flag_box_number(x,y):
    x,y = box_number_to_coords(x,y)
    pyautogui.rightClick(x, y)

#Empty = (189x3), Flag = (0x3), 1 = (0,0,255), 2 = (0,123,0), 3 = (255,0,0), 
#4 = (0,0,123) 5 = (123,0,0), 6 = (0,123,123), 7 = ?sus lets just hope it wont appear, 8 = (123,123,123)
def get_box_item(x,y):
    x_nr, y_nr = x, y
    x,y = box_number_to_coords(x,y)
    x -= top_left[0]
    y -= top_left[1]
    color = (cur_screenshot.getpixel((x+4,y+5)))
    if color == (189,189,189):
        box = get_box_image(x_nr, y_nr)
        box_converted = cv2.cvtColor(np.array(box), cv2.COLOR_RGB2BGR)
        _, _, _, _, size = find_biggest_contour(box_converted, [189,189,189])
        if size > 200:
            return "empty"
        else:
            return "?"
    elif color == (0,0,0):
        return "flag"
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

def get_box_image(x,y):
    x,y = box_number_to_coords(x,y)
    x -= top_left[0]
    y -= top_left[1]
    return cur_screenshot.crop((x-(box_width/2), y-(box_height/2), x+(box_width/2), y+(box_height/2)))

def get_changed_boxes():
    # Convert the images to numpy arrays
    np_image1 = np.array(prev_screenshot)
    np_image2 = np.array(cur_screenshot)

    # Calculate the absolute difference between the two images
    diff = np.abs(np_image1 - np_image2)

    # Convert the difference image to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    # Threshold the difference image to create a binary mask
    _, mask = cv2.threshold(diff_gray, 0, 255, cv2.THRESH_BINARY)

    # Find the coordinates of the changed pixels
    changed_pixels = np.where(mask != 0)

    # Calculate the box numbers of the changed pixels
    changed_boxes = set()
    for x, y in zip(changed_pixels[1], changed_pixels[0]):
        box_number = coords_to_box_number(x+top_left[0], y+top_left[1])
        changed_boxes.add(box_number)
    return changed_boxes

def get_neighbors(x, y):
    neighbors = []
    for i in range(max(-1, -int(x)), min(2, cols - int(x))):
        for j in range(max(-1, -int(y)), min(2, rows - int(y))):
            if i == 0 and j == 0:
                continue
            neighbors.append(((item_map[int(x+i)][int(y+j)]), (x+i, y+j)))
    return neighbors

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

def debug_n_count(x,y):
    neighbors = get_neighbors(x,y)
    print(neighbors)
    print("Flag count: ", neighbors.count("flag"))
    print("? count: ", neighbors.count("?"))