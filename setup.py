# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from distutils.core import setup
import os
import sys
from subprocess import call
import importlib

print("Installing peakthis\n. Checking for required packages.\n")

try:
    import PyQt4
except ImportError:
    print("\n----------------------------\n"
          "PyQt4 is not available please install the library or use a premade python distribution like Anaconda, "
          "Enthought or WinPython with PyQt4 included.\n")
    sys.exit(-1)

def check_if_library_exists_and_install(library_name):
    try:

        importlib.import_module(library_name)
    except ImportError:
        print("\n----------------------------\n"
              "{} library was not found. The peakit setup will try to install it via pip.".format(library_name))
        answer = raw_input("Proceed ([y]/n)? ").upper()
        if answer is "Y" or answer is "YES" or answer is '':
            call("pip install {}".format(library_name), shell=True)
        else:
            print("Aborting peakit installation.")
            sys.exit(-1)

check_if_library_exists_and_install("numpy")
check_if_library_exists_and_install("scipy")
check_if_library_exists_and_install("pyqtgraph")
check_if_library_exists_and_install("lmfit")


setup(name="peakit",
      version='0.1.1',
      description="Interactive peak fitting software.",
      author='Clemens Prescher',
      author_email='clemens.prescher@gmail.com',
      url='https://github.com/Luindil/peakit',
      license='GPL3',
      platforms=['Windows', 'Linux', 'Mac OS X'],
      classifiers=['Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
      ],
      packages=['peakit', 'peakit.controller', 'peakit.model', 'peakit.view', 'peakit.test'],
      package_data={'peakit.view':['*.qss', os.path.join('images', '*')],
                    'peakit.test':[os.path.join('data', '*')]},
      scripts=['scripts/peakit'])
