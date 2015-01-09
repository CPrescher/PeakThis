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
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)


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
        # and clicks define and sees that she can add points by clicking into the spectrum

        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        click_points_x = [2, 4, 5]
        click_points_y = [3, 4, 5]

        for ind in range(len(click_points_x)):
            self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(click_points_x[ind],
                                                                                   click_points_y[ind])

        bkg_points_x, bkg_points_y = self.main_widget.spectrum_widget.background_scatter_item.getData()

        self.array_almost_equal(bkg_points_x, click_points_x)
        self.array_almost_equal(bkg_points_y, click_points_y)

        # every time she clicks in the spectrum after the first three clicks she sees that the background changes
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(5.4, 2.4)

        x, bkg_y1 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_almost_equal(self.x, x)

        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(6.3, 2.5)
        x, bkg_y2 = self.main_widget.spectrum_widget.background_plot_item.getData()

        self.array_not_almost_equal(bkg_y1, bkg_y2)

        # after inspecting her data and background model she thinks that 'pchip' is maybe not the best way to
        # approximate the background so she tries the spline model, and she notices how the background is change

        self.main_widget.background_method_cb.setCurrentIndex(1)

        x, bkg_y3 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_not_almost_equal(bkg_y2, bkg_y3)

        # then she sees that spline is actually worse and goes back to pchip
        self.main_widget.background_method_cb.setCurrentIndex(0)
        x, bkg_y4 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_almost_equal(bkg_y4, bkg_y2)





        # then she starts the background selection process

        # and clicks on several points in the spectrum to add them to the background spectrum

        # then she adds 2 gaussian peaks because they seem to be

        self.fail("Finish the Test!")