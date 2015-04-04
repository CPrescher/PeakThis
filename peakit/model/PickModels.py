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
            try:
                slope = (y - self.pick_points[0].y) / \
                        (x - self.pick_points[0].x)
                self.set_parameter_value('slope', slope)
                self.set_parameter_value('intercept',  y - slope * x)
            except ZeroDivisionError:
                pass


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
            try:
                a, b, c = np.polyfit(self.x, self.y, 2)
                self.set_parameter_value('a', a)
                self.set_parameter_value('b', b)
                self.set_parameter_value('c', c)
            except np.linalg.LinAlgError:
                self.set_parameter_value('a', 0)


s2pi = np.sqrt(2*np.pi)

def gaussian(x, center=0.0, fwhm=1.0, intensity=1):
    """1 dimensional gaussian:
    gaussian(x, amplitude, center, sigma)
    """
    hwhm=fwhm/2.0
    return intensity*0.8326/(hwhm*1.7725)*np.exp(-(x-center)**2/(hwhm/0.8326)**2)

class GaussianModel(Model):
    __doc__ = gaussian.__doc__
    def __init__(self, *args, **kwargs):
        super(GaussianModel, self).__init__(gaussian, *args, **kwargs)

class PickGaussianModel(GaussianModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PickGaussianModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.set_parameter_value('intensity', 0)
        self.set_parameter_value('center', 0)
        self.set_parameter_value('fwhm', 0.5)

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.set_parameter_value('center', x)
            # fwhm = self.parameters['sigma'].value*2.354820
            self.set_parameter_value('intensity', y * 1.7724538509055159*self.get_parameter_value('fwhm')/1.6652)
        elif self.current_pick == 1:
            new_fwhm = abs(x - self.get_parameter_value('center')) * 2
            if new_fwhm==0:
                new_fwhm = 0.5
            self.set_parameter_value('fwhm', new_fwhm)
            self.set_parameter_value('intensity', self.pick_points[0].y * \
                                     1.7724538509055159*self.get_parameter_value('fwhm')/1.6652)


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



def pseudo_voigt(x, center=0, fwhm=0.3, intensity=1, n=0.5):
    return n*lorentzian(x, center, fwhm, intensity)+(1-n)*gaussian(x, center, fwhm, intensity)



class PseudoVoigtModel(Model):
    __doc__ = lorentzian.__doc__
    def __init__(self, *args, **kwargs):
        super(PseudoVoigtModel, self).__init__(pseudo_voigt, *args, **kwargs)

class PseudoVoigtPickModel(PseudoVoigtModel, PickModel):
    def __init__(self, *args, **kwargs):
        super(PseudoVoigtPickModel, self).__init__(*args, **kwargs)
        PickModel.__init__(self, 2)

        self.set_parameter_value('intensity', 0)
        self.set_parameter_value('center', 0)
        self.set_parameter_value('fwhm', 0.5)
        self.set_parameter_value('n', 0.5)

    def update_current_parameter(self, x, y):
        if self.current_pick == 0:
            self.set_parameter_value('center', x)
            self.set_parameter_value('intensity', y * np.pi*self.get_parameter_value('fwhm') *0.25  + \
                                                  y * 1.7724538509055159*self.get_parameter_value('fwhm')/1.6652 * 0.5)
        elif self.current_pick == 1:
            new_fwhm = abs(x - self.get_parameter_value('center'))*2
            if new_fwhm==0:
                new_fwhm = 0.5
            self.set_parameter_value('fwhm', new_fwhm)
            self.set_parameter_value('intensity',
                                     self.pick_points[0].y * np.pi*self.get_parameter_value('fwhm') *0.25  + \
                                     self.pick_points[0].y * 1.7724538509055159*self.get_parameter_value('fwhm')/1.6652 * 0.5)


models_dict = {
    "Gaussian Model": PickGaussianModel,
    "Lorentzian Model": LorentzianPickModel,
    "PseudoVoigt Model": PseudoVoigtPickModel,
    "Quadratic Model": PickQuadraticModel,
    "Linear Model": PickLinearModel,
    # "Constant Model": PickConstantModel,
}


        