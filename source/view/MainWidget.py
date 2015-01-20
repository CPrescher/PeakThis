# -*- coding: utf8 -*-

__author__ = 'Clemens Prescher'
__version__ = 0.1

import sys
from PyQt4 import QtCore, QtGui

from SpectrumWidget import SpectrumWidget
from view.ModelWidget import ModelWidget


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.horizontal_layout = QtGui.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.spectrum_widget = SpectrumWidget()
        self.control_widget = ControlWidget()

        self.horizontal_layout.addWidget(self.spectrum_widget)
        self.horizontal_layout.addWidget(self.control_widget)

        self.setLayout(self.horizontal_layout)

        self.setWindowTitle("PeakThis v{}".format(__version__))
        self.set_shortcuts()

    def set_shortcuts(self):
        self.load_file_btn = self.control_widget.file_widget.load_file_btn

        self.background_define_btn = self.control_widget.background_widget.define_btn
        self.background_method_cb = self.control_widget.background_widget.type_cb

        self.model_add_btn = self.control_widget.model_widget.add_btn
        self.model_delete_btn = self.control_widget.model_widget.delete_btn
        self.model_define_btn = self.control_widget.model_widget.define_btn
        self.model_copy_btn = self.control_widget.model_widget.copy_btn
        self.model_selector_dialog = self.control_widget.model_widget.model_selector_dialog
        self.model_list = self.control_widget.model_widget.model_list
        self.model_parameter_table = self.control_widget.model_widget.parameter_table

    def show(self):
        QtGui.QWidget.show(self)
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()


class ControlWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)
        self.main_vertical_layout = QtGui.QVBoxLayout()

        self.file_widget = FileWidget()
        self.background_widget = BackgroundWidget()
        self.model_widget = ModelWidget()

        self.main_vertical_layout.addWidget(self.file_widget)
        self.main_vertical_layout.addWidget(self.background_widget)
        self.main_vertical_layout.addWidget(self.model_widget)

        self.main_vertical_layout.addSpacerItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                                                  QtGui.QSizePolicy.Expanding))

        self.setLayout(self.main_vertical_layout)

    def disable(self, except_widget=None):
        for child1 in self.children():
            for child2 in child1.children():
                child2.setEnabled(False)
        except_widget.setEnabled(True)

    def enable(self):
        for child1 in self.children():
            for child2 in child1.children():
                child2.setEnabled(True)


class FileWidget(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)

        self.grid_layout = QtGui.QGridLayout()

        self.load_file_btn = QtGui.QPushButton("Load Data")
        self.save_file_btn = QtGui.QPushButton("Save Data")

        self.load_models_btn = QtGui.QPushButton("Load Models")
        self.save_models_btn = QtGui.QPushButton("Save Models")

        self.grid_layout.addWidget(self.load_file_btn, 0, 0)
        self.grid_layout.addWidget(self.save_file_btn, 0, 1)
        self.grid_layout.addWidget(self.load_models_btn, 2, 0)
        self.grid_layout.addWidget(self.save_models_btn, 2, 1)

        self.setLayout(self.grid_layout)


class BackgroundWidget(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(BackgroundWidget, self).__init__(parent)
        self.setTitle('Background')

        self.grid_layout = QtGui.QGridLayout()

        self.type_lbl = QtGui.QLabel("Type:")
        self.type_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.type_cb = QtGui.QComboBox()
        self.type_cb.addItem("pchip")
        self.type_cb.addItem("spline")
        self.define_btn = QtGui.QPushButton('Define')
        self.subtract_btn = QtGui.QPushButton('Subtract')

        type_layout = QtGui.QHBoxLayout()
        type_layout.addWidget(self.type_lbl)
        type_layout.addWidget(self.type_cb)
        self.grid_layout.addLayout(type_layout, 0, 0, 1, 2)

        self.grid_layout.addWidget(self.define_btn, 1, 0)
        self.grid_layout.addWidget(self.subtract_btn, 1, 1)

        self.setLayout(self.grid_layout)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_view = MainWidget()
    main_view.show()
    app.exec_()