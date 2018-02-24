# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from ..qt import QtGui, QtCore, QtWidgets

from ..CustomWidgets import FlatButton


class BackgroundWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BackgroundWidget, self).__init__(parent)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.grid_layout.setSpacing(5)

        self.type_lbl = QtWidgets.QLabel("Type:")
        self.type_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.type_cb = QtWidgets.QComboBox()
        self.type_cb.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.type_cb.view().setMinimumHeight(30)


        self.type_cb.addItem("pchip")
        self.type_cb.addItem("spline")
        self.define_btn = FlatButton('Define')
        self.define_btn.setCheckable(True)
        self.subtract_btn = FlatButton('Subtract')
        self.subtract_btn.setCheckable(True)

        type_layout = QtWidgets.QHBoxLayout()
        type_layout.addWidget(self.type_lbl)
        type_layout.addWidget(self.type_cb)
        self.grid_layout.addLayout(type_layout, 0, 0, 1, 2)

        self.grid_layout.addWidget(self.define_btn, 1, 0)
        self.grid_layout.addWidget(self.subtract_btn, 1, 1)

        self.set_cb_style()
        self.setLayout(self.grid_layout)

    def set_cb_style(self):
        cleanlooks = QtWidgets.QStyleFactory.create('plastique')
        self.type_cb.setStyle(cleanlooks)