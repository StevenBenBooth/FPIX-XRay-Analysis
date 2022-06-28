from venv import create
import cv2
import numpy as np
import functools


def remove_fiber(top_bound, bottom_bound, thickness, mask, close_ker, open_ker):
    """
    Processes the image to ignore the carbon fiber in the image classification.

    :param int top_bound: A pixel position below all of the upper layer of carbon fiber (numpy conventions)
    :param int bottom_bound: A pixel position above all of the lower layer of carbon fiber (numpy conventions)

    :param int thickness: The thickness of the carbon fiber layer to be excluded from the mask
    :param arr mask: The mask to be processed
    :param arr close_ker: The kernel to close the fiber chunks together before finding bounds
    :param arr open_ker: The kernel to clean up little pieces of fiber left over
    :returns arr result: mask without carbon foam
    """

    assert isinstance(top_bound, int), "top_upper_bound must be an integer"
    assert isinstance(bottom_bound, int), "bottom_lower_bound must be an integer"
    assert isinstance(thickness, int), "thickness must be an integer"
    rough_mask = np.ones(mask.shape[:2], np.uint8)
    rows, cols = mask.shape

    cv2.rectangle(rough_mask, (0, top_bound), (cols, bottom_bound), 0, -1)
    fiber_parts = cv2.bitwise_and(mask, rough_mask)
    closed_fiber = cv2.morphologyEx(
        fiber_parts, cv2.MORPH_CLOSE, close_ker, iterations=4
    )  # Closes up the fiber parts so the removal works better
    top_coords, bottom_coords = _find_coords(top_bound, bottom_bound, closed_fiber)

    # Creates an array whose values index row position
    row_vals = np.arange(rows).reshape(rows, 1)

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

    # def promote_dim(conditions):  # There may be a simpler implementation for this
    #     for i in range(len(conditions)):
    #         conditions[i] = conditions[i][:, np.newaxis]
    #     return conditions

    # def composite_mask(conditions, type="and"):
    #     if type == "and":
    #         fun = np.all
    #     elif type == "or":
    #         fun = np.any
    #     else:
    #         raise ValueError("Type must be 'any' or 'or'")
    #     return np.where(
    #         fun(np.stack(promote_dim(conditions), axis=-1), axis=-1), 1, 0
    #     )  # only selects values that satisfy all the conditions at once

    def composite_mask(conditions, type="and"):
        assert len(conditions) > 0, "Must have at least one condition"
        if type == "and":
            fun = np.logical_and
        elif type == "or":
            fun = np.logical_or

        # Folds masks together
        (
            mask,
            *c,
        ) = conditions
        for condition in c:
            mask = fun(mask, condition)
        return mask

    top = composite_mask(top_conditions)
    bot = composite_mask(bottom_conditions)
    combined = composite_mask([top, bot], type="or")

    mask = np.subtract(mask, combined)

    # Clear little fiber artifacts
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_ker, iterations=1)


def _find_coords(top_bound, bot_bound, img):
    """Returns -1 for top and/or bottom if it doesn't find it in the bounds given"""
    # This is gratefully stolen from the following stackoverflow post:
    # https://stackoverflow.com/questions/47269390/how-to-find-first-non-zero-value-in-every-column-of-a-numpy-array
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
