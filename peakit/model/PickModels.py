# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from lmfit.models import Model, ConstantModel, LinearModel, QuadraticModel
import numpy as np

from .PickModel import PickModel


class PickConstantModel(ConstantModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickConstantModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 1)

    def update_current_parameter(self, x, y):
        self.set_parameter_value('c', y)


class PickLinearModel(LinearModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickLinearModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.set_parameter_value('intercept', 0)
        self.set_parameter_value('slope', 0)

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.set_parameter_value('intercept', y)
        elif self.current_pick == 1:
            slope = (y - self.pick_points[0].y) / \
                    (x - self.pick_points[0].x)
            self.set_parameter_value('slope', slope)
            self.set_parameter_value('intercept',  y - slope * x)


class PickQuadraticModel(QuadraticModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickQuadraticModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 3)

        self.set_parameter_value('a', 0)
        self.set_parameter_value('b', 0)
        self.set_parameter_value('c', 0)

        # parameters for defining the initial fit
        self.x = np.array([0., 0., 0.])
        self.y = np.array([0., 0., 0.])

    def update_current_parameter(self, x, y):

        self.x[self.current_pick] = float(x)
        self.y[self.current_pick] = float(y)

        if self.current_pick == 0:
            self.set_parameter_value('c', y)
        elif self.current_pick == 1:
            slope = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
            self.set_parameter_value('b', slope)
            self.set_parameter_value('c', self.y[0] - slope * self.x[0])
        elif self.current_pick == 2:
            a, b, c = np.polyfit(self.x, self.y, 2)
            self.set_parameter_value('a', a)
            self.set_parameter_value('b', b)
            self.set_parameter_value('c', c)


s2pi = np.sqrt(2*np.pi)

def gaussian(x, amplitude=1.0, center=0.0, sigma=1.0):
    """1 dimensional gaussian:
    gaussian(x, amplitude, center, sigma)
    """
    return (amplitude/(s2pi*sigma)) * np.exp(-(1.0*x-center)**2 /(2*sigma**2))


class GaussianModel(Model):
    __doc__ = gaussian.__doc__
    def __init__(self, *args, **kwargs):
        super(GaussianModel, self).__init__(gaussian, *args, **kwargs)

class PickGaussianModel(GaussianModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickGaussianModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.set_parameter_value('amplitude', 0)
        self.set_parameter_value('center', 0)
        self.set_parameter_value('sigma', 0.5)

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.set_parameter_value('center', x)
            # fwhm = self.parameters['sigma'].value*2.354820
            self.set_parameter_value('amplitude', y * self.get_parameter_value('sigma') * 2.506470408)
        elif self.current_pick == 1:
            new_sigma = abs(x - self.get_parameter_value('center')) * 0.8493218001909796
            if new_sigma==0:
                new_sigma = 0.5
            self.set_parameter_value('sigma', new_sigma)
            self.set_parameter_value('amplitude', self.pick_points[0].y * self.get_parameter_value('sigma') * 2.506470408)


def lorentzian( x, center=0, fwhm=0.3, intensity=1):
    hwhm=fwhm*0.5
    return intensity/(np.pi*hwhm*(1+((x-center)/hwhm)**2))

class LorentzianModel(Model):
    __doc__ = lorentzian.__doc__
    def __init__(self, *args, **kwargs):
        super(LorentzianModel, self).__init__(lorentzian, *args, **kwargs)

class LorentzianPickModel(LorentzianModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(LorentzianPickModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.set_parameter_value('intensity', 0)
        self.set_parameter_value('center', 0)
        self.set_parameter_value('fwhm', 0.5)

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.set_parameter_value('center', x)
            self.set_parameter_value('intensity', y * np.pi*self.get_parameter_value('fwhm')/2.)
        elif self.current_pick == 1:
            new_fwhm = abs(x - self.get_parameter_value('center'))*2
            if new_fwhm==0:
                new_fwhm = 0.5
            self.set_parameter_value('fwhm', new_fwhm)
            self.set_parameter_value('intensity', self.pick_points[0].y * np.pi*self.get_parameter_value('fwhm')/2.)


models_dict = {
    "Gaussian Model": PickGaussianModel,
    "Lorentzian Model": LorentzianPickModel,
    "Quadratic Model": PickQuadraticModel,
    "Linear Model": PickLinearModel,
    # "Constant Model": PickConstantModel,
}


        