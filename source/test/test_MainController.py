# -*- coding: utf8 -*-

__author__ = 'Clemens Prescher'

import unittest
import os

import numpy as np
from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui

from controller.MainController import MainController


test_directory = os.path.dirname(os.path.realpath(__file__))


class MainControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.data = self.controller.data
        self.main_widget = self.controller.main_widget
        self.model_widget = self.controller.main_widget.control_widget.model_widget
        self.spectrum_widget = self.controller.main_widget.spectrum_widget

    def tearDown(self):
        del self.app

    def add_model(self, model_type_ind=0):
        QTest.mouseClick(self.main_widget.model_add_btn, QtCore.Qt.LeftButton)
        self.main_widget.model_selector_dialog.model_list.setCurrentRow(model_type_ind)
        QTest.mouseClick(self.main_widget.model_selector_dialog.ok_btn, QtCore.Qt.LeftButton)

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def test_loading_data(self):
        spectrum_filename = os.path.join(test_directory, 'TestData', 'spectrum1.txt')
        self.controller.load_data(spectrum_filename)
        self.assertEqual(self.data.spectrum.name, 'spectrum1')
        spec_x, spec_y = self.data.spectrum.data

        file_data = np.loadtxt(spectrum_filename)
        self.assertTrue(np.array_equal(spec_x, file_data[:, 0]))
        self.assertTrue(np.array_equal(spec_y, file_data[:, 1]))

    def test_adding_models(self):
        QTest.mouseClick(self.model_widget.add_btn, QtCore.Qt.LeftButton)
        self.assertTrue(self.model_widget.model_selector_dialog.isVisible())

        self.assertGreater(self.model_widget.model_selector_dialog.model_list.count(), 0)
        self.model_widget.model_selector_dialog.model_list.setCurrentRow(0)

        # closing the model dialog
        QTest.mouseClick(self.model_widget.model_selector_dialog.ok_btn, QtCore.Qt.LeftButton)
        self.assertFalse(self.model_widget.model_selector_dialog.isVisible())

        # now we impose that there is a new items list in on the right:
        self.assertGreater(self.model_widget.model_list.count(), 0)

        # by doing this there should also be a new model in the DataModel
        self.assertGreater(len(self.data.models), 0)

        # and in the spectrum
        self.assertGreater(self.spectrum_widget.get_number_of_model_plots(), 0)

    def test_updating_model_parameters(self):
        self.add_model()

        start_x, start_y = self.spectrum_widget.get_model_plot_data(0)
        self.model_widget.parameter_table.item(0, 1).setText('2.0')
        self.model_widget.parameter_table.item(1, 1).setText('3.0')
        self.model_widget.parameter_table.item(2, 1).setText('3.0')

        after_x, after_y = self.spectrum_widget.get_model_plot_data(0)
        self.array_almost_equal(start_x, after_x)
        self.array_not_almost_equal(start_y, after_y)

    def test_copy_models(self):
        self.add_model()
        QTest.mouseClick(self.main_widget.model_copy_btn, QtCore.Qt.LeftButton)
        self.assertEqual(self.model_widget.model_list.count(), 2)
        self.assertEqual(self.spectrum_widget.get_number_of_model_plots(), 2)

    def test_deleting_models(self):
        # adding some models:
        self.add_model()
        self.add_model()
        self.add_model()

        self.assertEqual(self.model_widget.model_list.count(), 3)
        self.assertEqual(self.spectrum_widget.get_number_of_model_plots(), 3)

        # now we delete the press delete and see what happens:
        QTest.mouseClick(self.main_widget.model_delete_btn, QtCore.Qt.LeftButton)
        self.assertEqual(self.model_widget.model_list.count(), 2)
        self.assertEqual(self.spectrum_widget.get_number_of_model_plots(), 2)

        # now add two more and select a peak in between
        self.add_model()
        self.add_model()
        self.model_widget.model_list.setCurrentRow(2)
        QTest.mouseClick(self.main_widget.model_delete_btn, QtCore.Qt.LeftButton)

    def test_fitting_a_model_and_updating_gui(self):
        # create dummy data
        x = np.linspace(-3, 3)
        intercept =  0.1
        slope = 2.
        y = intercept + x * slope

        self.data.set_data(x, y)
        self.add_model(2)

        before_x, before_y = self.spectrum_widget.get_model_plot_data(0)
        QTest.mouseClick(self.main_widget.fit_btn, QtCore.Qt.LeftButton)

        # model should have changed after it was fitted
        after_x, after_y = self.spectrum_widget.get_model_plot_data(0)
        self.array_not_almost_equal(before_y, after_y)

        # there should now also be a residual in the lower plot:
        residual_x, residual_y = self.spectrum_widget.get_residual_plot_data()
        self.array_almost_equal(after_x, residual_y)
        self.assertAlmostEqual(np.sum(residual_y), 0)






