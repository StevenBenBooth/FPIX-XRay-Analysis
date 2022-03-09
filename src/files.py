from tkinter import messagebox
from os.path import join
import os
import cv2

"""This module acts a singleton to manage and load images"""


__base_path = None
__slice_path = None
__tube_path = None
__save_path = None


__slice_imgs = None
__tube_imgs = None

__slice_total = None
__current_slice = None


def set_paths(base_path):
    try:
        global __base_path
        global __slice_path
        global __tube_path
        global __current_slice

        __current_slice = 0

        __base_path = check_path(base_path)
        __slice_path = check_path(join(base_path, "Pictures"))
        __tube_path = check_path(join(base_path, "Tube"))
        load_images()
    except NotADirectoryError as e:
        raise e


def save_file(processed):
    cv2.imwrite(join(__save_path, "slice {}".format(__current_slice)))


def _load_and_crop(path, slice):
    return cv2.imread(join(path, slice))[
        100:350, 75:575
    ]  # When treating image as a matrix, height then width. The OpenCV convention
    # is width then height


def get_tube_sample():
    return _load_and_crop(__tube_path, __tube_imgs[0])


def get_image_sample():
    center_slice = int(__slice_total / 2)
    return (
        _load_and_crop(__slice_path, __slice_imgs[center_slice]),
        _load_and_crop(__tube_path, __tube_imgs[center_slice]),
    )


def get_next():
    """returns (slice image, tube image), each cropped"""
    global __current_slice
    res = (
        _load_and_crop(__slice_path, __slice_imgs[__current_slice]),
        _load_and_crop(__tube_path, __tube_imgs[__current_slice]),
    )
    __current_slice += 1
    return res


def load_images():
    global __slice_imgs
    global __tube_imgs
    global __slice_total

    __slice_imgs = os.listdir(__slice_path)
    __tube_imgs = os.listdir(__tube_path)
    __slice_total = len(__slice_imgs)


def get_total():
    return __slice_total


def check_path(path):
    if not os.path.isdir(path):
        message = "{} does not define a valid folder path".format(path)
        messagebox.showerror("Not a path", message)
        raise NotADirectoryError(message)
    return path


def make_processed():
    global __save_path
    __save_path = join(__base_path, "Processed")
    try:
        os.mkdir(__save_path)
    except FileExistsError:
        pass
