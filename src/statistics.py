import numpy as np
import pandas as pd
import matplotlib.cm as cm

import files
import config
import math
import imageio
import cv2
import os

from PIL import Image
from os.path import join


from crust_slices import get_angle, annulus_mask


class StatTracker:
    """
    This is a Singleton tracker that records the tube coverage and slice area statistics. The initialization must supply
    radial_precision and slice_count.

    It might be worth refactoring this to be a module.

    ...

    Attributes
    ----------
    __instance: StatTracker
        if not None, reference to the one StatTracker in existence
    coverage_stats: arr
        2D boolean data array for tube coverage statistics

    Methods
    -------
    get_instance()
        If __instance is None, instantiates a new StatTracker. Otherwise, returns the reference to the StatTracker.
    initialize_matrix(rows, cols)
        Initializes stats to be a 2D array of False, with dimensions rows by cols
    update_area(row, col, value)
        Sets the row, col element of stats to boolean value
    get_stats():
        Returns a 2D array of integers, 0 or 1, representing stats
    """

    __instance = None
    coverage_stats = []
    area_stats = []

    @staticmethod
    def get_instance():
        """Static access method."""
        if StatTracker.__instance is None:
            StatTracker()
        return StatTracker.__instance

    def __initialize_coverage(self):
        # Setting dtype to np.bool_ makes np interpret the 0's as Falses
        self.coverage_stats = np.zeros(
            (files.Files.slice_total, config.num_wedges), dtype=np.bool_
        )

    def __initialize_area(self):
        self.area_stats = np.zeros((files.Files.slice_total,), dtype=np.uint8)

    def update_coverage(self, wedge, value: bool):
        self.coverage_stats[files.Files.current_slice][wedge] = value

    def update_area(self, slice_index, value):
        self.area_stats[slice_index] = value

    def get_stats(self):
        """returns coverage and area stats. Coverage stats are returned as a 0/1 array rather than a boolean array"""
        coverage_stats = np.where(self.coverage_stats, 1, 0)
        return coverage_stats, self.area_stats

    def __init__(self):
        """Virtually private constructor."""
        if StatTracker.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            StatTracker.__instance = self
            self.__initialize_area()
            self.__initialize_coverage()


def save_png_to_gif(folder, save_path):
    """
    Combines the images in folder into a gif lasting duration seconds, and saves that gif to save_path

    :param str folder: Folder to read image files from. Precondition: contains only PNG and JPEG files.
    :param str save_path: Save path for output GIF. Precondition: ends in ".gif"
    :param duration: Length of output gif in seconds. Defaults to 30.
    """
    assert save_path.endswith(".gif"), "Save path must end in .gif"
    with imageio.get_writer(save_path, mode="I") as frames:
        for file in os.listdir(folder):
            # NOTE: cv2 imread accepts more than just these file extensions, but they can be os dependent. See the imread doc for more
            file_endings = [
                file.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".bmp"]
            ]
            assert True in file_endings, "Files to be combined must be an image format"
            new_frame = cv2.imread(join(folder, file), color="RGB")
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
                    slice_intensities[int(get_angle(i, j, center) / slice_angle)]
                )[:3]

                img[i][j] = [255 * a for a in [B, G, R]]
    cv2.imwrite(join(save_folder, "heatmap.png"), img)
