import numpy as np
import pandas as pd
import matplotlib.cm as cm
import cv2
import os
from os.path import join
import math
import imageio
from PIL import Image


from crust_slices import get_angle, annulus_mask


def save_png_to_gif(folder, save_path, duration=30):
    """
    Combines the images in folder into a gif lasting duration seconds, and saves that gif to save_path

    :param str folder: Folder to read image files from. Precondition: contains only PNG and JPEG files.
    :param str save_path: Save path for output GIF. Precondition: ends in ".gif"
    :param duration: Length of output gif in seconds. Defaults to 30.
    """
    assert save_path.endswith(".gif"), "Save path must end in .gif"
    frames = []
    with imageio.get_writer("smiling.gif", mode="I") as writer:
        for file in os.listdir(folder):
            assert file.endswith(".png") or file.endswith(
                ".jpg"
            ), "Files to be combined must be PNG or JPEG format"
            new_frame = Image.open(
                join(folder, file)
            )  # I've only tried this with png, not jpeg. Not sure if you can mix them
            frames.append_data(new_frame)


def save_coverage_stats(source, save_folder, col_count):
    """
    Takes either an excel filepath or an array to extract coverage statistics and save them.
    :param source: Source of the data to be processed, either as an excel filepath or as an array.
    :param save_folder: Folder to save the heatmap and coverage statistics to
    :param col_count: The number of wedges in the tracker data to be analyzed
    """
    if isinstance(source, str) and source.endswith(".xlsx"):
        cols = [i for i in range(col_count + 1) if i != 0]
        array = pd.read_excel(source, usecols=cols).to_numpy()
    else:
        array = source

    try:
        rows, cols = array.shape
    except:
        raise ValueError("Source must be a numpy array or excel filepath!")

    slice_intensities = np.round(np.sum(array, 0) / rows, 4)

    to_write = open(join(save_folder, "coverage stats.txt"), "w")
    to_write.write(
        "This is the total tube coverage: "
        + str(np.round(np.sum(array) / (cols * rows), 4))
    )
    to_write.write("\nList of intensities by slice: " + str(slice_intensities))
    to_write.close()

    # The following makes a nice heatmap
    img = 255 * np.ones((300, 300, 3), np.uint8)
    center = (150, 150)
    annulus = annulus_mask(img.shape[:2], center, 50, 30)
    slice_angle = 2 * math.pi / col_count
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if annulus[i][j] == 255:
                R, G, B = cm.cividis(
                    slice_intensities[int(
                        get_angle(i, j, center) / slice_angle)]
                )[:3]

                img[i][j] = [255 * a for a in [B, G, R]]
    cv2.imwrite(join(save_folder, "heatmap.png"), img)
