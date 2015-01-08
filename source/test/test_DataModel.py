# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import numpy as np
from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui


from controller.MainController import MainController


class DataModelTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.data = self.controller.data

