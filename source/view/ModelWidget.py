# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore


class ModelWidget(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(ModelWidget, self).__init__("Models", parent)

        self.grid_layout = QtGui.QGridLayout()

        self.add_btn = QtGui.QPushButton("Add")
        self.delete_btn = QtGui.QPushButton("Delete")

        self.model_list = QtGui.QListWidget()

        self.parameter_table = QtGui.QTableWidget()
        self.parameter_table.verticalHeader().setVisible(False)
        self.parameter_table.setColumnCount(5)

        self.grid_layout.addWidget(self.add_btn, 0, 0)
        self.grid_layout.addWidget(self.delete_btn, 0, 1)
        self.grid_layout.addWidget(self.model_list, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.parameter_table, 2, 0, 1, 2)

        self.setLayout(self.grid_layout)

        self.model_selector_dialog = ModelSelectorDialog(self)

    def show_model_selector_dialog(self):
        self.model_selector_dialog.show()

    def update_parameters(self, parameters):
        self.parameter_table.clear()
        self.parameter_table.setRowCount(len(parameters))

        ind = 0
        for name in parameters:
            self.parameter_table.setItem(ind, 0, QtGui.QTableWidgetItem(name))
            self.parameter_table.setItem(ind, 1, QtGui.QTableWidgetItem(str(parameters[name].value)))
            self.parameter_table.setItem(ind, 2, QtGui.QTableWidgetItem(str(parameters[name].vary)))
            self.parameter_table.setItem(ind, 3, QtGui.QTableWidgetItem(str(parameters[name].min)))
            self.parameter_table.setItem(ind, 4, QtGui.QTableWidgetItem(str(parameters[name].max)))

            ind += 1

        self.parameter_table.resizeColumnsToContents()


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

    def populate_models(self, model_dict):
        self.model_list.clear()
        for model_key in model_dict:
            self.model_list.addItem(model_key)

    def get_selected_index(self):
        return self.model_list.currentRow()

    def get_selected_item_string(self):
        return str(self.model_list.currentItem().text())

    def show(self):
        QtGui.QWidget.show(self)
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()

