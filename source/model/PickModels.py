# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from lmfit.models import *
from model.PickModel import PickModel


class PickConstantModel(ConstantModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickConstantModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 1)

    def update_current_parameter(self, x, y):
        self.parameters['c'].value = y


class PickLinearModel(LinearModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickLinearModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.parameters['intercept'].value = 0
        self.parameters['slope'].value = 0

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.parameters['intercept'].value = y
        elif self.current_pick == 1:
            slope = (y - self.pick_points[0].y) / \
                    (x - self.pick_points[0].x)
            self.parameters['slope'].value = slope
            self.parameters['intercept'].value = y - slope * x


class PickQuadraticModel(QuadraticModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickQuadraticModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 3)

        self.parameters['a'].value = 0
        self.parameters['b'].value = 0
        self.parameters['c'].value = 0

        # parameters for defining the initial fit
        self.x = np.array([0., 0., 0.])
        self.y = np.array([0., 0., 0.])

    def update_current_parameter(self, x, y):
        self.x[self.current_pick] = float(x)
        self.y[self.current_pick] = float(y)
        if self.current_pick == 0:
            self.parameters['c'].value = y
        elif self.current_pick == 1:
            slope = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
            self.parameters['b'].value = slope
            self.parameters['c'].value = self.y[0] - slope * self.x[0]
        elif self.current_pick == 2:
            a, b, c = np.polyfit(self.x, self.y, 2)
            self.parameters['a'].value = a
            self.parameters['b'].value = b
            self.parameters['c'].value = c


class PickGaussianModel(GaussianModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickGaussianModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.parameters['amplitude'].value = 0
        self.parameters['center'].value = 0
        self.parameters['sigma'].value = 0.5

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.parameters['center'].value = x
            # fwhm = self.parameters['sigma'].value*2.354820
            self.parameters['amplitude'].value = y * self.parameters['sigma'].value * 2.506470408
        elif self.current_pick == 1:
            self.parameters['sigma'].value = abs(x - self.parameters['center']) * 0.8493218001909796
            self.parameters['amplitude'].value = self.pick_points[0].y * self.parameters['sigma'].value * 2.506470408





        