# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from .widget.qt import QtWidgets
import sys
from .controller.MainController import MainController

def run():
    app = QtWidgets.QApplication(sys.argv)
    main_controller = MainController()
    main_controller.show_view()
    app.exec_()