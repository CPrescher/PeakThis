# -*- coding: utf8 -*-

import numpy as np

from view.MainWidget import MainView

__author__ = 'Clemens Prescher'


class MainController(object):
    def __init__(self):
        self.main_widget = MainView()
        self.plot_some_data()
        self.create_subscriptions()

    def show_view(self):
        self.main_widget.show()

    def plot_some_data(self):
        x = np.linspace(0, 30, 1000)
        y = np.sin(x)
        self.main_widget.spectrum_widget.plot_data(x, y)
        self.main_widget.spectrum_widget.plot_background(x,-0.5+0.03*x)

    def create_subscriptions(self):
        self.main_widget.control_widget.model_widget.add_btn.clicked.connect(self.add_model)

    def add_model(self, *args, **kwargs):
        self.main_widget.control_widget.model_widget.show_model_selector_dialog()