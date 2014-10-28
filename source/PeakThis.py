# -*- coding: utf8 -*-
from PyQt4 import QtGui
import sys
from controllers.MainController import MainController

__author__ = 'Clemens Prescher'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_controller = MainController()
    app.exec_()