# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel, LorentzianModel, VoigtModel, PseudoVoigtModel, LinearModel

gauss_curve = GaussianModel(prefix='gauss1')
gauss_curve.set_param('amplitude', 10)
gauss_curve.set_param('center', 1)
gauss_curve.set_param('sigma', 1.9)
lorentz_curve = LorentzianModel(prefix='lorentz1')
lorentz_curve.set_param('amplitude', 10)
lorentz_curve.set_param('center', 2.4)
lorentz_curve.set_param('sigma', 0.3)

voigt_curve = VoigtModel(prefix='voigt1')
voigt_curve.set_param('amplitude', 10)
voigt_curve.set_param('center', 0)
voigt_curve.set_param('sigma', 0.9)

pseudo_voigt_curve = PseudoVoigtModel(prefix='lorentz1')
pseudo_voigt_curve.set_param('amplitude', 10)
pseudo_voigt_curve.set_param('center', 0)
pseudo_voigt_curve.set_param('sigma', 3)

background = LinearModel()
background.set_param('intercept', 1.3)
background.set_param('slope', 0.13)

compound_model = gauss_curve + lorentz_curve + background

x = np.linspace(-100, 100, 10000)
y =pseudo_voigt_curve.eval(x=x)

print np.trapz(y,x)

plt.plot(x,y)
plt.show()