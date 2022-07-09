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

    rows, cols = mask.shape

    # Closing the image a bit makes it easier to find fiber consistently
    closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_ker, iterations=4)
    top_coords, bottom_coords = _find_coords(top_bound, bottom_bound, closed)

    # Creates an array whose values index row position. Type must match mask
    row_vals = np.arange(rows, dtype=np.uint8).reshape(rows, 1)

    # Get distance of each pixel from the top edge of the top CF
    fiber_distance_to_top = np.subtract(row_vals, top_coords)
    # Same for the bottom (flipped sign because we want to remove pixels above bottom_bound (i.e., lower index))
    fiber_distance_to_bottom = np.subtract(bottom_coords, row_vals)

    def create_conditions(surface_distance_array, coords):
        """Defines our conditions for which pixels are identified as caron fiber"""
        return [
            surface_distance_array <= thickness,
            surface_distance_array > 0,
            (coords != -1).reshape(1, cols),
        ]

    top_conditions = create_conditions(fiber_distance_to_top, top_coords)

    bottom_conditions = create_conditions(fiber_distance_to_bottom, bottom_coords)

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

    top_mask = mask_lfold(top_conditions, np.logical_and)
    bottom_mask = mask_lfold(bottom_conditions, np.logical_and)
    fiber_mask = mask_lfold([top_mask, bottom_mask], np.logical_or)

    # Mask is a grayscale image, so we convert the boolean 'combined' array
    mask = np.subtract(mask, 255 * fiber_mask.astype("uint8"))

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

        return np.where(mask.any(axis=axis), val, invalid_value)

    top_coords = first_nonzero(img[:top_bound, :]).reshape((1, -1))
    bottom_coords = last_nonzero(img[bot_bound:, :], img.shape[0]).reshape((1, -1))

    return top_coords, bottom_coords
