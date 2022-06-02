import eel
import pandas as pd

import config
from os.path import join
import files
from epoxy import find_epoxy
from image_output import person_output
from stat_tracker import StatTracker
import tracker_analysis


@eel.expose
def process():
    tracker = StatTracker.get_instance()
    folder = config.save_path
    for i, (foam_slice, tube_slice) in enumerate(files.slices):
        epox, circle = find_epoxy(foam_slice, tube_slice)
        files.slices.save_img(person_output(foam_slice, epox, circle))
        if (i + 1) % 5 == 0:
            eel.update(files.slices.get_progress())
    eel.update(files.slices.get_progress())
    # I haven't been doing anything with the area stats. They give information
    # on the distribution along the tube. This could be useful later on if you
    # notice that the dispensor works better for earlier dispensing
    coverage_stats, _ = tracker.get_stats()
    df = pd.DataFrame(coverage_stats)
    df.to_excel(join(folder, "Coverage data.xlsx"))
    tracker_analysis.save_coverage_stats(
        df.to_numpy(), save_folder=folder, col_count=config.num_wedges
    )
    tracker_analysis.save_png_to_gif(
        config.processed_path, join(folder, "processed.gif")
    )
    # config.save_settings(join(folder, "settings.txt"))
