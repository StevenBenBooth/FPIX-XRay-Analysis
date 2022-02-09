import eel
import paths
from os.path import join

# initializing the application (points to the folder)
eel.init("src/gui")


@eel.expose
def path_input(base_path):
    path = "{}".format(base_path)
    try:
        paths.set_paths(path)
        paths.make_processed()
        eel.loadNextPage()
    except NotADirectoryError:
        pass


# starting the application
eel.start("select_folder.html")
