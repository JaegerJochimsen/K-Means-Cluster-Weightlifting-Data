"""
Author: Jaeger Jochimsen

Resources: Python Programming in Context 2ed by Miller and Ranum pg.242

This file contains the class Point() which is a point object containing the coordinates of each data point.
"""


class Point(object):
    """
    A Point will contain all the coordinates of the original data point along with some helpful methods.
    """

    def __init__(self, cal, fat, cho, pro, water, expected_vol, actual_vol, wrk_fraction):
        self.cal = cal
        self.fat = fat
        self.cho = cho
        self.pro = pro
        self.water = water
        self.expected = expected_vol
        self.actual = actual_vol
        self.work = wrk_fraction

    def __repr__(self):
        return f'Point({self.cal}, {self.fat}, {self.cho}, {self.pro}, {self.water}, {self.expected}, {self.actual}, {self.work})'

    def __str__(self):
        return f'Point({self.cal}, {self.fat}, {self.cho}, {self.pro}, {self.water}, {self.expected}, {self.actual}, {self.work})'
