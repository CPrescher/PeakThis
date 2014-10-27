# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'


from lmfit.models import LorentzianModel
import numpy as np
import matplotlib.pyplot as plt
pi = 3.141592653589793238462643
def my_lorentzian(x, center, fwhm, intensity):
    hwhm=fwhm*0.5
    return intensity/(pi*hwhm*(1+((x-center)/hwhm)**2))

x = np.linspace(-100,100, 10000)

lorentzian_model = LorentzianModel()
y1 = lorentzian_model.eval(x=x, center=0, sigma=0.5, amplitude=10)
y2 = my_lorentzian(x, 0, 1, 10)

print np.trapz(y1, x=x)
print np.trapz(y2, x=x)

plt.plot(x, y1)
plt.plot(x, y2)
plt.show()
