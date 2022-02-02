import numpy as np
import cv2
from enum import Enum


class Method(Enum):
    CONTOUR = 1
    HOUGH = 2


def get_bound_circ(tube_img, radius, method=Method.CONTOUR):
    """
    Takes in an image of the tube, returns the position and radius of the circle bounding the outer surface.

    :param tube_img: Image of the tube
    :param int radius:
        Means two different things depending on the method chosen. If method = Method.CONTOUR, then the radius is the
        chosen radius of the outer tube by the user. If method = Method.HOUGH, then the radius is the minimum allowed
        radius to be detected
    :param method:
        The method to find the outer circle. CONTOUR definitely works better, but maybe HOUGH will be useful in the
        future.
    :return:
    """
    assert isinstance(radius, int), "radius must be an integer"
    if method is Method.CONTOUR:
        return _get_bound_circ_cont(tube_img, radius)
    if method is Method.HOUGH:
        return _get_bound_circ_Hough(tube_img, radius)


def _get_bound_circ_cont(tube_img, radius):
    tube_gray = cv2.cvtColor(tube_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.inRange(tube_gray, 200, 255)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_area = -1
    big_contour = contours[0]
    for contour in contours:
        size = cv2.contourArea(contour)
        if size >= max_area:
            big_contour = contour
            max_area = size

    x, y, w, h = cv2.boundingRect(big_contour)
    return x + int(w / 2), y + int(h / 2), radius


def _get_bound_circ_Hough(tube_img, min_radius):
    tube_gray = cv2.cvtColor(tube_img, cv2.COLOR_BGR2GRAY)
    tube_opened = cv2.morphologyEx(tube_gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    tube_closed = cv2.morphologyEx(tube_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21)),
                                   iterations=4)
    # Find circles
    circles = cv2.HoughCircles(tube_closed, cv2.HOUGH_GRADIENT, 1.3, 1, minRadius=min_radius)

    if circles is None: raise ValueError("Didn't find any circles")
    # Get the (x, y, r) as integers
    circles = np.round(circles[0, :]).astype("int")

    max_radius = -1
    bounding_circle = (0, 0, 0)
    for circle in circles:
        r = circle[2]
        if r >= max_radius:
            bounding_circle = circle
            max_radius = r
    return bounding_circle
