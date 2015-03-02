# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'


from PyQt4 import QtGui
import sys
from controller.MainController import MainController

def run():
    app = QtGui.QApplication(sys.argv)
    main_controller = MainController()
    main_controller.show_view()
    app.exec_()