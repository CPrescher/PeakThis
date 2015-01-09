# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np
from scipy.interpolate import UnivariateSpline, PchipInterpolator
from PyQt4 import QtCore

from model.Spectrum import Spectrum




class BackgroundModel(QtCore.QObject):
    background_model_changed = QtCore.pyqtSignal()

    def __init__(self, method = 'pchip'):
        """
        :param method: possible values are 'pchip' and 'spline'
        :return:
        """
        super(BackgroundModel, self).__init__()
        self.x = np.array([])
        self.y = np.array([])
        self.method = method

    def add_point(self, x, y):
        print x, y
        self.x = np.append(self.x, x)
        self.y = np.append(self.y, y)

        self.background_model_changed.emit()

    def delete_point_close_to(self, x, y, max_distance=2):
        distances = np.sqrt((np.array(self.x)-x)**2+(np.array(self.y)-y)**2)
        ind = np.argsort(distances)
        if distances[ind[0]]<max_distance:
            self.x.remove(self.x[ind[0]])
            self.y.remove(self.y[ind[0]])

        self.background_model_changed.emit()

    def data(self, x):
        if len(self.x)==0:
            return np.zeros(x.shape)
        elif len(self.x)==1:
            return np.ones(x.shape)*self.y[0]
        elif len(self.x)>=3:
            if self.method == 'pchip':
                #first everything needs to be sorted
                ind = np.argsort(self.x)
                print ind
                self.x = self.x[ind]
                self.y = self.y[ind]
                pchip_interpolator = PchipInterpolator(self.x, self.y, extrapolate=True)
                y = pchip_interpolator(x)
            else:
                spline_interpolator = UnivariateSpline(self.x, self.y)
                y= spline_interpolator(x)
            return y




