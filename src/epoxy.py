import cv2
import numpy as np

from fiber_processing import remove_fiber
from tube_interpolate import process_highlights
from tube_analysis import get_bound_circ

import config


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

    # Roughly identify the epoxy layer
    img_epoxy_raw = cv2.inRange(
        img_blur, config.epoxy_low_bound, config.highlight_low_bound
    )

    # This function returns information on the tube center
    outer_tube = get_bound_circ(img_tube, config.tube_radius)

    tube_mask = np.zeros(
        img_epoxy_raw.shape[:2], np.uint8
    )  # This mask is just the tube

    x, y, r = outer_tube
    cv2.circle(tube_mask, (x, y), r, 255, -1)
    # Masks the rough epoxy to exclude inside the tube
    not_tube_mask = 255 - tube_mask
    img_epoxy_ntube = cv2.bitwise_and(img_epoxy_raw, img_epoxy_raw, mask=not_tube_mask)

    # Removes the carbon fiber from the epoxy mask
    img_epoxy = remove_fiber(
        config.cf_bottom_bound,
        config.cf_top_bound,
        config.cf_thickness,
        img_epoxy_ntube,
        fiber_close_ker,
        open_ker,
    )

    # The highlights around the tube may be epoxy or may not. We need to interpolate whether they are or are not,
    # and to do so we need to extract the highlights
    img_highlights = cv2.bitwise_and(
        cv2.inRange(img_blur, config.highlight_low_bound, 255), not_tube_mask
    )

    img_interpolated = process_highlights(
        save_information,
        img_epoxy,
        img_highlights,
        outer_tube,
        config.num_wedges,
        config.highlight_thickness,
        config.interpolation_thresh,
        config.epoxy_interp_thresh,
        interpolate_close_ker,
    )
    return img_interpolated, outer_tube
