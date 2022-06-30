import cv2
import numpy as np


def remove_fiber(top_bound, bottom_bound, thickness, mask, close_ker, open_ker):
    """
    Processes the image to ignore the carbon fiber in the image classification.

    :param int top_bound: The pixel position of the middle of the upper layer of carbon fiber (numpy conventions)
    :param int bottom_bound:
    The pixel position of the middle of the lower layer of carbon fiber (numpy conventions)

    :param int thickness: The thickness of the carbon fiber layer to be excluded from the mask
    :param arr mask: The mask to be processed
    :param arr close_ker: The kernel to close the fiber chunks together before finding bounds
    :param arr open_ker: The kernel to clean up little pieces of fiber left over
    :returns arr result: mask without carbon foam
    """

    assert isinstance(top_bound, int), "top_upper_bound must be an integer"
    assert isinstance(bottom_bound, int), "bottom_lower_bound must be an integer"
    assert isinstance(thickness, int), "thickness must be an integer"
    rough_mask = 255 * np.ones(mask.shape[:2], np.uint8)  # Not sure if 255 is necessary
    shape = np.shape(mask)
    _, cols = shape
    cv2.rectangle(rough_mask, (0, top_bound), (cols, bottom_bound), 0, -1)
    fiber_parts = cv2.bitwise_and(mask, rough_mask)
    closed_fiber = cv2.morphologyEx(
        fiber_parts, cv2.MORPH_CLOSE, close_ker, iterations=4
    )  # Closes up the fiber parts so the removal works better
    top_coords, bottom_coords = _find_coords(
        top_bound, bottom_bound, closed_fiber, shape
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
    # This is gratefully stolen from user Divakar's StackOverflow answer:
    # https://stackoverflow.com/a/47269413/19333140
    def first_nonzero(arr, axis=0, invalid_value=-1):
        # Create a mask with True for nonzero elements, False for zero elements
        mask = arr != 0
        # If there are any True values along the column, put the index of its first occurence
        # in the array. Otherwise, put invalid_value into the output array
        return np.where(mask.any(axis=axis), arr.argmax(axis=axis), invalid_value)

    def last_nonzero(arr, axis_length, axis=0, invalid_value=-1):
        mask = arr != 0

        # To take advantage of the argmax behavior, we need to flip the array;
        # this way, the first argmax coord will correspond to the last nonzero element in that column
        # We need to compensate for the effect of this flip
        val = axis_length - np.flip(mask, axis=axis).argmax(axis=axis) - 1

        return np.where(mask.any(axis=axis), val, invalid_value)

    top_coords = first_nonzero(img[:top_bound, :]).reshape((1, -1))
    bottom_coords = last_nonzero(img[bot_bound:, :], img.shape[0]).reshape((1, -1))

    return top_coords, bottom_coords
