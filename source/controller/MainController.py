# -*- coding: utf8 -*-

import numpy as np
from PyQt4 import QtCore, QtGui

from view.MainWidget import MainWidget
from model.DataModel import DataModel

__author__ = 'Clemens Prescher'


class MainController(object):
    def __init__(self):
        self.main_widget = MainWidget()
        self.data = DataModel()
        self.plot_some_data()
        self.create_subscriptions()

    def show_view(self):
        self.main_widget.show()

    def plot_some_data(self):
        x = np.linspace(0, 30, 1000)
        y = np.sin(x)
        self.main_widget.spectrum_widget.plot_data(x, y)
        self.main_widget.spectrum_widget.plot_background(x, -0.5 + 0.03 * x)

    def create_subscriptions(self):
        self.connect_click_function(self.main_widget.load_file_btn, self.load_data)

        self.data.spectrum_changed.connect(self.main_widget.spectrum_widget.plot_data_spectrum)



        self.main_widget.control_widget.model_widget.add_btn.clicked.connect(self.add_model)

    def connect_click_function(self, emitter, function):
        self.main_widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def add_model(self, *args, **kwargs):
        self.main_widget.control_widget.model_widget.show_model_selector_dialog()

    def load_data(self, filename = None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_widget, "Load Data File",
                                                             '', ('Data (*.txt)')))
        if filename is not '':
            self.data.load_data(filename)
