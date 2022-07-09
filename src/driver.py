import eel
import pandas as pd
from os.path import join

import files
import config
import statistics
import image_output
from process import find_epoxy


"""This module serves as a hub for communication between the python and javascript components,
as well as some of the disparate modules. It also calls the main processing loop."""

# initializing the application (points to the folder containing the web components)
eel.init("src/gui")


@eel.expose
def set_path(base_path):
    files.setup(base_path)
    # After the path is set, we need to set the default cropping bounds
    h, w = files.Files.get_img_size()
    config.image_size = (h, w)
    config.cropping_bounds = [0, w, 0, h]


@eel.expose
def update_bounds(bounds):
    config.cropping_bounds = bounds


@eel.expose
def update_radius(radius):
    config.tube_radius = radius


@eel.expose
def update_params(params):
    # TODO: find a way to make this more resistant to changes in the order of array elements
    config.update_params(*params)


@eel.expose
def update_cropping_sample():
    image_output.write_crop_sample()


@eel.expose
def update_tube_sample():
    image_output.write_tube_sample(config.tube_radius)


@eel.expose
def update_slice_sample():
    image_output.write_image_sample()


@eel.expose
def get_bounds():
    return config.cropping_bounds


@eel.expose
def get_radius():
    return config.tube_radius


@eel.expose
def get_parameters():
    return config.get_params()


@eel.expose
def log(val):
    print(val)


@eel.expose
def process():
    tracker = statistics.StatTracker.get_instance()
    folder = config.save_path
    for i, (foam_slice, tube_slice) in enumerate(files.Files):
        epox, circle = find_epoxy(foam_slice, tube_slice)
        files.Files.save_img(image_output.pretty_output(foam_slice, epox, circle))
        if (i + 1) % 5 == 0:
            eel.update(files.Files.get_progress())
    # update the number at the end, or else it's very frustrating
    eel.update(files.Files.get_progress())

    # I haven't been doing anything with the area stats. They give information
    # on the distribution along the tube. This could be useful later on if you
    # notice that the dispensor works better for earlier dispensing
    coverage_stats, _ = tracker.get_stats()
    df = pd.DataFrame(coverage_stats)
    df.to_excel(join(folder, "Coverage data.xlsx"))
    statistics.save_coverage_stats(
        df.to_numpy(), save_folder=folder, col_count=config.num_wedges
    )
    statistics.save_png_to_gif(config.processed_path, join(folder, "processed.gif"))
    # config.save_settings(join(folder, "settings.txt"))


# starting the application
eel.start("select_folder.html", mode="chrome")
