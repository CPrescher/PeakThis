# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'
from model.Spectrum import Spectrum
from model.BackgroundModel import BackgroundModel

from PyQt4 import QtCore

class DataModel(QtCore.QObject):
    spectrum_changed = QtCore.pyqtSignal(Spectrum)
    background_changed = QtCore.pyqtSignal(Spectrum)
    background_points_changed = QtCore.pyqtSignal(Spectrum)

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
        self.background_spectrum = Spectrum(x, bkg_y)
        self.background_changed.emit(self.background_spectrum)
        #emit the points:
        x, y = self.background_model.get_points()
        self.background_points_changed.emit(Spectrum(x,y))

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
