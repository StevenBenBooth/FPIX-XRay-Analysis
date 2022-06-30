"""This module stores the global state, both gui settings and save paths"""
import sys
import os
import numpy as np
from os.path import join
from tkinter import messagebox
from typing import Any


class _Config:
    def __init__(self):
        self.tube_radius = 33

        # Use width then height
        self.cropping_bounds = (75, 575, 100, 350)

        self.num_wedges = 50
        self.epoxy_low_bound = 40
        # highlight low bound is both the lower intensity bound for pixels to be
        # interpreted as a highlight and the upper bound for them to be interpreted as epoxy
        self.highlight_low_bound = 210
        self.cf_top_bound = (
            70  # top_bound < bottom_bound because indexing starts from the top
        )
        # These bounds should be set to the y-position of somewhere in the carbon foam layers
        self.cf_bottom_bound = 173
        self.cf_thickness = 7
        self.highlight_thickness = 9
        self.interpolation_thresh = 0.7
        self.epoxy_interp_thresh = 0
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
        return (
            self.num_wedges,
            self.epoxy_low_bound,
            self.highlight_low_bound,
            self.cf_top_bound,
            self.cf_bottom_bound,
            self.cf_thickness,
            self.highlight_thickness,
            self.interpolation_thresh,
            self.epoxy_interp_thresh,
        )

    def js_cast(self, fun, val, name):
        assert isinstance(name, str), "The variable name should be a string"
        try:
            return fun(val)
        except ValueError:
            raise ValueError(name + " was not coercible to the correct type")

    def intcast(self, val, name):
        return self.js_cast(int, val, name)

    def floatcast(self, val, name):
        return self.js_cast(float, val, name)

    def parse_bounds(self, val, name):
        # Converts the JavaScript string representation of the integer bounds into a tuple of integers
        return self.js_cast(
            lambda x: tuple(
                map(self.intcast, x.replace("\[|]", "")).split(", ")),
            val,
            name,
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        val = None
        if __name == "tube_radius":
            val = self.intcast(__value, "Radius")
            assert val > 0, "Tube radius must be positive"

        elif __name == "num_wedges":
            val = self.intcast(__value, "Wedge count")
            assert val > 0, "The number of interpolation slices must be positive"

        elif __name == "epoxy_low_bound":
            val = self.intcast(__value, "Epoxy low bound")
            assert (
                val >= 0 and val <= 255
            ), "The low cutoff for epoxy must be an integer in 0, ..., 255"

        elif __name == "highlight_low_bound":
            val = self.intcast(__value, "Highlight low cutoff")
            assert (
                val >= 0 and val <= 255
            ), "The cutoff intensity for highlights must be in 0, ..., 255"
            assert (  # note: this assertion makes things complicated, restricting one to updating the epoxy bound before the highlight bound (or else an exception could crop up)
                val > self.epoxy_low_bound
            ), "The low cutoff for highlights must be greater than the low cutoff for epoxy"

        elif __name == "cf_top_bound":
            val = self.intcast(__value, "Carbon Foam top bound")
            assert val >= 0, "The carbon foam top bound must be a nonnegative integer"

        elif __name == "cf_bottom_bound":
            val = self.intcast(__value, "Carbon Foam bottom bound")
            assert (
                val >= 0
            ), "The carbon foam bottom bound must be a nonnegative integer"
            assert (
                val > self.cf_top_bound
            ), "Counterintuitively, the cf bottom bound should should be higher than the cf top bound (numpy indexing is the opposite of how the picture looks)"

        elif __name == "cf_thickness":
            val = self.intcast(__value, "Carbon Foam thickness")
            assert val >= 0, "Carbon foam thickness should be nonnegative"

        elif __name == "highlight_thickness":
            val = self.intcast(__value, "Highlight thickness")
            assert val >= 0, "Highlight thickness should be nonnegative"

        elif __name == "interpolation_thresh":
            val = self.floatcast(__value, "Interpolation threshold")
            assert (
                val >= 0 and val <= 1
            ), "The interpolation threshold is a proportion, so must be in the interval [0, 1]"

        elif __name == "epoxy_interp_thresh":
            val = self.floatcast(__value, "Epoxy threshold")
            assert (
                val >= 0 and val <= 1
            ), "The epoxy interpolation threshold is a proportion, so must be in the interval [0, 1]"

        elif __name == "cropping_bounds":
            val = self.parse_bounds(__value, "Cropping bounds")
            left, right, top, bottom = val
            assert np.any(
                np.array(map(lambda x: not isinstance(x, int), val))
            ), "Bounds must be integers"
            assert (
                top < bottom
            ), "Due to numpy conventions, the top bound must have a lower value than the bottom bound for the image's height"

            assert (
                left < right
            ), "The left bound must have a lower value than the right value for image cropping"

        if val is not None:
            super().__setattr__(
                __name, val
            )  # Has to add the typecast value for non-string attributes
        else:
            super().__setattr__(
                __name, __value
            )  # Default behavior for adding attribute to this object

    def __getattribute__(self, __name: str) -> Any:
        return super().__getattribute__(__name)


# To take advantage of overwriting __setattr__, we need to use a trick.
# We use the following trick to replace this module in the system with
# an instance of the above class, so that our custom __setattr__ behavior gets
# called whenever we change an attribute of the program.
# See the top reply on this StackOverflow for more information on the trick:
# https://stackoverflow.com/questions/2447353/getattr-on-a-module

# If, at some point in the future, one wishes to add specialized behavior on
# getters as well as setters, it may be worth replacing this implementation with
# one using properties. Modules are (roughly) singleton instances of an internal
# module class. However, properties must exist as attributes of a class, rather
# than of an instance, so we use this trick to replace the (instance) module with
# the above class.
# Release 0.1.0 has an implementation of these attributes as properties.
sys.modules["config"] = _Config()
