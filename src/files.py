from tkinter import messagebox
from os.path import join
import os
import cv2

"""This module acts a singleton to manage the files"""


__base_path = None
__slice_path = None
__tube_path = None


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
        __slice_path = check_path(join(base_path, "pictures"))
        __tube_path = check_path(join(base_path, "tube"))
        load_images()
    except NotADirectoryError as e:
        raise e


def _load_and_crop(path, slice):
    return cv2.imread(join(path, slice))[100:350, 75:575]


def get_tube_sample():
    return _load_and_crop(__tube_path, __tube_imgs[0])


def get_next_imgs():
    """returns (tube image, slice image), each cropped"""
    return (
        _load_and_crop(__tube_path, __tube_imgs[__current_slice]),
        _load_and_crop(__slice_path, __slice_imgs[__current_slice]),
    )


def load_images():
    global __slice_imgs
    global __tube_imgs
    global __slice_total

    __slice_imgs = os.listdir(__slice_path)
    __tube_imgs = os.listdir(__tube_path)
    __slice_total = len(__slice_imgs)


def check_path(path):
    if not os.path.isdir(path):
        message = "{} does not define a valid folder path".format(path)
        messagebox.showerror("Not a path", message)
        raise NotADirectoryError(message)
    return path


def make_processed():
    try:
        os.mkdir(join(__base_path, "Processed"))
    except FileExistsError:
        pass
