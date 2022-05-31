"""This module stores the global settings inputted from the gui, to be used for processing"""
import sys

from numpy import isin


class _Config:
    def __init__(self):
        self._tube_radius = 33
        self._num_wedges = 50
        self._epoxy_low_bound = 40
        # highlight low bound is both the lower intensity bound for pixels to be
        # interpreted as a highlight and the upper bound for them to be interpreted as epoxy
        self._highlight_low_bound = 210
        self._cf_top_bound = (
            70  # top_bound < bottom_bound because indexing starts from the top
        )
        # These bounds should be set to the y-position of somewhere in the carbon foam layers
        self._cf_bottom_bound = 173
        self._cf_thickness = 7
        self._highlight_thickness = 9
        self._interpolation_thresh = 0.7
        self._epoxy_interp_thresh = 0

    def update_values(self, values):
        self._num_wedges,
        self._epoxy_low_bound,
        self._highlight_low_bound,
        self._cf_top_bound,
        self._cf_bottom_bound,
        self._cf_thickness,
        self._highlight_thickness,
        self._interpolation_thresh,
        self._epoxy_interp_thresh = values

    # TODO: Refactor to only use __setattr__ in order to avoid bloat from getters
    @property
    def tube_radius(self):
        return self._tube_radius

    @tube_radius.setter
    def tube_radius(self, value):
        try:
            radius = int(value)
        except ValueError:
            raise ValueError("Value must be an integer or coercible to an integer")
        assert radius > 0, "Tube radius must be positive"
        self._tube_radius = radius

    @property
    def num_wedges(self):
        return self._num_wedges

    @num_wedges.setter
    def num_wedges(self, value):
        assert (
            isinstance(value, int) and value > 0
        ), "The number of interpolation slices must be a positive integer"
        self._num_wedges = value

    @property
    def epoxy_low_bound(self):
        return self._epoxy_low_bound

    @epoxy_low_bound.setter
    def epoxy_low_bound(self, value):
        assert (
            isinstance(value, int) and value >= 0 and value <= 255
        ), "The low cutoff for epoxy must be an integer in 0, ..., 255"
        assert (
            value < self._highlight_low_bound
        ), "The low cutoff for epoxy must be below the low cutoff for highlights"
        self._epoxy_low_bound = value

    @property
    def highlight_low_bound(self):
        return self._highlight_low_bound

    @highlight_low_bound.setter
    def highlight_low_bound(self, value):
        assert (
            isinstance(value, int) and value >= 0 and value <= 255
        ), "The cutoff intensity for highlights must be an integer in 0, ..., 255"
        assert (
            value > self._highlight_low_bound
        ), "The low cutoff for epoxy must be below the low cutoff for highlights"

        self._highlight_low_bound = value

    @property
    def cf_top_bound(self):
        return self._cf_top_bound

    @cf_top_bound.setter
    def cf_top_bound(self, value):
        assert (
            isinstance(value, int) and value >= 0
        ), "The carbon foam top bound must be a nonnegative integer"
        assert (
            value < self._cf_bottom_bound
        ), "Counterintuitively, the cf top bound should should be lower than the cf bottom bound (numpy indexing)"
        self._cf_top_bound = value

    @property
    def cf_bottom_bound(self):
        return self._cf_bottom_bound

    @cf_bottom_bound.setter
    def cf_top_bound(self, value):
        assert (
            isinstance(value, int) and value >= 0
        ), "The carbon foam top bound must be a nonnegative integer"
        assert (
            value > self._cf_top_bound
        ), "Counterintuitively, the cf bottom bound should should be higher than the cf top bound (numpy indexing is the opposite of how the picture looks)"
        self._cf_bottom_bound = value

    @property
    def cf_thickness(self):
        return self._cf_thickness

    @cf_thickness.setter
    def cf_thickness(self, value):
        assert (
            isinstance(value, int) and value >= 0
        ), "carbon foam thickness should be a nonnegative integer"
        self._cf_thickness = value

    @property
    def highlight_thickness(self):
        return self._highlight_thickness

    @highlight_thickness.setter
    def highlight_thickness(self, value):
        assert (
            isinstance(value, int) and value >= 0
        ), "highlight thickness should be a nonnegative integer"
        self._highlight_thickness = value

    @property
    def interpolation_thresh(self):
        return self._interpolation_thresh

    @interpolation_thresh.setter
    def interpolation_thresh(self, value):
        assert (
            value >= 0 and value <= 1
        ), "The interpolation threshold is a proportion, so must be in the interval [0, 1]"
        self._interpolation_thresh = value

    @property
    def epoxy_interp_thresh(self):
        return self._epoxy_interp_thresh

    @epoxy_interp_thresh.setter
    def epoxy_interp_thresh(self, value):
        assert (
            value >= 0 and value <= 1
        ), "The epoxy interpolation threshold is a proportion, so must be in the interval [0, 1]"
        self._epoxy_interp_thresh = value


# Properties must exist as attributes of a class, rather than of an instance.
# However, modules are (roughly) singleton instances of an internal module class.
# As a result, we use the following trick to replace this module in the system with
# an instance of the above class, for which properties are class attributes
# See the top reply on this StackOverflow for more information on the trick:
# https://stackoverflow.com/questions/2447353/getattr-on-a-module
sys.modules["config"] = _Config()
