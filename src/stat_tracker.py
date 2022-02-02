import numpy as np


class StatTracker:
    """
    This is a Singleton tracker that records the tube coverage and slice area statistics. The initialization must supply
    radial_precision and slice_count.

    If you ever have a need to instantiate two trackers, rewrite this to not be a Singleton.

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
        radial_precision and slice_count must be supplied on first call, and must not on later references
    initialize_matrix(rows, cols)
        Initializes stats to be a 2D array of False, with dimensions rows by cols
    update_value(row, col, value)
        Sets the row, col element of stats to boolean value
    get_stats():
        Returns a 2D array of integers, 0 or 1, representing stats
    """
    __instance = None
    coverage_stats = []
    area_stats = []

    @staticmethod
    def get_instance(radial_precision=None, slice_count=None):
        """ Static access method. """
        if StatTracker.__instance is None:
            assert radial_precision is not None and slice_count is not None, "On first reference, must pass in " \
                                                                             "radial_precision and slice_count"
            StatTracker(radial_precision, slice_count)
        else:
            assert radial_precision is None and slice_count is None, "After instantiation, you cannot change dimensions"
        return StatTracker.__instance

    def __initialize_coverage(self, rows, cols):
        # Setting dtype to np.bool_ makes np interpret the 0's as Falses
        self.coverage_stats = np.zeros((rows, cols), dtype=np.bool_)

    def __initialize_area(self, slices):
        self.area_stats = np.zeros((slices,), dtype=np.uint8)

    def update_coverage(self, row, col, value: bool):
        self.coverage_stats[row][col] = value

    def update_area(self, slice_index, value):
        self.area_stats[slice_index] = value

    def get_stats(self):
        self.coverage_stats = np.where(self.coverage_stats, 1, 0)
        return self.coverage_stats

    def __init__(self, radial_num, slice_num):
        """ Virtually private constructor. """
        if StatTracker.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            StatTracker.__instance = self
            self.__initialize_area(slice_num)
            self.__initialize_coverage(slice_num, radial_num)
