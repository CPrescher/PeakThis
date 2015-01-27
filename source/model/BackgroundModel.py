# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np
from scipy.interpolate import UnivariateSpline, PchipInterpolator
from PyQt4 import QtCore


class BackgroundModel(QtCore.QObject):
    background_model_changed = QtCore.pyqtSignal()

    def __init__(self, method='pchip'):
        """
        :param method: possible values are 'pchip' and 'spline'
        :return:
        """
        super(BackgroundModel, self).__init__()
        self.x = np.array([])
        self.y = np.array([])
        self.method = method

    def add_point(self, x, y):
        self.x = np.append(self.x, x)
        self.y = np.append(self.y, y)

        self.background_model_changed.emit()

    def delete_point_close_to(self, x, y, max_distance=2):
        if len(self.x) > 0:
            distances = np.sqrt((np.array(self.x) - x) ** 2 + (np.array(self.y) - y) ** 2)
            ind = np.argsort(distances)

            self.x = np.delete(self.x, [ind[0]])
            self.y = np.delete(self.y, [ind[0]])

            self.background_model_changed.emit()

    def get_points(self):
        return self.x, self.y

    def set_method(self, method):
        self.method = method
        self.background_model_changed.emit()

    def data(self, x):
        x = np.asarray(x)
        if len(self.x) == 0:
            return np.zeros(x.shape)
        elif len(self.x) == 1:
            return np.ones(x.shape) * self.y[0]
        elif len(self.x) == 2:
            m = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
            n = self.y[1] - self.x[1] * m
            return m * x + n
        elif len(self.x) >= 2:
            ind = np.argsort(self.x)
            self.x = self.x[ind]
            self.y = self.y[ind]
            if self.method == 'pchip':
                # first everything needs to be sorted
                pchip_interpolator = PchipInterpolator(self.x, self.y, extrapolate=True)
                y = pchip_interpolator(x)
            elif self.method == 'spline':
                spline_interpolator = UnivariateSpline(self.x, self.y, k=3, s=0)
                y = spline_interpolator(x)
            else:
                y = None
            return y




