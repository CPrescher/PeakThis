# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'
import numpy as np
from model.Spectrum import Spectrum

from PyQt4 import QtCore, QtGui

class DataModel(QtCore.QObject):
    spectrum_changed = QtCore.pyqtSignal(Spectrum)

    def __init__(self):
        super(DataModel, self).__init__()
        self.models = []
        self.models_sum = Spectrum()
        self.background_model = None

        self.spectrum = Spectrum()
        self.residual = Spectrum()

    def load_data(self, filename):
        self.spectrum.load(filename)
        self.spectrum_changed.emit(self.spectrum)

    def save_data(self, filename):
        pass

    def add_model(self, model_name):
        pass

    def del_model(self, index):
        pass

    def save_models(self, filename):
        pass

    def load_models(self, filename):
        pass

    def fit_data(self):
        pass
