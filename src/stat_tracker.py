import numpy as np
import files
import config


class StatTracker:
    """
    This is a Singleton tracker that records the tube coverage and slice area statistics. The initialization must supply
    radial_precision and slice_count.

    It might be worth refactored this to be a module.

    ...

    Attributes
    ----------
    __instance: StatTracker
        if not None, reference to the one StatTracker in existence
    coverage_stats: arr
        2D boolean data array for tube coverage statistics

    Methods
    -------
    get_instance()
        If __instance is None, instantiates a new StatTracker. Otherwise, returns the reference to the StatTracker.
    initialize_matrix(rows, cols)
        Initializes stats to be a 2D array of False, with dimensions rows by cols
    update_area(row, col, value)
        Sets the row, col element of stats to boolean value
    get_stats():
        Returns a 2D array of integers, 0 or 1, representing stats
    """

    __instance = None
    coverage_stats = []
    area_stats = []

    @staticmethod
    def get_instance():
        """Static access method."""
        if StatTracker.__instance is None:
            StatTracker()
        return StatTracker.__instance

    def __initialize_coverage(self):
        # Setting dtype to np.bool_ makes np interpret the 0's as Falses
        self.coverage_stats = np.zeros(
            (files.slices.slice_total, config.num_wedges), dtype=np.bool_
        )

    def __initialize_area(self):
        self.area_stats = np.zeros((files.slices.slice_total,), dtype=np.uint8)

    def update_coverage(self, wedge, value: bool):
        self.coverage_stats[files.slices.current_slice][wedge] = value

    def update_area(self, slice_index, value):
        self.area_stats[slice_index] = value

    def get_stats(self):
        """returns coverage and area stats. Coverage stats are returned as a 0/1 array rather than a boolean array"""
        coverage_stats = np.where(self.coverage_stats, 1, 0)
        return coverage_stats, self.area_stats

    def __init__(self):
        """Virtually private constructor."""
        if StatTracker.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            StatTracker.__instance = self
            self.__initialize_area()
            self.__initialize_coverage()
