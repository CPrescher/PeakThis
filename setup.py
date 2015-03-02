# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from distutils.core import setup
import os

setup(name="PeakThis",
      version='0.1',
      description="Interactive peak fitting software.",
      author='Clemens Prescher',
      author_email='clemens.prescher@gmail.com',
      url='https://github.com/Luindil/PeakThis',
      license='GPL3',
      platforms=['Windows', 'Linux', 'Mac OS X'],
      classifiers=['Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
      ],
      packages=['PeakThis', 'PeakThis.controller', 'PeakThis.model', 'PeakThis.view', 'PeakThis.test'],
      package_dir={'PeakThis': 'source'},
      package_data={'PeakThis.view':['*.qss', os.path.join('images', '*')],
                    'PeakThis.test':[os.path.join('data', '*')]},
      scripts=['PeakThis'])
