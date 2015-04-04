# -*- coding: utf8 -*-
from __future__ import absolute_import

from PyQt4 import QtGui
import sys
from controller.MainController import MainController

def run():
    app = QtGui.QApplication(sys.argv)
    main_controller = MainController()
    main_controller.show_view()
    app.exec_()


if __name__ == '__main__':
    run()