import cv2
import numpy as np

from fiber_processing import remove_fiber
from tube_interpolate import process_highlights
from tube_analysis import get_bound_circ


def find_epoxy(
    img,
    img_tube,
    tube_radius,
    slice_num,
    num_wedges,
    highlight_cutoff=210,
    epox_low_bound=40,
    cf_top_bound=70,  # top_bound < bottom_bound because indexing starts from the top
    # These bounds should be set to the y-position of somewhere in the carbon foam layers
    cf_bottom_bound=173,
    cf_thickness=7,
    highlight_thickness=9,
    interpolation_thresh=0.7,
    epoxy_interp_thresh=0,
):
    """Performs all the actions required to extract the epoxy from the image"""

    # These kernels don't need to be touched (most likely)
    open_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fiber_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    interpolate_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    blur_ker = (5, 5)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # opening then blur found to be better than blur then opening--makes sense since blur spreads out the foam features
    # First opening is used to remove some foam features
    img_open = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, open_ker, iterations=1)
    img_blur = cv2.GaussianBlur(img_open, blur_ker, 0)

    # Roughly identify the epoxy layer
    img_epoxy_raw = cv2.inRange(img_blur, epox_low_bound, highlight_cutoff)

    # This function returns information on the tube center
    outer_tube = get_bound_circ(img_tube, tube_radius)

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
        cf_top_bound,
        cf_bottom_bound,
        cf_thickness,
        img_epoxy_ntube,
        fiber_close_ker,
        open_ker,
    )

    # The highlights around the tube may be epoxy or may not. We need to interpolate whether they are or are not,
    # and to do so we need to extract the highlights
    img_highlights = cv2.bitwise_and(
        cv2.inRange(img_blur, highlight_cutoff, 255), not_tube_mask
    )

    img_interpolated = process_highlights(
        img_epoxy,
        img_highlights,
        outer_tube,
        slice_num,
        num_wedges,
        highlight_thickness,
        interpolation_thresh,
        epoxy_interp_thresh,
        interpolate_close_ker,
    )
    return img_interpolated, outer_tube
