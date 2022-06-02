import cv2
import numpy as np

from epoxy import find_epoxy
import files

from epoxy import find_epoxy
from tube_analysis import get_bound_circ

# defines a red image used to make a nice output later on


def person_output(img, epoxy_mask, circle):
    """Takes in the raw image, base color, epoxy mask, and circle to make a nice processed image"""
    red = np.full((250, 500, 3), [0, 0, 255], dtype=np.uint8)

    x, y, r = circle
    a = cv2.bitwise_and(img, red, mask=epoxy_mask)
    epoxy_mask = 255 - epoxy_mask
    b = cv2.bitwise_and(img, img, mask=epoxy_mask)
    pretty = cv2.bitwise_or(a, b)
    cv2.circle(pretty, (x, y), r, (255, 0, 0), 1)
    return pretty


def write_tube_sample(radius):
    """Saves the image of the tube with selected radius"""
    tube_input = files.slices.get_tube_sample()
    circ = get_bound_circ(tube_input, radius)
    x, y = circ[:2]
    tube_file = tube_input.copy()
    cv2.circle(tube_file, (x, y), radius, (255, 0, 0), 1)
    cv2.imwrite("src/gui/res/tube_sample.png", tube_file)


def write_image_sample():
    img, tube = files.slices.get_image_sample()
    processed_mask, tube_info = find_epoxy(img, tube, save_information=False)
    cv2.imwrite(
        "src/gui/res/settings_sample.png",
        person_output(img, processed_mask, tube_info),
    )
