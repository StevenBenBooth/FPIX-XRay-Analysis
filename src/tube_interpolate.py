import cv2
from crust_slices import get_crust_masks
from stat_tracker import StatTracker


def process_highlights(
    save_information,
    start_epoxy_mask,
    highlights,
    tube_circle,
    precision,
    thickness,
    thresh,
    epox_thresh,
    ker,
):
    """
    Classifies the highlights around the tube as either epoxy or not. To do so, it looks in a small pizza-crust slice
    outwards from the highlight, and checks how much is epoxy and highlight vs nothingness. Currently, epox_thresh is
    set to 0, so it's really only checking that there isn't too much void in the crust slice.

    :param bool save_information: whether the stat tracker should record information for this slice
    :param img start_epoxy_mask: Input of epoxy mask.
    :param img highlights: Mask of the image highlights, to be classified.
    :param tuple tube_circle: Contains information about the bounding circle for the tube.
    :param int precision: How many pizza crust slices to use.
    :param int thickness:
        How thick the crusts should be for the interpolation. If this is too high, you may need to lower thresholds.
        Too low and you might have holes in the final image for sections with thick highlights.
    :param float thresh:
        Overall threshold for how much of the stuff in the crust slice must be either epoxy or highlights to classify
        the slice as epoxy. Too high, and you may miss on actual epoxy. Too low and you might get false positives.
    :param float epox_thresh:
        Threshold for how much epoxy must be in crust slice to characterize highlight as epoxy.
        Often 0 works fine, as the reflections seem to be more extreme around the tube when there's epoxy.
    :param ker: Kernel for closing small holes at end of analysis.
    :return:
    """
    assert isinstance(precision, int), "precision must be int"
    assert isinstance(thickness, int), "thickness must be int"
    assert 0 <= thresh <= 1, "thresh must be between 0 and 1"
    assert 0 <= epox_thresh <= 1, "epox_thresh must be between 0 and 1"

    result = start_epoxy_mask.copy()
    masks = get_crust_masks(start_epoxy_mask.shape, tube_circle, precision, thickness)

    for i in range(len(masks)):
        crust = masks[i]
        tot = cv2.countNonZero(crust)
        epoxy_crust = cv2.bitwise_and(start_epoxy_mask, crust)
        highlight_crust = cv2.bitwise_and(highlights, crust)
        prop_epoxy_crust = cv2.countNonZero(epoxy_crust) / tot
        prop_highlight_crust = cv2.countNonZero(highlight_crust) / tot
        is_epoxy = (
            prop_epoxy_crust + prop_highlight_crust >= thresh
            and prop_epoxy_crust >= epox_thresh
        )
        if is_epoxy:
            result = cv2.bitwise_or(
                result, cv2.bitwise_or(epoxy_crust, highlight_crust)
            )
        if save_information:
            StatTracker.get_instance().update_coverage(i, is_epoxy)
    result = cv2.morphologyEx(
        result, cv2.MORPH_CLOSE, ker
    )  # Closure to remove little holes
    return result
