import cv2
import numpy as np


def remove_fiber(top_bound, bottom_bound, thickness, mask, close_ker, open_ker):
    """
    Processes the mask to ignore the carbon fiber.

    :param int top_bound: A pixel position below all of the upper layer of carbon fiber (numpy conventions)
    :param int bottom_bound: A pixel position above all of the lower layer of carbon fiber (numpy conventions)

    :param int thickness: The thickness of the carbon fiber layer to be excluded from the mask
    :param arr mask: The mask to be processed
    :param arr close_ker: The kernel to close the fiber chunks together before finding bounds
    :param arr open_ker: The kernel to clean up little pieces of fiber left over after the main removal
    :returns arr result: mask without carbon foam
    """

    assert isinstance(top_bound, int), "top_upper_bound must be an integer"
    assert isinstance(bottom_bound, int), "bottom_lower_bound must be an integer"
    assert isinstance(thickness, int), "thickness must be an integer"

    # rough_mask = np.ones(mask.shape, np.uint8)
    rows, cols = mask.shape

    # # cv2.rectangle(rough_mask, (0, top_bound), (cols, bottom_bound), 0, -1)
    # ys, _ = np.ogrid[0:rows, 0:0]
    # print(ys)
    # fiber_parts = np.where((ys < top_bound) or (ys > bottom_bound), mask, 0)

    # fiber_parts = cv2.bitwise_and(mask, rough_mask)

    # Closing the image a bit makes it easier to find fiber consistently
    closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_ker, iterations=4)
    top_coords, bottom_coords = _find_coords(top_bound, bottom_bound, closed)

    # Creates an array whose values index row position
    row_vals = np.arange(rows).reshape(rows, 1)
    # TODO: Is it better to use ogrid here?

    # Gets the distance of each array position to the fiber top
    fiber_distance_top = np.subtract(row_vals, top_coords)
    # Same for the bottom (flipped sign because we want to remove pixels above bottom_bound (i.e., lower index))
    fiber_distance_bottom = np.subtract(bottom_coords, row_vals)

    def create_conditions(surface_distance_array):
        return [
            surface_distance_array <= thickness,
            surface_distance_array > 0,
            (top_coords != -1).reshape(1, cols),
        ]

    top_conditions = create_conditions(fiber_distance_top)

    bottom_conditions = create_conditions(fiber_distance_bottom)

    def mask_lfold(conditions, fun):
        assert len(conditions) > 0, "Must have at least one condition"
        # Left folds masks together using fun
        (
            mask,
            *c,
        ) = conditions
        for condition in c:
            mask = fun(mask, condition)
        return mask

    top = mask_lfold(top_conditions, np.logical_and)
    bot = mask_lfold(bottom_conditions, np.logical_or)
    combined = mask_lfold([top, bot], np.logical_or)

    mask = np.subtract(mask, combined)

    # Clear little fiber artifacts
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_ker, iterations=1)


def _find_coords(top_bound, bot_bound, img):
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
        # We then subtract this from the axis length to obtain the actual column position
        val = axis_length - np.flip(mask, axis=axis).argmax(axis=axis) - 1

        return np.where(mask.any(axis=axis), val, invalid_value).reshape((1, -1))

    top_coords = first_nonzero(img[:top_bound, :])
    bottom_coords = last_nonzero(img[bot_bound:, :], img.shape[0])

    return top_coords, bottom_coords
