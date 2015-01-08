# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui

from controller.MainController import MainController


class MainControllerTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.main_widget = self.controller.main_widget
        self.model_widget = self.controller.main_widget.control_widget.model_widget

    def test_use_case_for_raman_fitting(self):

        # Edith opens PeakThis sees the open file button and loads her spectrum into the program


        self.fail("Finish the Test!")