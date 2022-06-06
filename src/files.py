from os.path import join
import os
import cv2
import config

"""This module contains an iterable for the slices of the scan"""

slices = None

def setup(path):
    config.set_paths(path)
    global slices
    if slices is None:
        slices = _Files(path)
    else:
        raise ValueError("The images should only be set up once")


def load_and_crop(path, slice):
    return cv2.imread(join(path, slice))[
        100:350, 75:575
    ]  # When treating image as a matrix, height then width. The OpenCV convention
    # is width then height


class _Files:
    def __init__(self, path):
        config.set_paths(path)
        self.current_slice = (
            -1
        )  # Starts on -1, since the first call to next gets the index-0 index
        self.slice_imgs = os.listdir(config.slice_path)
        self.tube_imgs = os.listdir(config.tube_path)
        self.slice_total = len(self.slice_imgs)
        assert self.slice_total == len(
            self.tube_imgs
        ), "There must be the same number of tube images as slice images"

    def __iter__(self):
        return self

    def __next__(self):
        """returns next (slice image, tube image) to be processed, each cropped"""
        if self.current_slice >= self.slice_total - 1:
            raise StopIteration
        res = (
            load_and_crop(config.slice_path, self.slice_imgs[self.current_slice]),
            load_and_crop(config.tube_path, self.tube_imgs[self.current_slice]),
        )
        self.current_slice += 1
        return res

    def __len__(self):
        return self.slice_total

    def save_img(self, img):
        cv2.imwrite(
            join(config.processed_path, "slice {}.png".format(self.current_slice)), img
        )

    def get_tube_sample(self):
        return load_and_crop(config.tube_path, self.tube_imgs[0])

    def get_image_sample(self):
        center_slice = int(
            self.slice_total / 2
        )  # The middle slices are more indicitave of the sample scan than the ends
        return (
            load_and_crop(config.slice_path, self.slice_imgs[center_slice]),
            load_and_crop(config.tube_path, self.tube_imgs[center_slice]),
        )

    def get_progress(self):
        return "{}/{} images processed".format(self.current_slice + 1, self.slice_total)
