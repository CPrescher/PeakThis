# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from lmfit.models import LinearModel
import numpy as np

import matplotlib.pyplot as plt

testmodel = LinearModel()
testmodel.set_param_hint('slope', value=5)
testmodel.set_param_hint('intercept', value=4)
parameters = testmodel.make_params()
print parameters.keys()

print parameters['slope'].value

# parameters['slope'].value = 5
# parameters['intercept'].value = 2

x = np.linspace(0,10)
y = testmodel.eval(parameters, x=x)


plt.plot(x,y)
plt.show()


