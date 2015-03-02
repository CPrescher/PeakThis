# -*- coding: utf8 -*-

__author__ = 'Clemens Prescher'
__version__ = 0.1

import sys
import os
from PyQt4 import QtCore, QtGui

from .SpectrumWidget import SpectrumWidget
from .ModelWidget import ModelWidget
from .GuiElements import FlatButton


class MainWidget(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.main_splitter = QtGui.QSplitter()

        self.spectrum_widget = SpectrumWidget(self)
        self.control_widget = ControlWidget(self)

        self.main_splitter.addWidget(self.spectrum_widget)
        self.main_splitter.addWidget(self.control_widget)

        self.load_stylesheet()

        self.setCentralWidget(self.main_splitter)
        self.main_splitter.setStretchFactor(0,1)
        self.main_splitter.setStretchFactor(1,0)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, False)

        self.setWindowTitle("PeakThis v{}".format(__version__))
        self.set_shortcuts()

    def set_shortcuts(self):
        self.load_file_btn = self.control_widget.file_widget.load_file_btn

        self.background_define_btn = self.control_widget.background_widget.define_btn
        self.background_method_cb = self.control_widget.background_widget.type_cb
        self.background_subtract_btn = self.control_widget.background_widget.subtract_btn

        self.model_add_btn = self.control_widget.model_widget.add_btn
        self.model_delete_btn = self.control_widget.model_widget.delete_btn
        self.model_define_btn = self.control_widget.model_widget.define_btn
        self.model_copy_btn = self.control_widget.model_widget.copy_btn
        self.model_selector_dialog = self.control_widget.model_widget.model_selector_dialog
        self.model_list = self.control_widget.model_widget.model_list
        self.model_parameter_table = self.control_widget.model_widget.parameter_table

        self.fit_btn = self.control_widget.fit_widget.fit_btn

    def load_stylesheet(self):
        stylesheet_file = open(os.path.join(module_path(), "DioptasStyle.qss"), 'r')
        stylesheet_str = stylesheet_file.read()
        self.setStyleSheet(stylesheet_str)


    def show(self):
        QtGui.QWidget.show(self)
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()


class ControlWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)
        self.main_vertical_layout = QtGui.QVBoxLayout()
        self.main_vertical_layout.setContentsMargins(0,5,5,5)
        self.main_vertical_layout.setSpacing(5)

        self.file_widget = FileWidget(self)
        self.background_widget = BackgroundWidget(self)
        self.model_widget = ModelWidget(self)
        self.fit_widget = FitWidget(self)

        self.main_vertical_layout.addWidget(self.file_widget)
        self.main_vertical_layout.addWidget(self.background_widget)
        self.main_vertical_layout.addWidget(self.model_widget)
        self.main_vertical_layout.addWidget(self.fit_widget)

        self.main_vertical_layout.addSpacerItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                                                  QtGui.QSizePolicy.Expanding))

        self.setLayout(self.main_vertical_layout)

    def disable(self, except_widgets=None):
        for child1 in self.children():
            for child2 in child1.children():
                child2.setEnabled(False)

        for widget in except_widgets:
            widget.setEnabled(True)

    def enable(self):
        for child1 in self.children():
            for child2 in child1.children():
                child2.setEnabled(True)


class FileWidget(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)

        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.setContentsMargins(5,5,5,5)
        self.grid_layout.setSpacing(5)

        self.load_file_btn = FlatButton("Load Data")
        self.save_file_btn = FlatButton("Save Data")

        self.load_models_btn = FlatButton("Load Models")
        self.save_models_btn = FlatButton("Save Models")

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
        self.grid_layout.setContentsMargins(5,10,5,5)
        self.grid_layout.setSpacing(5)

        self.type_lbl = QtGui.QLabel("Type:")
        self.type_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.type_cb = QtGui.QComboBox()
        self.type_cb.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.type_cb.view().setMinimumHeight(30)


        self.type_cb.addItem("pchip")
        self.type_cb.addItem("spline")
        self.define_btn = FlatButton('Define')
        self.define_btn.setCheckable(True)
        self.subtract_btn = FlatButton('Subtract')
        self.subtract_btn.setCheckable(True)

        type_layout = QtGui.QHBoxLayout()
        type_layout.addWidget(self.type_lbl)
        type_layout.addWidget(self.type_cb)
        self.grid_layout.addLayout(type_layout, 0, 0, 1, 2)

        self.grid_layout.addWidget(self.define_btn, 1, 0)
        self.grid_layout.addWidget(self.subtract_btn, 1, 1)

        self.set_cb_style()
        self.setLayout(self.grid_layout)

    def set_cb_style(self):
        cleanlooks = QtGui.QStyleFactory.create('plastique')
        self.type_cb.setStyle(cleanlooks)


class FitWidget(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(FitWidget, self).__init__(parent)
        self.setTitle('Fit')
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(5,5,5,5)
        self.main_layout.setSpacing(5)

        self.fit_btn = FlatButton('Fit')
        self.main_layout.addWidget(self.fit_btn)

        self.setLayout(self.main_layout)



def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_view = MainWidget()
    main_view.show()
    app.exec_()