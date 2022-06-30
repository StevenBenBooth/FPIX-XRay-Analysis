"""This module stores the global state, both gui settings and save paths"""
# I'm justifying this global state with the fact that it is only set in one
# part of the gui running, then never again (ideally). It may be worth locking
# the state after it is set in the appropriate part of the program so it then
# can't be changed. One way of doing this would be to refactor the properties into
# one __setattr__ function, since the getters don't have custom behavior anyway
import sys
import os
from os.path import join
from tkinter import messagebox


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
        self.slice_path = None
        self.tube_path = None
        self.save_path = None
        self.processed_path = None

    def check_path(self, path):
        if not os.path.isdir(path):
            message = "{} does not define a valid folder path".format(path)
            messagebox.showerror("Not a path", message)
            raise NotADirectoryError(message)
        return path

    def set_paths(self, base_path):
        try:
            base_path = self.check_path(
                base_path
            )  # Obvious candidate for a setattr refactor, same as the next two
            self.slice_path = self.check_path(join(base_path, "Pictures"))
            self.tube_path = self.check_path(join(base_path, "Tube"))
            self.processed_path = join(base_path, "Processed")
            self.save_path = base_path
        except NotADirectoryError as e:
            raise e

        try:
            os.mkdir(self.processed_path)
        except FileExistsError:
            pass

    def update_params(self, *values):
        (
            self.num_wedges,
            self.epoxy_low_bound,
            self.highlight_low_bound,
            self.cf_top_bound,
            self.cf_bottom_bound,
            self.cf_thickness,
            self.highlight_thickness,
            self.interpolation_thresh,
            self.epoxy_interp_thresh,
        ) = values

    def get_params(self):  # TODO: make this stuff prettier if possible
        return [
            self.num_wedges,
            self.epoxy_low_bound,
            self.highlight_low_bound,
            self.cf_top_bound,
            self.cf_bottom_bound,
            self.cf_thickness,
            self.highlight_thickness,
            self.interpolation_thresh,
            self.epoxy_interp_thresh,
        ]

    def intcast(self, val, name):
        assert isinstance(name, str), "The variable name should be a string"
        try:
            return int(val)
        except ValueError:
            raise ValueError(name + " must be an integer or coercible to an integer")

    def floatcast(self, val, name):
        assert isinstance(name, str), "The variable name should be a string"
        try:
            return float(val)
        except ValueError:
            raise ValueError(name + " must be an float or coercible to a float")

    # TODO: Refactor to only use __setattr__ in order to avoid bloat from getters
    @property
    def tube_radius(self):
        return self._tube_radius

    @tube_radius.setter
    def tube_radius(self, val):
        radius = self.intcast(val, "Radius")
        assert radius > 0, "Tube radius must be positive"
        self._tube_radius = radius

    @property
    def num_wedges(self):
        return self._num_wedges

    @num_wedges.setter
    def num_wedges(self, val):
        num = self.intcast(val, "Wedge count")
        assert num > 0, "The number of interpolation slices must be positive"
        self._num_wedges = num

    @property
    def epoxy_low_bound(self):
        return self._epoxy_low_bound

    @epoxy_low_bound.setter
    def epoxy_low_bound(self, val):
        low_bound = self.intcast(val, "Epoxy low bound")
        assert (
            low_bound >= 0 and low_bound <= 255
        ), "The low cutoff for epoxy must be an integer in 0, ..., 255"
        self._epoxy_low_bound = low_bound

    @property
    def highlight_low_bound(self):
        return self._highlight_low_bound

    @highlight_low_bound.setter
    def highlight_low_bound(self, val):
        low_bound = self.intcast(val, "Highlight low cutoff")
        assert (
            low_bound >= 0 and low_bound <= 255
        ), "The cutoff intensity for highlights must be in 0, ..., 255"
        assert (
            low_bound > self.epoxy_low_bound
        ), "The low cutoff for highlights must be greater than the low cutoff for epoxy"
        self._highlight_low_bound = low_bound

    @property
    def cf_top_bound(self):
        return self._cf_top_bound

    @cf_top_bound.setter
    def cf_top_bound(self, val):
        top_bound = self.intcast(val, "Carbon Foam top bound")

        assert top_bound >= 0, "The carbon foam top bound must be a nonnegative integer"
        self._cf_top_bound = top_bound

    @property
    def cf_bottom_bound(self):
        return self._cf_bottom_bound

    @cf_bottom_bound.setter
    def cf_bottom_bound(self, val):
        bottom_bound = self.intcast(val, "Carbon Foam bottom bound")

        assert (
            bottom_bound >= 0
        ), "The carbon foam bottom bound must be a nonnegative integer"
        assert (
            bottom_bound > self._cf_top_bound
        ), "Counterintuitively, the cf bottom bound should should be higher than the cf top bound (numpy indexing is the opposite of how the picture looks)"
        self._cf_bottom_bound = bottom_bound

    @property
    def cf_thickness(self):
        return self._cf_thickness

    @cf_thickness.setter
    def cf_thickness(self, val):
        thickness = self.intcast(val, "Carbon Foam thickness")
        assert thickness >= 0, "Carbon foam thickness should be nonnegative"
        self._cf_thickness = thickness

    @property
    def highlight_thickness(self):
        return self._highlight_thickness

    @highlight_thickness.setter
    def highlight_thickness(self, val):
        thickness = self.intcast(val, "Highlight thickness")

        assert thickness >= 0, "Highlight thickness should be nonnegative"
        self._highlight_thickness = thickness

    @property
    def interpolation_thresh(self):
        return self._interpolation_thresh

    @interpolation_thresh.setter
    def interpolation_thresh(self, val):
        thresh = self.floatcast(val, "Interpolation threshold")
        assert (
            thresh >= 0 and thresh <= 1
        ), "The interpolation threshold is a proportion, so must be in the interval [0, 1]"
        self._interpolation_thresh = thresh

    @property
    def epoxy_interp_thresh(self):
        return self._epoxy_interp_thresh

    @epoxy_interp_thresh.setter
    def epoxy_interp_thresh(self, val):
        thresh = self.floatcast(val, "Epoxy threshold")
        assert (
            thresh >= 0 and thresh <= 1
        ), "The epoxy interpolation threshold is a proportion, so must be in the interval [0, 1]"
        self._epoxy_interp_thresh = thresh


# Properties must exist as attributes of a class, rather than of an instance.
# However, modules are (roughly) singleton instances of an internal module class.
# As a result, we use the following trick to replace this module in the system with
# an instance of the above class, for which properties are class attributes
# See the top reply on this StackOverflow for more information on the trick:
# https://stackoverflow.com/questions/2447353/getattr-on-a-module
sys.modules["config"] = _Config()
