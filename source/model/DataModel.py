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

    model_sum_changed = QtCore.pyqtSignal(Spectrum)

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
        # emit background model
        x, y = self.spectrum.data
        bkg_y = self.background_model.data(x)
        if bkg_y is not None:
            self.background_spectrum = Spectrum(x, bkg_y)
        else:
            self.background_spectrum = Spectrum(np.array([]), np.array([]))
        self.background_changed.emit(self.background_spectrum)
        #emit the points:
        x, y = self.background_model.get_points()
        self.background_points_changed.emit(Spectrum(x, y))

        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        for ind in range(len(self.models)):
            self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))


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

        self.model_sum_changed.emit(self.get_model_sum_spectrum())

    def get_model_spectrum(self, ind):
        x, _ = self.spectrum.data


        y = self.models[ind].quick_eval(x)

        _, y_bkg = self.background_spectrum.data
        if x.shape == y_bkg.shape:
            y+=y_bkg

        return Spectrum(x, y)

    def update_model_parameter(self, ind, x, y):

        y_bkg = self.background_model.data(x)
        if y_bkg is not None:
            y-=y_bkg
        self.models[ind].update_current_parameter(x, y)
        self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))
        self.model_sum_changed.emit(self.get_model_sum_spectrum())

    def pick_model_parameters(self, ind, x, y):
        y_bkg = self.background_model.data(x)
        if y_bkg is not None:
            y-=y_bkg
        more_parameters_available = self.models[ind].pick_parameter(x, y)
        self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))
        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        return more_parameters_available

    def del_model(self, index=-1):
        del self.models[index]
        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        self.model_deleted.emit(index)

    def get_model_sum_spectrum(self):
        x, _ = self.spectrum.data
        sum = np.zeros(x.shape)
        _, y_bkg = self.background_spectrum.data
        if x.shape == y_bkg.shape:
            sum+=y_bkg

        for model in self.models:
            sum+= model.quick_eval(x)
        return Spectrum(x, sum)

    def save_models(self, filename):
        pass

    def load_models(self, filename):
        pass

    def fit_data(self):
        pass
