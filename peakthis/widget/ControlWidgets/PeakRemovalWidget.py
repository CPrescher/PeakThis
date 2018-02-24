# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from ..qt import  QtWidgets


from ..CustomWidgets.GuiElements import FlatButton


class PeakRemovalWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PeakRemovalWidget, self).__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        self.subtract_btn = FlatButton('Subtract Peaks')
        self.subtract_btn.setFixedHeight(50)
        self.save_btn = FlatButton('Save Data')
        self.save_btn.setFixedHeight(50)
        self.layout.addWidget(self.subtract_btn)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)
