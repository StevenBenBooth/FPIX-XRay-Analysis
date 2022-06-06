import eel
from files import setup
import config
from image_output import write_tube_sample, write_image_sample
from process import process
import sys
import os


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# initializing the application (points to the folder containing the web components)
eel.init("src/gui")


@eel.expose
def set_path(base_path):
    setup(base_path)
    eel.loadNextPage()


@eel.expose
def update_radius(radius):
    config.tube_radius = radius


@eel.expose
def update_tube_sample():
    write_tube_sample(config.tube_radius)


@eel.expose
def update_params(params):
    # TODO: refactor this so that it passes a dictionary instead an array,
    # if it is possible to get eel to pass it well and to implement this efficiently
    config.update_params(*params)


@eel.expose
def get_radius():
    return config.tube_radius


@eel.expose
def get_parameters():
    return config.get_params()


@eel.expose
def update_slice_sample():
    write_image_sample()


@eel.expose
def start_processing():
    process()


@eel.expose
def log(val):
    print(val)


# starting the application
eel.start(
    "select_folder.html", mode="chrome"
)  # chrome looks nicer, but edge would work on machines without chrome installed
