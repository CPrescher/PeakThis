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

    def create_spectrum(self):
        self.x = np.linspace(0,10,100)
        self.y = np.zeros(self.x.shape)
        gauss_curve = PickGaussianModel()
        gauss_curve.parameters['center'].value = 6
        gauss_curve.parameters['amplitude'].value = 10
        self.y += gauss_curve.quick_eval(self.x)
        gauss_curve.parameters['center'].value = 2
        gauss_curve.parameters['amplitude'].value = 6
        self.y += gauss_curve.quick_eval(self.x)

        self.temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        np.savetxt(self.temp_file, (self.x,self.y))
        self.temp_file.close()


    def test_use_case_for_raman_fitting(self):

        # Edith opens PeakThis sees the open file button and loads her spectrum into the program
        # she clicks the button and loads a spectrum
        self.controller.load_data(self.temp_file.name)

        # Edith notices that the spectrum is immediately shown in the graph window
        x, y = self.main_widget.spectrum_widget.data_plot_item.getData()

        self.assertTrue(np.array_equal(x, self.x))
        self.assertTrue(np.array_equal(y, self.y))


        #chooses the right

        self.fail("Finish the Test!")