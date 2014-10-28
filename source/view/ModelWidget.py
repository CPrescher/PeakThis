# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore


class ModelWidget(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(ModelWidget, self).__init__("Models", parent)

        self.grid_layout = QtGui.QGridLayout()

        self.add_btn = QtGui.QPushButton("Add")
        self.delete_btn = QtGui.QPushButton("Delete")

        self.model_list = QtGui.QListView()

        self.parameter_table = QtGui.QTableWidget()

        self.grid_layout.addWidget(self.add_btn, 0, 0)
        self.grid_layout.addWidget(self.delete_btn, 0, 1)
        self.grid_layout.addWidget(self.model_list, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.parameter_table, 2, 0, 1, 2)

        self.setLayout(self.grid_layout)

        self.model_selector_dialog = ModelSelectorDialog(self)

    def show_model_selector_dialog(self):
        self.model_selector_dialog.show()


class ModelSelectorDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ModelSelectorDialog, self).__init__(parent)

        self.setWindowTitle("Please select a Model:")

        self._vertical_layout = QtGui.QVBoxLayout()
        self.model_list = QtGui.QListWidget()

        self._ok_cancel_layout = QtGui.QHBoxLayout()
        self.ok_btn = QtGui.QPushButton("OK")
        self.cancel_btn = QtGui.QPushButton("Cancel")

        self._ok_cancel_layout.addSpacerItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                                               QtGui.QSizePolicy.Fixed))
        self._ok_cancel_layout.addWidget(self.ok_btn)
        self._ok_cancel_layout.addWidget(self.cancel_btn)

        self._vertical_layout.addWidget(self.model_list)
        self._vertical_layout.addLayout(self._ok_cancel_layout)

        self.setLayout(self._vertical_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def show(self):
        QtGui.QWidget.show(self)
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()

