import eel
import paths
import os
from os.path import join

# initializing the application (points to the folder)
eel.init("src/gui")

# window.open('http://www.website.com/page') js for opening page


@eel.expose
def path_input(base_path):
    try:
        paths.set_paths(base_path)
        paths.make_processed()

    except NotADirectoryError:
        pass


# starting the application
eel.start("select_folder.html")
