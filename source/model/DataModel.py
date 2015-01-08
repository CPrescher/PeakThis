# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from model.Spectrum import Spectrum


class DataModel(object):
    def __init__(self):
        self.models = []
        self.models_sum = Spectrum()
        self.background_model = None

        self.spectrum = Spectrum()
        self.residual = Spectrum()

    def load_data(self, filename):
        self.spectrum.load(filename)

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