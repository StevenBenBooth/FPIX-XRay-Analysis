import cv2
import numpy as np
import pandas as pd
import os
from os.path import join
from tqdm import tqdm

# from PIL import Image

from epoxy import find_epoxy
from stat_tracker import StatTracker
from tube_analysis import get_bound_circ
import tracker_analysis

dataset = "Left"
folder = join(
    "D:\\Documents\\Dragonfly data\\Junior fall\\Diamond plaquette 1\\A", dataset
)
base_path = join(folder, dataset + " pictures")
tube_path = join(folder, dataset + " tube")
processed_path = join(folder, dataset + " processed")

files = os.listdir(base_path)
tube_files = os.listdir(tube_path)


def person_output(img, color, epoxy_mask, circle):
    """Takes in the raw image, base color, epoxy mask, and circle to make a nice processed image"""

    x, y, r = circle
    a = cv2.bitwise_and(img, color, mask=epoxy_mask)
    epoxy_mask = 255 - epoxy_mask
    b = cv2.bitwise_and(img, img, mask=epoxy_mask)
    pretty = cv2.bitwise_or(a, b)
    cv2.circle(pretty, (x, y), r, (255, 0, 0), 1)
    return pretty


def pick_radius(tube_input, radius=33):
    """Prompts the user to pick the radius for the tube"""

    circ = get_bound_circ(tube_input, radius)
    x, y = circ[:2]
    tube_file = tube_input.copy()
    cv2.circle(tube_file, (x, y), radius, (255, 0, 0), 1)
    cv2.imshow("Tube with selected radius", tube_file)
    cv2.waitKey(0)
    response = input("Is the current radius good? (y/n)")
    assert response == "y" or response == "n", "Must be y or n"
    if response == "y":
        return radius
    else:
        inp = input("Input a different radius (int)")
        assert float(inp).is_integer(), "Inputted radius must be an integer"
        num = int(inp)
        return pick_radius(tube_input, num)


# If you ever need to just run the program with one image, just process it with cv2.imread as usual
precision = 50  # The number of radial slices for the analysis

total_slices = len(files)
tracker = StatTracker.get_instance(precision, total_slices)
rad = pick_radius(cv2.imread(join(tube_path, tube_files[0]))[100:350, 75:575])


red = np.full((250, 500, 3), [0, 0, 255], dtype=np.uint8)
for i in tqdm(range(total_slices)):
    tube_raw = cv2.imread(join(tube_path, tube_files[i]))
    img_raw = cv2.imread(join(base_path, files[i]))

    img_cropped = img_raw[
        100:350, 75:575
    ]  # When treating image as a matrix, height then width. The OpenCV convention
    # is width then height
    tube_cropped = tube_raw[100:350, 75:575]

    epox, circle = find_epoxy(img_cropped, tube_cropped, rad, i, precision)
    cv2.imwrite(
        processed_path + "\\processed_" + files[i],
        person_output(img_cropped, red, epox, circle),
    )


df = pd.DataFrame(tracker.get_stats())
df.to_excel(join(folder, "Coverage data.xlsx"))
tracker_analysis.save_coverage_stats(
    df.to_numpy(), save_folder=folder, col_count=precision
)
tracker_analysis.save_png_to_gif(processed_path, join(folder, "processed.gif"))
