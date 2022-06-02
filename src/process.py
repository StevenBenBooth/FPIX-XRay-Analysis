import eel
import pandas as pd

import config
from os.path import join
from files import slices
from epoxy import find_epoxy
from image_output import person_output
from stat_tracker import StatTracker
import tracker_analysis


@eel.expose
def process():
    tracker = StatTracker.get_instance()
    folder = config.save_path

    for foam_slice, tube_slice in slices:
        epox, circle = find_epoxy(foam_slice, tube_slice)
        slices.save_img(person_output(foam_slice, epox, circle))

    df = pd.DataFrame(tracker.get_stats())
    df.to_excel(join(folder, "Coverage data.xlsx"))
    tracker_analysis.save_coverage_stats(
        df.to_numpy(), save_folder=folder, col_count=config.num_wedges
    )
    tracker_analysis.save_png_to_gif(
        config.processed_path, join(folder, "processed.gif")
    )
