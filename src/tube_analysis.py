import numpy as np
import cv2
from enum import Enum


class CircleMethod(Enum):
    CONTOUR = 1
    HOUGH = 2


def get_bound_circ(tube_img, radius, method=CircleMethod.CONTOUR):
    """
    Takes in an image of the tube, returns the position and radius of the circle bounding the outer surface.

    :param tube_img: Image of the tube
    :param int radius:
        Means two different things depending on the method chosen. If method = Method.CONTOUR, then radius will be the
        radius of the output circle. If method = Method.HOUGH, then radius gives a minimum size for identifying the circle
    :param method:
        The method to find the outer circle. I've found CONTOUR to work better, so it is the default.
    :return:
    """
    assert isinstance(radius, int), "radius must be an integer"
    if method is CircleMethod.CONTOUR:
        return _get_bound_circ_cont(tube_img, radius)
    if method is CircleMethod.HOUGH:
        return _get_bound_circ_Hough(tube_img, radius)


def _get_bound_circ_cont(tube_img, radius):
    tube_gray = cv2.cvtColor(tube_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.inRange(tube_gray, 200, 255)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Return largest contour
    big_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    x, y, w, h = cv2.boundingRect(big_contour)
    return x + w // 2, y + h // 2, radius


def _get_bound_circ_Hough(tube_img, min_radius):
    tube_gray = cv2.cvtColor(tube_img, cv2.COLOR_BGR2GRAY)
    tube_opened = cv2.morphologyEx(
        tube_gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    )
    tube_closed = cv2.morphologyEx(
        tube_opened,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)),
        iterations=4,
    )
    # Find circles
    circles = cv2.HoughCircles(
        tube_closed, cv2.HOUGH_GRADIENT, 1.3, 1, minRadius=min_radius
    )

    if circles is None:
        raise ValueError("Didn't find any circles")
    # Get the (x, y, r) as integers
    circles = np.round(circles[0, :]).astype("int")

    # Return largest circle (by radius)
    return sorted(circles, lambda x: x[2], reverse=True)[0]
