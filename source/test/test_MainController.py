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
        self.main_view = self.controller.main_view
        self.model_widget = self.controller.main_view.control_widget.model_widget

    def tearDown(self):
        pass

    def test_adding_models(self):
        QTest.mouseClick(self.model_widget.add_btn, QtCore.Qt.LeftButton)
        self.assertTrue(self.model_widget.model_selector_dialog.isVisible())

        self.model_widget.model_selector_dialog.model_list.setCurrentRow(1)
        QTest.mouseClick(self.model_widget.model_selector_dialog.ok_btn, QtCore.Qt.LeftButton)

        self.assertFalse(self.model_widget.model_selector_dialog.isVisible())
