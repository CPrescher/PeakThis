# -*- coding: utf8 -*-

import numpy as np

from views.MainView import MainView

__author__ = 'Clemens Prescher'


class MainController(object):
    def __init__(self):
        self.main_view = MainView()

        self.plot_some_data()

        self.main_view.show()

    def plot_some_data(self):
        x = np.linspace(0, 30, 1000)
        y = np.sin(x)
        self.main_view.spectrum_widget.plot_data(x, y)
        self.main_view.spectrum_widget.plot_background(x,np.cos(x))