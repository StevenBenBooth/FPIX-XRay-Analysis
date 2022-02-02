import cv2
import numpy as np

from src.fiber_processing import remove_fiber
from tube_interpolate import process_highlights
from src.tube_analysis import get_bound_circ


def find_epoxy(img, img_tube, tube_radius, slice_num, num_wedges):
    """Performs all the actions required to extract the epoxy from the image"""

    # These kernels you probably don't need to touch
    open_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fiber_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    interpolate_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    blur_ker = (5, 5)

    epox_hlght_cutoff = 210

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # opening then blur found to be better than blur then opening--makes sense since blur spreads out the foam features
    # First opening is used to remove some foam features
    img_open = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, open_ker, iterations=1)
    img_blur = cv2.GaussianBlur(img_open, blur_ker, 0)

    # Roughly identify the epoxy layer. 40, 220 is a good base
    img_epoxy_raw = cv2.inRange(img_blur, 30, epox_hlght_cutoff)

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

    # If you have some issue where carbon fiber is still interpreted as epoxy, you need to adjust these two numbers.
    # Just open up a pic of the cropped tube in paint, and set the bounds to be the y-axis pixel pos for somewhere in
    # the two fiber regions. Because indexing starts from the top, the top_bound is a lower number than the bottom_bound
    top_bound = 70
    bottom_bound = 173
    cf_thickness = 7  # This is the thickness of the carbon foam layers in pixels. It might vary a bit, but 6-8 works

    # Removes the carbon fiber from the epoxy mask
    img_epoxy = remove_fiber(
        top_bound,
        bottom_bound,
        cf_thickness,
        img_epoxy_ntube,
        fiber_close_ker,
        open_ker,
    )

    # The highlights around the tube may be epoxy or may not. We need to interpolate whether they are or are not,
    # and to do so we need to extract the highlights
    img_highlights = cv2.bitwise_and(
        cv2.inRange(img_blur, epox_hlght_cutoff, 255), not_tube_mask
    )

    # The parameters on this one are pretty tricky. I think (9, 0.7, 0, interpolate_close_ker) is a good starting place
    img_interpolated = process_highlights(
        img_epoxy,
        img_highlights,
        outer_tube,
        slice_num,
        num_wedges,
        9,
        0.6,
        0,
        interpolate_close_ker,
    )
    return img_interpolated, outer_tube
