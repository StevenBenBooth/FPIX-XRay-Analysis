import eel
import files
from image_output import write_tube_img, write_image_sample

# initializing the application (points to the folder containing the web components)
eel.init("src/gui")

__tube_radius = None


@eel.expose
def path_input(base_path):
    path = "{}".format(base_path)
    try:
        files.set_paths(path)
        files.make_processed()
        write_tube_img()
        eel.loadNextPage()
    except NotADirectoryError:
        pass


@eel.expose
def update_tube_sample(radius):
    global __tube_radius
    __tube_radius = int(radius)
    write_tube_img(__tube_radius)


@eel.expose
def update_slice_sample(params):
    print(params)
    write_image_sample(*tuple(params))


@eel.expose
def log(val):
    print(val)


# starting the application
eel.start("select_folder.html")
