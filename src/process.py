import cv2
import numpy as np

import config

from fiber_processing import remove_fiber
from tube_interpolate import process_highlights
from tube_analysis import get_bound_circ


def find_epoxy(img, img_tube, save_information=True):
    """Performs all the actions required to extract the epoxy from the image"""

    # NOTE: these kernels may need to be changed depending on image size. If so,
    # they could be set programmatically based on cropping dimensions.
    open_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fiber_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 5))
    interpolate_close_ker = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    blur_ker = (5, 5)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # opening then blur found to be better than blur then opening--makes sense since blur spreads out the foam features
    # First opening is used to remove some foam features
    img_open = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, open_ker, iterations=1)
    img_blur = cv2.GaussianBlur(img_open, blur_ker, 0)

    rough_mask = cv2.inRange(
        img_blur, config.epoxy_low_bound, config.highlight_low_bound
    )

    outer_tube = get_bound_circ(img_tube, config.tube_radius)
    x, y, r = outer_tube

    # Creates a map that computes the euclidean distance of a pixel position to the identified tube center (for points close to the tube)
    h, w = rough_mask.shape[:2]
    middle_h, middle_w = h // 2, w // 2
    top, bottom, left, right = middle_h - r, middle_h + r, middle_w - r, middle_w + r
    # It should not be the case that middle_h +- r is outside the image
    ys, xs = np.ogrid[top:bottom, left:right]

    # For points near the tube, we compute the actual distance. For far points, we spare some compute and just set them to have a high distance
    dist = np.full((h, w), 2 * r)
    dist[top:bottom, left:right] = np.sqrt((x - xs) ** 2 + (y - ys) ** 2)

    # Sets all points of the mask within the tube circle to 0, removing the tube from the mask
    no_tube = np.where(dist <= r, 0, rough_mask)

    no_fiber = remove_fiber(
        config.cf_bottom_bound,
        config.cf_top_bound,
        config.cf_thickness,
        no_tube,
        fiber_close_ker,
        open_ker,
    )

    # TODO: this is a bug source?
    hightlights_mask = cv2.bitwise_and(
        cv2.inRange(img_blur, config.highlight_low_bound, 255), no_fiber
    )

    epoxy_mask = process_highlights(
        save_information,
        no_fiber,
        hightlights_mask,
        outer_tube,
        config.num_wedges,
        config.highlight_thickness,
        config.interpolation_thresh,
        config.epoxy_interp_thresh,
        interpolate_close_ker,
    )

    cv2.imwrite("C:\\Users\\Work\\Desktop\\temp\\initial thresh.png", rough_mask)
    cv2.imwrite("C:\\Users\\Work\\Desktop\\temp\\no tube.png", no_tube)
    cv2.imwrite("C:\\Users\\Work\\Desktop\\temp\\no fiber.png", no_fiber)
    cv2.imwrite("C:\\Users\\Work\\Desktop\\temp\\final.png", epoxy_mask)

    return epoxy_mask, outer_tube
