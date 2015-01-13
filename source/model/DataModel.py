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

    model_added = QtCore.pyqtSignal()
    model_deleted = QtCore.pyqtSignal(int)
    model_parameters_changed = QtCore.pyqtSignal(int, Spectrum)

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
        self.model_added.emit()

    def update_model(self, ind, parameters):
        for key, val in parameters.iteritems():
            self.models[ind].parameters[key].value = parameters[key].value
            self.models[ind].parameters[key].vary = parameters[key].vary
            self.models[ind].parameters[key].min = parameters[key].min
            self.models[ind].parameters[key].max = parameters[key].max
        self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))

    def get_model_spectrum(self, ind):
        x, _ = self.spectrum.data
        y = self.models[ind].quick_eval(x)
        return Spectrum(x, y)

    def del_model(self, index=-1):
        del self.models[index]
        self.model_deleted.emit(index)

    def save_models(self, filename):
        pass

    def load_models(self, filename):
        pass

    def fit_data(self):
        pass
