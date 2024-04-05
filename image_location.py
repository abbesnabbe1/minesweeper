import cv2
import numpy as np

def find_template_in_image(template, image, threshold = 0.5, method_input = cv2.TM_CCOEFF_NORMED):
    
    method = method_input
    res = cv2.matchTemplate(image, template, method)

    max_val, max_loc = cv2.minMaxLoc(res)[1], cv2.minMaxLoc(res)[3]
    if max_val >= threshold:
        print(f'Template found with value: {max_val}')
        cv2.imshow('Template', template)
    else:
        print('Template not found in image.')