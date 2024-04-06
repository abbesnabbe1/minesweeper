from image_location import *
from logic import *
import time
from pynput import keyboard
import pyautogui

#Image template
test_template = "img/board100.png"
test_image = "img/fake_screen.png"

#Image loaded with cv2
template = cv2.imread(test_template)
image = cv2.imread(test_image)

cols, rows = 30, 16

field_width = 0  #Width of the minefield
field_height = 0 #Height of the minefield

def on_press(key):
    try:
        if key == keyboard.Key.esc:
            print("Exiting...")
            return False
        elif key == keyboard.Key.home:
            print("Running bot...")
            main_function()

        elif key == keyboard.Key.shift_r: #debug print mouse
            click_all_corners()
            #pos = pyautogui.position()
            #print("Mouse position: ", {pos})
            #print("Box tuple: ", get_box_tuple(pos[0], pos[1]))
            #click_box_tuple(29,15)
    
    except Exception as e:
        print(e)


#
#   MAIN CODE HERE:
#
def main_function():
    #Get (x, y), width height for the game board
    game_board_region = find_game_board_coords() # (x, y, w, h)
    screenshot = pyautogui.screenshot(region=game_board_region)
    
    #Get (x, y), width height for the minefield (clickable boxes!)
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR) #Convert image to cv2 BGR to then find the minefield region
    minefield_region = find_biggest_contour(image, [123,123,123])

    #Coords for the top left of minefield!
    top_left = game_board_region[0] + minefield_region[0], game_board_region[1] + minefield_region[1]
    
    #Coords for the bottom right of minefield!
    #game_board_region= (x, y, w, h), minefield_region = (x, y, w, h)
    bottom_right = game_board_region[0] + minefield_region[0] + minefield_region[2], game_board_region[1] + minefield_region[1] + minefield_region[3]
    global field_width, field_height
    field_width = minefield_region[2]
    field_height = minefield_region[3]

    #Init logic
    init_logic(field_width, field_height, rows, cols, top_left)

    #pos = list(pyautogui.position())
    #pos[0] -= (game_board_region[0] + minefield_region[0])
    #pos[1] -= (game_board_region[1] + minefield_region[1])
    #print(pos[0], pos[1])
    #print((field_width/rows), (field_height/cols))
    #print(pos[0]//(field_width/rows), pos[1]//(field_height/cols))

#
if __name__ == '__main__':
    print('Starting...')
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print('Exiting complete')      