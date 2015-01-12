# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np
from PyQt4 import QtCore

from model.Spectrum import Spectrum
from model.BackgroundModel import BackgroundModel


class DataModel(QtCore.QObject):
    spectrum_changed = QtCore.pyqtSignal(Spectrum)

    background_changed = QtCore.pyqtSignal(Spectrum)
    background_points_changed = QtCore.pyqtSignal(Spectrum)

    models_changed = QtCore.pyqtSignal()

    def __init__(self):
        super(DataModel, self).__init__()
        self.models = []
        self.models_sum = Spectrum()

        self.background_model = BackgroundModel()
        self.background_model.background_model_changed.connect(self.background_model_changed)

        self.spectrum = Spectrum()
        self.background_spectrum = Spectrum()
        self.residual = Spectrum()

    def load_data(self, filename):
        self.spectrum.load(filename)
        self.spectrum_changed.emit(self.spectrum)

    def save_data(self, filename):
        pass

    def background_model_changed(self):
        #emit background model
        x, y = self.spectrum.data
        bkg_y = self.background_model.data(x)
        if bkg_y is not None:
            self.background_spectrum = Spectrum(x, bkg_y)
        else:
            self.background_spectrum = Spectrum(np.array([]),np.array([]))
        self.background_changed.emit(self.background_spectrum)
        #emit the points:
        x, y = self.background_model.get_points()
        self.background_points_changed.emit(Spectrum(x,y))

    def add_model(self, model):
        self.models.append(model)
        self.models_changed.emit()

    def del_model(self, index):
        del self.models[index]
        self.models_changed.emit()

    def save_models(self, filename):
        pass

    def load_models(self, filename):
        pass

    def fit_data(self):
        pass
