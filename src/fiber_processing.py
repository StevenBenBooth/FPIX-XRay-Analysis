import cv2
import numpy as np


def remove_fiber(
    top_upper_bound, bottom_lower_bound, thickness, mask, close_ker, open_ker
):
    """
    Processes the image to ignore the carbon fiber in the image classification.

    :param int top_upper_bound: The pixel position of the middle of the upper layer of carbon fiber (numpy conventions)
    :param int bottom_lower_bound:
        The pixel position of the middle of the lower layer of carbon fiber (numpy conventions)
    :param int thickness: The thickness of the carbon fiber layer to be excluded from the mask
    :param arr mask: The mask to be processed
    :param arr close_ker: The kernel to close the fiber chunks together before finding bounds
    :param arr open_ker: The kernel to clean up little pieces of fiber left over
    :returns arr result: mask without carbon foam
    """

    assert isinstance(top_upper_bound, int), "top_upper_bound must be an integer"
    assert isinstance(bottom_lower_bound, int), "bottom_lower_bound must be an integer"
    assert isinstance(thickness, int), "thickness must be an integer"
    rough_mask = 255 * np.ones(mask.shape[:2], np.uint8)  # Not sure if 255 is necessary
    shape = np.shape(mask)
    rows, cols = shape
    cv2.rectangle(rough_mask, (0, top_upper_bound), (cols, bottom_lower_bound), 0, -1)
    fiber_parts = cv2.bitwise_and(mask, rough_mask)
    closed_fiber = cv2.morphologyEx(
        fiber_parts, cv2.MORPH_CLOSE, close_ker, iterations=4
    )  # Closes up the fiber parts so the removal works better
    top_coords, bottom_coords = _find_coords(
        top_upper_bound, bottom_lower_bound, closed_fiber, shape
    )

    for j in range(cols):
        if top_coords[j] != -1:
            t = top_coords[j]
            for i in range(t, thickness + t):
                mask[i][j] = 0
        if bottom_coords[j] != -1:
            b = bottom_coords[j]
            for i in range(b - thickness + 1, b + 1):
                mask[i][j] = 0

    result = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, open_ker, iterations=1
    )  # Clear little fiber artifacts
    return result


def _find_coords(top_bound, bot_bound, closed_img, img_dim):
    """Returns -1 for top and/or bottom if it doesn't find it in the bounds given"""
    rows, cols = img_dim
    top_coords = []
    bottom_coords = []
    for j in range(cols):
        top_found = False
        top = -1
        bottom = -1
        for i in range(rows):
            if closed_img[i][j] == 255:
                if not top_found and i < top_bound:
                    top_found = True
                    top = i
                elif i >= bot_bound:
                    bottom = i
        top_coords.append(top)
        bottom_coords.append(bottom)
    return top_coords, bottom_coords
