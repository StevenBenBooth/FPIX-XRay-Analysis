from tkinter import messagebox
from os.path import join
import os

base_path = None
slice_path = None
tube_path = None


def set_paths(base_path):
    try:
        base_path = check_path(base_path)
        slice_path = check_path(join(base_path, " pictures"))
        tube_path = check_path(join(base_path, " tube"))
    except NotADirectoryError as e:
        raise e


def make_processed():
    try:
        os.mkdir(join(base_path, " processed"))
    except FileExistsError:
        pass


def check_path(path):
    if not os.path.isdir(path):
        message = "{} does not define a valid folder path".format(path)
        messagebox.showerror("Not a path", message)
        raise NotADirectoryError(message)
    return path
