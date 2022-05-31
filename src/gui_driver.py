import eel
import files
import config
from image_output import write_tube_sample, write_image_sample

# initializing the application (points to the folder containing the web components)
eel.init("src/gui")


@eel.expose
def path_input(base_path):
    path = "{}".format(base_path)
    try:
        files.set_paths(path)
        files.make_processed()
        eel.loadNextPage()
    except NotADirectoryError:
        pass


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
    config.update_values(*tuple(params))


@eel.expose
def get_radius():
    return config.tube_radius


@eel.expose
def update_slice_sample():
    write_image_sample()


@eel.expose
def get_parameters():
    return config.get_params


@eel.expose
def log(val):
    print(val)


# starting the application
eel.start(
    "select_folder.html", mode="chrome"
)  # chrome looks nicer, but edge would work on machines without chrome installed
