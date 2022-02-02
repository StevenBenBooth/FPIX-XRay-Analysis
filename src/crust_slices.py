import cv2
import numpy as np
import math


def get_crust_masks(img_dim, tube_circle, number_slices, thickness):
    """
    Loops over the pixels in a box enclosing the tube, characterizing them according to their angle wrt the tube center.
    Combining the resulting radial slices with an annulus, returns a List of Pizza-crust shaped masks

    Parameters
    ----------
    :param img_dim: 2D array
        Dimensions of image to be processed.
    :param tube_circle: tuple (int, int, int)
        Tuple (x, y, r) containing information about tube outer diameter. (x, y) denotes tube's center in
        numpy coordinates (x and y switched for numpy and cv2), and r denotes the tube's radius.
    :param int number_slices:
        Must be a positive integer. Denotes the number of crusts to slice. ie, 1 would return a full annulus, 2 would
        return two half-annuli, etc.
    :param thickness: int
        Must be a positive integer. The thickness of the crusts to be returned.
    :return: List
    """
    assert number_slices > 0 and isinstance(number_slices, int), "number_slices must be a positive integer"
    assert thickness > 0 and isinstance(thickness, int), "thickness must be a positive integer"
    cent_y, cent_x, radius = tube_circle
    angle_swept = 2 * math.pi / number_slices

    # Bounds avoid looping over whole image
    x_min = max(0, cent_x - int(1.25 * radius) - thickness)
    x_max = min(img_dim[0], cent_x + int(1.25 * radius) + thickness)
    y_min = max(0, cent_y - int(1.25 * radius) - thickness)
    y_max = min(img_dim[1], cent_y + int(1.25 * radius) + thickness)

    annulus = annulus_mask(img_dim, (cent_y, cent_x), radius, thickness)  # Awkward indexing courtesy of
    # numpy/opencv indexing inconsistency

    slices = []
    for i in range(number_slices):
        slices.append(np.zeros(img_dim, np.uint8))

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            slices[int(get_angle(x, y, (cent_x, cent_y)) / angle_swept)][x][y] = 255

    crusts = []
    for slice in slices:
        crusts.append(cv2.bitwise_and(slice, annulus))
    return crusts


def get_angle(x, y, center):
    cent_x, cent_y = center
    # In cases where x-cent_x == 0, sets the angle to avoid the /0 error
    if x == cent_x:
        if y > cent_y:
            angle = math.pi / 2
        else:
            angle = 3 * math.pi / 2
    else:
        # Note that the origin is pointing down, because the "x-axis" is vertical in numpy matrix coords
        angle = math.atan((y - cent_y) / (x - cent_x))
        if x - cent_x < 0:
            angle += math.pi
        if angle < 0:
            angle += 2 * math.pi
    return angle


def annulus_mask(dim, center, inner_radius, thickness):
    outer = np.zeros(dim, np.uint8)
    inner = np.zeros(dim, np.uint8)

    cv2.circle(outer, center, inner_radius + thickness, 255, -1)
    cv2.circle(inner, center, inner_radius, 255, -1)
    return cv2.bitwise_xor(inner, outer)
