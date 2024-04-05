from image_location import *
import time
import keyboard
import pyautogui

#Image template
test_template = "img/board100.png"
test_image = "img/fake_screen.png"

#Image loaded with cv2
template = cv2.imread(test_template)
image = cv2.imread(test_image)

if __name__ == '__main__':
    print('Starting...')
    time.sleep(3)

    while keyboard.is_pressed('q') == False:
        game_board_region = find_game_board_coords() # (x, y, w, h)
        screenshot = pyautogui.screenshot(region=game_board_region)
        
        image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR) #cv2 uses BGR instead of RGB which we screenshot in
        x, y, w, h = find_biggest_contour(image, [123,123,123])
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.imshow('All Positions', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Done, waiting 10 seconds...")
        time.sleep(10)
    print("Done!")