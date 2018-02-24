# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(
    name='peakthis',
    version=0.2,
    license='GPL3',
    author='Clemens Prescher',
    author_email="clemens.prescher@gmail.com",
    url='https://github.com/CPrescher/PeakThis',
    install_requires=['numpy', 'scipy', 'lmfit', 'pyqtgraph'],
    test_requires=['numpy', 'scipy', 'lmfit', 'pyqtgraph', 'pytest'],
    description='Simple Peak Fitting software where peaks and background can be defined visually',
    classifiers=['Intended Audience :: Science/Research',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 ],
    packages=find_packages(),
    package_data={'peakthis': ['widget/DioptasStyle.qss',
                              ]},
    scripts=['scripts/peakthis']
)