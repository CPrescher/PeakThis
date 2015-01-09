# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from PyQt4 import QtGui

from controller.MainController import MainController


class DataModelTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.data = self.controller.data

