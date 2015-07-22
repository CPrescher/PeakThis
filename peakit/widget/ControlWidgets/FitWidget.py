# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import  QtGui


from ..CustomWidgets.GuiElements import FlatButton


class FitWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FitWidget, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(5)

        self.fit_btn = FlatButton('Fit')
        self.main_layout.addWidget(self.fit_btn)

        self.setLayout(self.main_layout)

