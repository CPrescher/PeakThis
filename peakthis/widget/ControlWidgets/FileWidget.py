# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from ..qt import QtWidgets
from ..CustomWidgets.GuiElements import FlatButton

class FileWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.grid_layout.setSpacing(5)

        self.load_file_btn = FlatButton("Load Data")
        self.save_data_btn = FlatButton("Save Data")

        self.load_models_btn = FlatButton("Load Models")
        self.save_models_btn = FlatButton("Save Models")

        self.grid_layout.addWidget(self.load_file_btn, 0, 0)
        self.grid_layout.addWidget(self.save_data_btn, 0, 1)
        self.grid_layout.addWidget(self.load_models_btn, 2, 0)
        self.grid_layout.addWidget(self.save_models_btn, 2, 1)

        self.setLayout(self.grid_layout)
