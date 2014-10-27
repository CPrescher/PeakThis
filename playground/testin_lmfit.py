# -*- coding: utf8 -*-
# - GUI program for fast processing of 2D X-ray data
#     Copyright (C) 2014  Clemens Prescher (clemens.prescher@gmail.com)
#     GSECARS, University of Chicago
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Clemens Prescher'


import lmfit
import numpy as np
import matplotlib.pyplot as plt

# creating random data
x = np.linspace(-10, 10, 1000)
y = np.sin(2*x)

y += np.random.random(np.size(y))*1.5
plt.plot(x,y )

def func(x, a, b):
    return b+np.sin(a*x)

model = lmfit.Model(func, independent_vars=['x'])
result = model.fit(y,a=1.6, b=0, x=x)

print result.params['a']
print result.params['b']

plt.plot(x,func(x, result.params['a'].value, result.params['b'].value), 'r-', lw=3)
plt.show()


