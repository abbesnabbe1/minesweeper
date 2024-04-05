from image_location import *

test_template = "img/board100.png"
test_image = "img/fake_screen.png"

template = cv2.imread(test_template, cv2.IMREAD_GRAYSCALE)
image = cv2.imread(test_image, cv2.IMREAD_GRAYSCALE)

def resize_image(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

if __name__ == '__main__':
    print('Starting...')
    print("Original size:")
    find_template_in_image(template, image)

    print("Resized 2x:")
    resized_template = resize_image(image, 0.3)
    find_template_in_image(resized_template, image)
    print("Done!")