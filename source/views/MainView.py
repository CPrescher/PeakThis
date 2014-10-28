# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import sys

from PyQt4 import QtCore, QtGui


class MainView(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.horizontal_layout = QtGui.QHBoxLayout(self)

        self.spectrum_frame = QtGui.QFrame()
        self.control_frame = ControlWidget()

        self.horizontal_layout.addWidget(self.spectrum_frame)
        self.horizontal_layout.addWidget(self.control_frame)

        self.setLayout(self.horizontal_layout)

        self.setWindowTitle("Testing the universe")

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


        self.main_vertical_layout.addWidget(self.file_widget)
        self.main_vertical_layout.addWidget(HorizontalLine())
        self.main_vertical_layout.addWidget(self.background_widget)

        self.setLayout(self.main_vertical_layout)

class FileWidget(QtGui.QWidget):
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
        self.define_btn = QtGui.QPushButton('Define')
        self.subtract_btn = QtGui.QPushButton('Subtract')

        type_layout = QtGui.QHBoxLayout()
        type_layout.addWidget(self.type_lbl)
        type_layout.addWidget(self.type_cb)
        self.grid_layout.addLayout(type_layout, 0, 0, 1, 2)

        self.grid_layout.addWidget(self.define_btn, 1, 0)
        self.grid_layout.addWidget(self.subtract_btn, 1, 1)

        self.setLayout(self.grid_layout)

class HorizontalLine(QtGui.QFrame):
    def __init__(self, parent=None):
        super(HorizontalLine, self).__init__(parent)
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_view = MainView()
    main_view.show()
    app.exec_()