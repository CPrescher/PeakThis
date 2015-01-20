# -*- coding: utf8 -*-
from PyQt4 import QtGui
import sys
from controller.MainController import MainController

__author__ = 'Clemens Prescher'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle('plastique')
    main_controller = MainController()
    main_controller.show_view()
    app.exec_()