# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np
from PyQt4 import QtCore
from lmfit import Parameters

from .Spectrum import Spectrum
from .BackgroundModel import BackgroundModel


class DataModel(QtCore.QObject):
    spectrum_changed = QtCore.pyqtSignal(Spectrum)

    background_changed = QtCore.pyqtSignal(Spectrum)
    background_points_changed = QtCore.pyqtSignal(Spectrum)

    model_added = QtCore.pyqtSignal()
    model_deleted = QtCore.pyqtSignal(int)
    model_parameters_changed = QtCore.pyqtSignal(int, Spectrum)

    model_sum_changed = QtCore.pyqtSignal(Spectrum)

    residual_changed = QtCore.pyqtSignal(Spectrum)

    def __init__(self):
        super(DataModel, self).__init__()
        self.models = []
        self.models_sum = Spectrum()

        self.background_model = BackgroundModel()
        self.background_model.background_model_changed.connect(self.background_model_changed)
        self._background_subtracted_flag = False

        self.spectrum = Spectrum()
        self.background_spectrum = Spectrum([], [])
        self.residual = Spectrum()

        self.background_model_changed()

    def load_data(self, filename):
        self.spectrum.load(filename)
        self.background_model_changed()
        self.spectrum_changed.emit(self.get_spectrum())

    def set_spectrum_data(self, x, y):
        self.spectrum.data = x, y
        self.background_model_changed()
        self.spectrum_changed.emit(self.get_spectrum())

    def get_spectrum(self):
        if self._background_subtracted_flag and len(self.background_spectrum):
            return self.spectrum - self.background_spectrum
        else:
            return self.spectrum

    def get_spectrum_data(self):
        return self.get_spectrum().data

    def add_background_model_point(self, x, y):
        if self._background_subtracted_flag:
            y_bkg = self.background_model.data(x)
            self.background_model.add_point(x, y+y_bkg)
        else:
            self.background_model.add_point(x, y)
        self.background_points_changed.emit(self.get_background_points_spectrum())

    def remove_background_model_point_close_to(self, x, y):
        if self._background_subtracted_flag:
            y += self.background_model.data(x)
        self.background_model.delete_point_close_to(x, y)
        self.background_points_changed.emit(self.get_background_points_spectrum())

    def background_model_changed(self):
        # emit background model
        x, y = self.spectrum.data
        bkg_y = self.background_model.data(x)
        if bkg_y is not None:
            self.background_spectrum = Spectrum(x, bkg_y)
        else:
            self.background_spectrum = Spectrum(np.array([]), np.array([]))
        self.background_changed.emit(self.get_background_spectrum())

        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        for ind in range(len(self.models)):
            self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))

        if self._background_subtracted_flag:
            self.spectrum_changed.emit(self.get_spectrum())

    def set_background_subtracted(self, bool):
        self._background_subtracted_flag = bool

        self.spectrum_changed.emit(self.get_spectrum())
        self.model_sum_changed.emit(self.get_model_sum_spectrum())

        self.background_changed.emit(self.get_background_spectrum())
        self.background_points_changed.emit(self.get_background_points_spectrum())

        for ind in range(len(self.models)):
            self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))

    def get_background_spectrum(self):
        if self._background_subtracted_flag:
            x, y = self.spectrum.data
            return Spectrum(x, np.zeros(y.shape))
        else:
            return self.background_spectrum

    def get_background_points_spectrum(self):
        if self._background_subtracted_flag:
            x, y = self.background_model.get_points()
            y -= self.background_model.data(x)
            return Spectrum(x, y)
        else:
            x, y = self.background_model.get_points()
            return Spectrum(x, y)


    def add_model(self, model):
        self.models.append(model)
        self.model_added.emit()

    def update_model(self, ind, parameters):
        for key, val in parameters.iteritems():
            if not key.startswith(self.models[ind].prefix):
                model_key = self.models[ind].prefix + key
            else:
                model_key = key
            self.models[ind].parameters[model_key].value = parameters[key].value
            self.models[ind].parameters[model_key].vary = parameters[key].vary
            self.models[ind].parameters[model_key].min = parameters[key].min
            self.models[ind].parameters[model_key].max = parameters[key].max

        self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))
        self.model_sum_changed.emit(self.get_model_sum_spectrum())

    def get_model_spectrum(self, ind):
        x, _ = self.spectrum.data

        y = self.models[ind].quick_eval(x)

        if not self._background_subtracted_flag:
            _, y_bkg = self.background_spectrum.data
            if x.shape == y_bkg.shape:
                y += y_bkg

        return Spectrum(x, y)

    def get_model_sum_spectrum(self):
        x, _ = self.spectrum.data
        sum = np.zeros(x.shape)

        if not self._background_subtracted_flag:
            _, y_bkg = self.background_spectrum.data
            if x.shape == y_bkg.shape:
                sum += y_bkg

        sum = reduce(lambda a, y: a+y.quick_eval(x), self.models, sum)
        return Spectrum(x, sum)

    def update_current_model_parameter(self, ind, x, y):
        y -= self.background_model.data(x)

        self.models[ind].update_current_parameter(x, y)
        self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))
        self.model_sum_changed.emit(self.get_model_sum_spectrum())

    def pick_current_model_parameters(self, ind, x, y):
        y -= self.background_model.data(x)

        more_parameters_available = self.models[ind].pick_parameter(x, y)
        self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))
        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        return more_parameters_available

    def del_model(self, index=-1):
        del self.models[index]
        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        self.model_deleted.emit(index)

    def save_models(self, filename):
        pass

    def load_models(self, filename):
        pass

    def fit_data(self):
        if len(self.models) == 0:
            return

        # adding models and parameters by using reduce is the shortest and simplest way
        # otherwise there are strange if conditions and for loops due to each case with 1 or 2
        # or more models...
        combined_model = reduce(lambda a, x: a + x, self.models)
        combined_parameters = reduce(lambda a, x: a + x.parameters, self.models, Parameters())

        x, y = self.spectrum.data
        x_bkg, y_bkg = self.background_spectrum.data
        if x.shape == y_bkg.shape:
            y -= y_bkg

        out = combined_model.fit(y, params=combined_parameters, x=x)

        # save the data into the model
        for ind, model in enumerate(self.models):
            for key, val in out.best_values.iteritems():
                if key in model.parameters.keys():
                    model.parameters[key].value = val
            self.model_parameters_changed.emit(ind, self.get_model_spectrum(ind))

        self.model_sum_changed.emit(self.get_model_sum_spectrum())
        self.residual_changed.emit(Spectrum(x, out.residual))