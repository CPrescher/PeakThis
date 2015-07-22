# -*- coding: utf8 -*-

__author__ = 'Clemens Prescher'
__version__ = 0.1

import sys
import os
from PyQt4 import QtCore, QtGui

from .CustomWidgets import SpectrumWidget
from .ControlWidgets import FileWidget, FitWidget, BackgroundWidget, ModelWidget

from .CustomWidgets import ExpandableBox

class MainWidget(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.main_splitter = QtGui.QSplitter()

        self.spectrum_widget = SpectrumWidget(self)
        self.control_widget = ControlWidget(self)
        self.control_widget.setMinimumWidth(250)

        self.main_splitter.addWidget(self.spectrum_widget)
        self.main_splitter.addWidget(self.control_widget)

        self.load_stylesheet()

        self.setCentralWidget(self.main_splitter)
        self.main_splitter.setStretchFactor(0,100)
        self.main_splitter.setStretchFactor(1,0)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, False)

        self.setWindowTitle("PeakThis v{}".format(__version__))
        self.set_shortcuts()

    def set_shortcuts(self):
        self.load_file_btn = self.control_widget.file_widget.load_file_btn
        self.save_data_btn = self.control_widget.file_widget.save_data_btn

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

        self.main_vertical_layout.addWidget(ExpandableBox(self.file_widget, "Data"))
        self.main_vertical_layout.addWidget(ExpandableBox(self.background_widget, "Background"))
        self.main_vertical_layout.addWidget(ExpandableBox(self.model_widget, "Model"))
        self.main_vertical_layout.addWidget(ExpandableBox(self.fit_widget, "Fit"))

        self.main_vertical_layout.addSpacerItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                                                  QtGui.QSizePolicy.Expanding))

        self.setLayout(self.main_vertical_layout)

    def disable(self, except_widgets=None):
        for control_box in self.children():
            try:
                control_box.enable_widgets(False)
            except AttributeError:
                pass

        for widget in except_widgets:
            widget.setEnabled(True)

    def enable(self):
        for control_box in self.children():
            try:
                control_box.enable_widgets(True)
            except AttributeError:
                pass




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