# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from ..qt import QtGui, QtCore, QtWidgets

from .ExpandableBox import ExpandableBox
from .GuiElements import FlatButton, HorizontalLine, VerticalLine
from .SpectrumWidget import SpectrumWidget


class NumberTextField(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(NumberTextField, self).__init__(*args, **kwargs)
        self.setValidator(QtGui.QDoubleValidator())
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    def value(self):
        return float(str(self.text()).replace(',', '.'))