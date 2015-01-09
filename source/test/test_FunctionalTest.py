# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest

import numpy as np

from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt

import tempfile

from controller.MainController import MainController
from model.PickModels import PickGaussianModel


class PeakThisFunctionalTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.main_widget = self.controller.main_widget
        self.model_widget = self.controller.main_widget.control_widget.model_widget
        self.create_spectrum()

    def tearDown(self):
        del self.app


    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1-array2), 0)


    def create_spectrum(self):
        self.x = np.linspace(0, 10, 145)
        self.y = np.zeros(self.x.shape)
        gauss_curve = PickGaussianModel()
        gauss_curve.parameters['center'].value = 6
        gauss_curve.parameters['amplitude'].value = 10
        self.y += gauss_curve.quick_eval(self.x)
        gauss_curve.parameters['center'].value = 2
        gauss_curve.parameters['amplitude'].value = 6
        self.y += gauss_curve.quick_eval(self.x)

        self.temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        np.savetxt(self.temp_file, np.dstack((self.x, self.y))[0])
        self.temp_file.close()


    def test_use_case_for_raman_fitting(self):
        # Edith opens PeakThis sees the open file button and loads her spectrum into the program
        # she clicks the button and loads a spectrum
        self.controller.load_data(self.temp_file.name)

        # Edith notices that the spectrum is immediately shown in the graph window
        QtGui.QApplication.processEvents()
        x, y = self.main_widget.spectrum_widget.data_plot_item.getData()

        self.array_almost_equal(x, self.x)
        self.array_almost_equal(y, self.y)

        # then she sees that she can define a background for her Data
        # she chooses that the standard pchip should be fine to model her data
        # and clicks define and sees that she can miracoulsy change the background by adding points in the spectrum

        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(2, 3)
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(4, 4)
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(5, 5)
        x, bkg_y = self.main_widget.spectrum_widget.background_plot_item.getData()

        self.array_almost_equal(self.x, x)
        # everytime she clicks somewhere in the spectrum graph she sees that the background changes
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(5.4, 2.4)

        x, bkg_y2 = self.main_widget.spectrum_widget.background_plot_item.getData()

        self.array_not_almost_equal(bkg_y, bkg_y2)


        # then she starts the background selection process

        # and clicks on several points in the spectrum to add them to the background spectrum

        # then she adds 2 gaussian peaks because they seem to be

        self.fail("Finish the Test!")