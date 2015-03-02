# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest

import numpy as np
from PyQt4 import QtGui

from ..view.SpectrumWidget import SpectrumWidget
from ..model.Spectrum import Spectrum


class SpectrumWidgetTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.spectrum_widget = SpectrumWidget()

        self.dummy_x = np.linspace(0, 5, 100)
        self.dummy_y = self.dummy_x ** 2
        self.dummy_spectrum = Spectrum(self.dummy_x, self.dummy_y)

    def tearDown(self):
        del self.app

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def test_creating_data_plot(self):
        self.spectrum_widget.plot_data(self.dummy_x, self.dummy_y)
        x_plot, y_plot = self.spectrum_widget.get_plot_data()
        self.array_almost_equal(self.dummy_x, x_plot)
        self.array_almost_equal(self.dummy_y, y_plot)

    def test_creating_background_plot(self):
        self.spectrum_widget.plot_background(self.dummy_x, self.dummy_y)
        self.spectrum_widget.plot_background_points(self.dummy_x, self.dummy_y)

        x_plot, y_plot = self.spectrum_widget.get_background_plot_data()
        self.array_almost_equal(self.dummy_x, x_plot)
        self.array_almost_equal(self.dummy_y, y_plot)

        x_points, y_points = self.spectrum_widget.get_background_points_data()
        self.array_almost_equal(self.dummy_x, x_points)
        self.array_almost_equal(self.dummy_y, y_points)

    def test_adding_model_plot(self):
        # adding the model
        self.spectrum_widget.add_model()
        self.assertGreater(self.spectrum_widget.get_number_of_model_plots(), 0)

        # changing the data
        self.spectrum_widget.update_model(0, self.dummy_x, self.dummy_y)
        x_model, y_model = self.spectrum_widget.get_model_plot_data(0)
        self.array_almost_equal(self.dummy_x, x_model)
        self.array_almost_equal(self.dummy_y, y_model)

        # changing the data using a spectrum
        self.spectrum_widget.update_model_spectrum(0, Spectrum(x_model, y_model * 2))
        x_model, y_model = self.spectrum_widget.get_model_plot_data(0)
        self.array_almost_equal(self.dummy_x, x_model)
        self.array_almost_equal(self.dummy_y * 2, y_model)

        # adding another model using a spectrum
        self.spectrum_widget.add_model(Spectrum(self.dummy_x / 2.0, self.dummy_y * 1.5))
        x_model, y_model = self.spectrum_widget.get_model_plot_data(1)
        self.array_almost_equal(self.dummy_x / 2, x_model)
        self.array_almost_equal(self.dummy_y * 1.5, y_model)

    def test_deleting_model_plots(self):
        self.spectrum_widget.add_model(self.dummy_spectrum)
        self.spectrum_widget.add_model(self.dummy_spectrum)
        self.spectrum_widget.add_model(self.dummy_spectrum)
        self.spectrum_widget.add_model(self.dummy_spectrum)
        self.spectrum_widget.add_model(self.dummy_spectrum)
        self.assertEqual(self.spectrum_widget.get_number_of_model_plots(), 5)

        self.spectrum_widget.del_model(4)
        self.assertEqual(self.spectrum_widget.get_number_of_model_plots(), 4)
        self.spectrum_widget.del_model()
        self.spectrum_widget.del_model()
        self.spectrum_widget.del_model()
        self.spectrum_widget.del_model()
        self.assertEqual(self.spectrum_widget.get_number_of_model_plots(), 0)