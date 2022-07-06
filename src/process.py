import eel
import cv2
import numpy as np
import pandas as pd
from os.path import join

import files
import config
from image_output import person_output
from statistics import StatTracker
from fiber_processing import remove_fiber
from tube_interpolate import process_highlights
from tube_analysis import get_bound_circ

import statistics


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
    statistics.save_coverage_stats(
        df.to_numpy(), save_folder=folder, col_count=config.num_wedges
    )
    statistics.save_png_to_gif(config.processed_path, join(folder, "processed.gif"))
    # config.save_settings(join(folder, "settings.txt"))


def find_epoxy(img, img_tube, save_information=True):
    """Performs all the actions required to extract the epoxy from the image"""

    # These kernels don't need to be touched (most likely)
    open_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fiber_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 5))
    interpolate_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    blur_ker = (5, 5)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # opening then blur found to be better than blur then opening--makes sense since blur spreads out the foam features
    # First opening is used to remove some foam features
    img_open = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, open_ker, iterations=1)
    img_blur = cv2.GaussianBlur(img_open, blur_ker, 0)

    epoxy_mask = cv2.inRange(
        img_blur, config.epoxy_low_bound, config.highlight_low_bound
    )

    outer_tube = get_bound_circ(img_tube, config.tube_radius)
    x, y, r = outer_tube

    # Creates a map that computes the euclidean distance of a pixel position to the identified tube center
    h, w = epoxy_mask.shape[:2]
    ys, xs = np.ogrid[0:h, 0:w]
    dist = np.sqrt((x - xs) ** 2 + (y - ys) ** 2)

    # Sets all points of the mask within the tube circle to 0, removing the tube from the mask
    epoxy_mask = np.where(dist <= r, 0, epoxy_mask)

    epoxy_mask = remove_fiber(
        config.cf_bottom_bound,
        config.cf_top_bound,
        config.cf_thickness,
        epoxy_mask,
        fiber_close_ker,
        open_ker,
    )

    hightlights_mask = cv2.bitwise_and(
        cv2.inRange(img_blur, config.highlight_low_bound, 255), epoxy_mask
    )

    epoxy_mask = process_highlights(
        save_information,
        epoxy_mask,
        hightlights_mask,
        outer_tube,
        config.num_wedges,
        config.highlight_thickness,
        config.interpolation_thresh,
        config.epoxy_interp_thresh,
        interpolate_close_ker,
    )
    return epoxy_mask, outer_tube
