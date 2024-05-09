from image_location import *
from logic import *
import time
from pynput import keyboard
import pyautogui
import traceback

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
            box_nr = coords_to_box_number(pyautogui.position()[0], pyautogui.position()[1])
            print("Box number: ", box_nr)
            pressed_bomb(box_nr[0], box_nr[1])
        
        elif key == keyboard.Key.delete: #debug for me to update screen after i press with my own mouse
            update_screen()
    
    except Exception as e:
        print(e)
        traceback.print_exc()

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
    update_screen()
    
    #Game loop here:
    for i in range(5):
        if run_logic() == True: #When all bombs are used we return True and end the loop! Else return false and continue
            break
        #Else we need to reset the game board
        x = top_left[0] + field_width/2
        y = top_left[1] + 0.07*field_height
        print("RESEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        pyautogui.click(x, y)
        init_logic(field_width, field_height, rows, cols, top_left)
        update_screen()
    print("YOU JUST WON THE GAME!")


#
if __name__ == '__main__':
    print('Starting...')
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print('Exiting complete')      