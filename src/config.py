"""This module stores the global settings inputted from the gui, to be used for processing"""
import sys


class _Config:
    _tube_radius = 33

    @property
    def tube_radius():
        return _tube_radius

    @tube_radius.setter
    def tube_radius(value):
        global _tube_radius
        assert (
            isinstance(value, int) and value > 0
        ), "Tube radius must be a positive integer"
        _tube_radius = value

    _num_wedges = 50

    @property
    def num_wedges():
        return _num_wedges

    @num_wedges.setter
    def num_wedges(value):
        global _num_wedges
        assert (
            isinstance(value, int) and value > 0
        ), "The number of interpolation slices must be a positive integer"
        _num_wedges = value

    _epoxy_low_bound = 40
    # highlight low bound is both the lower intensity bound for pixels to be interpreted as a highlight and the upper bound for them to be interpreted as epoxy
    _highlight_low_bound = 210

    @property
    def epoxy_low_bound():
        return _epoxy_low_bound

    @epoxy_low_bound.setter
    def epoxy_low_bound(value):
        global _epoxy_low_bound
        assert (
            isinstance(value, int) and value >= 0 and value <= 255
        ), "The low cutoff for epoxy must be an integer in 0, ..., 255"
        assert (
            value < _highlight_low_bound
        ), "The low cutoff for epoxy must be below the low cutoff for highlights"
        _epoxy_low_bound = value

    @property
    def highlight_low_bound():
        return _highlight_low_bound

    @highlight_low_bound.setter
    def highlight_low_bound(value):
        global _highlight_low_bound
        assert (
            isinstance(value, int) and value >= 0 and value <= 255
        ), "The cutoff intensity for highlights must be an integer in 0, ..., 255"
        assert (
            value > _highlight_low_bound
        ), "The low cutoff for epoxy must be below the low cutoff for highlights"

        _highlight_low_bound = value

    _cf_top_bound = 70  # top_bound < bottom_bound because indexing starts from the top
    # These bounds should be set to the y-position of somewhere in the carbon foam layers
    _cf_bottom_bound = 173

    @property
    def cf_top_bound():
        return _cf_top_bound

    @cf_top_bound.setter
    def cf_top_bound(value):
        global _cf_top_bound
        assert (
            isinstance(value, int) and value >= 0
        ), "The carbon foam top bound must be a nonnegative integer"
        assert (
            value < _cf_bottom_bound
        ), "Counterintuitively, the cf top bound should should be lower than the cf bottom bound (numpy indexing)"
        _cf_top_bound = value

    @property
    def cf_bottom_bound():
        return _cf_bottom_bound

    @cf_bottom_bound.setter
    def cf_top_bound(value):
        global _cf_bottom_bound
        assert (
            isinstance(value, int) and value >= 0
        ), "The carbon foam top bound must be a nonnegative integer"
        assert (
            value > _cf_top_bound
        ), "Counterintuitively, the cf bottom bound should should be higher than the cf top bound (numpy indexing is the opposite of how the picture looks)"
        _cf_bottom_bound = value

    _cf_thickness = 7

    @property
    def cf_thickness():
        return _cf_thickness

    @cf_thickness.setter
    def cf_thickness(value):
        global _cf_thickness
        assert (
            isinstance(value, int) and value >= 0
        ), "carbon foam thickness should be a nonnegative integer"
        _cf_thickness = value

    _highlight_thickness = 9

    @property
    def highlight_thickness():
        return _highlight_thickness

    @highlight_thickness.setter
    def highlight_thickness(value):
        global _highlight_thickness
        assert (
            isinstance(value, int) and value >= 0
        ), "highlight thickness should be a nonnegative integer"
        _highlight_thickness = value

    _interpolation_thresh = 0.7

    @property
    def interpolation_thresh():
        return _interpolation_thresh

    @interpolation_thresh.setter
    def interpolation_thresh(value):
        global _interpolation_thresh
        assert (
            value >= 0 and value <= 1
        ), "The interpolation threshold is a proportion, so must be in the interval [0, 1]"
        _interpolation_thresh = value

    _epoxy_interp_thresh = 0

    @property
    def epoxy_interp_thresh():
        return _epoxy_interp_thresh

    @epoxy_interp_thresh.setter
    def epoxy_interp_thresh(value):
        global _epoxy_interp_thresh
        assert (
            value >= 0 and value <= 1
        ), "The epoxy interpolation threshold is a proportion, so must be in the interval [0, 1]"
        _epoxy_interp_thresh = value


# Properties must exist as attributes of a class, rather than of an instance.
# However, modules are (roughly) singleton instances of an internal module class.
# As a result, we use the following trick to replace this module in the system with
# an instance of the above class, for which properties are class attributes
# See the top reply on this StackOverflow for more information on the trick:
# https://stackoverflow.com/questions/2447353/getattr-on-a-module
sys.modules["config"] = _Config()
