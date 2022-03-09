import cv2
import numpy as np
import pandas as pd
from os.path import join

# from tqdm import tqdm
from epoxy import find_epoxy
import files

# from PIL import Image

from epoxy import find_epoxy
from stat_tracker import StatTracker
from tube_analysis import get_bound_circ
import tracker_analysis

red = np.full((250, 500, 3), [0, 0, 255], dtype=np.uint8)


def person_output(img, color, epoxy_mask, circle):
    """Takes in the raw image, base color, epoxy mask, and circle to make a nice processed image"""

    x, y, r = circle
    a = cv2.bitwise_and(img, color, mask=epoxy_mask)
    epoxy_mask = 255 - epoxy_mask
    b = cv2.bitwise_and(img, img, mask=epoxy_mask)
    pretty = cv2.bitwise_or(a, b)
    cv2.circle(pretty, (x, y), r, (255, 0, 0), 1)
    return pretty


def write_tube_img(radius=33):
    """Saves the image of the tube with selected radius"""
    tube_input = files.get_tube_sample()
    circ = get_bound_circ(tube_input, radius)
    x, y = circ[:2]
    tube_file = tube_input.copy()
    cv2.circle(tube_file, (x, y), radius, (255, 0, 0), 1)
    cv2.imwrite("src/gui/res/tube_sample.png", tube_file)


def write_image_sample(params):
    img, tube = files.get_image_sample()
    processed_mask, tube_info = find_epoxy(img, tube, params)
    cv2.imwrite(
        "src/gui/res/settings_sample.png",
        person_output(img, red, processed_mask, tube_info),
    )


def write_image(params):
    img, tube = files.get_next()
    processed_mask, tube_info = find_epoxy(img, tube, params)
    files.save_file(person_output(img, red, processed_mask, tube_info))


# tracker = StatTracker.get_instance(precision, files.get_total())


# for i in tqdm(range(total_slices)):

#     epox, circle = find_epoxy(img_cropped, tube_cropped, rad, i, precision)
#     cv2.imwrite(
#         processed_path + "\\processed_" + files[i],
#         person_output(img_cropped, red, epox, circle),
#     )


# df = pd.DataFrame(tracker.get_stats())
# df.to_excel(join(folder, "Coverage data.xlsx"))
# tracker_analysis.save_coverage_stats(
#     df.to_numpy(), save_folder=folder, col_count=precision
# )
# tracker_analysis.save_png_to_gif(processed_path, join(folder, "processed.gif"))


# cv2.imshow("Tube with selected radius", tube_file)
# cv2.waitKey(0)
# response = input("Is the current radius good? (y/n)")
# assert response == "y" or response == "n", "Must be y or n"
# if response == "y":
#     return radius
# else:
#     inp = input("Input a different radius (int)")
#     assert float(inp).is_integer(), "Inputted radius must be an integer"
#     num = int(inp)
#     return pick_radius(tube_input, num)


# # If you ever need to just run the program with one image, just process it with cv2.imread as usual
# precision = 50  # The number of radial slices for the analysis

# # total_slices = len(files)
#
# rad = pick_radius(cv2.imread(join(tube_path, tube_files[0]))[100:350, 75:575])
