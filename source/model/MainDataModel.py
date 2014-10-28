# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'


class MainDataModel(object):
    def __init__(self):
        self.models = []
        self.background_model = None

        self.spectrum = Spectrum()
        self.residual = Spectrum()

    def load_data(self, filename):
        pass

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


class Spectrum(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    @property
    def data(self):
        return self.x, self.y

