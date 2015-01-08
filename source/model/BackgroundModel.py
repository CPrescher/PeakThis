# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np
from scipy.interpolate import UnivariateSpline, PchipInterpolator
from PyQt4 import QtCore




class BackgroundModel(QtCore.QObject):
    def __init__(self, method = 'pchip'):
        """
        :param method: possible values are 'pchip' and 'spline'
        :return:
        """
        super(BackgroundModel, self).__init__()
        self.x = []
        self.y = []
        self.method = method

    def add_point(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def delete_point_close_to(self, x, y, max_distance=2):
        distances = np.sqrt((np.array(self.x)-x)**2+(np.array(self.y)-y)**2)
        ind = np.argsort(distances)
        if distances[ind[0]]<max_distance:
            self.x.remove(self.x[ind[0]])
            self.y.remove(self.y[ind[0]])

    def data(self, x):
        if self.method == 'pchip':
            pchip_interpolator = PchipInterpolator(self.x, self.y, extrapolate=True)
            y = pchip_interpolator(x)
        else:
            spline_interpolator = UnivariateSpline(self.x, self.y)
            y= spline_interpolator(x)
        return y




