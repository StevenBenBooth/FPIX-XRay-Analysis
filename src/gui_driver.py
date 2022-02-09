import eel
import files
from os.path import join
from image_output import write_tube_img

# initializing the application (points to the folder)
eel.init("src/gui")


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


# starting the application
eel.start("select_folder.html")
