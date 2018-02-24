# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from ..qt import QtWidgets


class FlatButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(FlatButton, self).__init__(*args, **kwargs)
        self.setFlat(True)

class HorizontalLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(HorizontalLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class VerticalLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(VerticalLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)