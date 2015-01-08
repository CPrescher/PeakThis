# -*- coding: utf8 -*-

__author__ = 'Clemens Prescher'

import unittest
import numpy as np
from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui


from controller.MainController import MainController


class MainControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.data = self.controller.data
        self.main_view = self.controller.main_widget
        self.model_widget = self.controller.main_widget.control_widget.model_widget

    def tearDown(self):
        del self.app

    def test_adding_models(self):
        QTest.mouseClick(self.model_widget.add_btn, QtCore.Qt.LeftButton)
        self.assertTrue(self.model_widget.model_selector_dialog.isVisible())

        self.model_widget.model_selector_dialog.model_list.setCurrentRow(1)
        QTest.mouseClick(self.model_widget.model_selector_dialog.ok_btn, QtCore.Qt.LeftButton)

        self.assertFalse(self.model_widget.model_selector_dialog.isVisible())

    def test_loading_data(self):
        self.controller.load_data("TestData/spectrum1.txt")
        self.assertEqual(self.data.spectrum.name,'spectrum1')
        spec_x, spec_y = self.data.spectrum.data

        file_data = np.loadtxt("TestData/spectrum1.txt")
        self.assertTrue(np.array_equal(spec_x, file_data[:,0]))
        self.assertTrue(np.array_equal(spec_y, file_data[:,1]))


