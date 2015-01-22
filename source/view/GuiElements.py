# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui


class FlatButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(FlatButton, self).__init__(*args, **kwargs)
        self.setFlat(True)

class HorizontalLine(QtGui.QFrame):
    def __init__(self, parent=None):
        super(HorizontalLine, self).__init__(parent)
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class VerticalLine(QtGui.QFrame):
    def __init__(self, parent=None):
        super(VerticalLine, self).__init__(parent)
        self.setFrameShape(QtGui.QFrame.VLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)