# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore

import pyqtgraph as pg
import numpy as np

pg.setConfigOption('useOpenGL', False)
pg.setConfigOption('leftButtonPan', False)
pg.setConfigOption('background', '#EEE')
pg.setConfigOption('foreground', 'k')
pg.setConfigOption('antialias', True)

class SpectrumWidget(QtGui.QWidget):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    range_changed = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(SpectrumWidget, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.create_graphs()
        self.create_position_widget()

        self.setLayout(self.layout)

        self.spectrum_plot.connect_mouse_move_event()
        self.residual_plot.connect_mouse_move_event()

        self.spectrum_plot.mouse_moved.connect(self.update_position_widget)
        self.residual_plot.mouse_moved.connect(self.update_position_widget)

    def create_graphs(self):
        self.pg_layout_widget = pg.GraphicsLayoutWidget()
        self.pg_layout = pg.GraphicsLayout()
        self.pg_layout.setContentsMargins(0,0,0,0)
        self.pg_layout_widget.setContentsMargins(0,0,0,0)

        self.spectrum_plot = AdvancedPlotItem()
        self.residual_plot = AdvancedPlotItem()

        self.pg_layout.addItem(self.spectrum_plot, 0, 0)
        self.pg_layout.addItem(self.residual_plot, 1, 0)

        self.residual_plot.setXLink(self.spectrum_plot)
        self.residual_plot.hideAxis('bottom')

        self.pg_layout.layout.setRowStretchFactor(0, 100)
        self.pg_layout.layout.setRowStretchFactor(1, 0)

        self.pg_layout_widget.addItem(self.pg_layout)
        self.layout.addWidget(self.pg_layout_widget)

    def create_position_widget(self):
        self.pos_layout = QtGui.QHBoxLayout()
        self.x_lbl = QtGui.QLabel('x:')
        self.y_lbl = QtGui.QLabel('y:')

        self.x_lbl.setMinimumWidth(60)
        self.y_lbl.setMinimumWidth(60)

        self.pos_layout.addSpacerItem(QtGui.QSpacerItem(20,20, QtGui.QSizePolicy.Expanding,
                                                                  QtGui.QSizePolicy.Fixed))
        self.pos_layout.addWidget(self.x_lbl)
        self.pos_layout.addWidget(self.y_lbl)

        self.layout.addLayout(self.pos_layout)

    def update_position_widget(self, x, y):
        self.x_lbl.setText('x: {:02.4f}'.format(x))
        self.y_lbl.setText('y: {:02.4f}'.format(y))


class AdvancedPlotItem(pg.PlotItem):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    range_changed = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(AdvancedPlotItem, self).__init__(*args, **kwargs)

        self.modify_mouse_behavior()

    def modify_mouse_behavior(self):
        self.vb.mouseClickEvent = self.myMouseClickEvent
        self.vb.mouseDragEvent = self.myMouseDragEvent
        self.vb.mouseDoubleClickEvent = self.myMouseDoubleClickEvent
        # self.vb.wheelEvent = self.myWheelEvent
        self.range_changed_timer = QtCore.QTimer()
        self.range_changed_timer.timeout.connect(self.emit_sig_range_changed)
        self.range_changed_timer.setInterval(30)
        self.last_view_range = np.array(self.vb.viewRange())

    def connect_mouse_move_event(self):
        self.scene().sigMouseMoved.connect(self.myMouseMoveEvent)

    def myMouseMoveEvent(self, pos):
        if self.sceneBoundingRect().contains(pos):
            pos = self.vb.mapSceneToView(pos)
            self.mouse_moved.emit(pos.x(), pos.y())

    def myMouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                 ev.modifiers() & QtCore.Qt.ControlModifier):
            self.vb.scaleBy(2)
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
        elif ev.button() == QtCore.Qt.LeftButton:
            if self.sceneBoundingRect().contains(ev.pos()):
                pos = self.vb.mapToView(ev.pos())
                x = pos.x()
                y = pos.y()
                self.mouse_left_clicked.emit(x, y)


    def myMouseDoubleClickEvent(self, ev):
        if (ev.button() == QtCore.Qt.RightButton) or (ev.button() == QtCore.Qt.LeftButton and
                                                      ev.modifiers() & QtCore.Qt.ControlModifier):
            self.vb.autoRange()
            self.vb.enableAutoRange()
            self._auto_range = True
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])

    def myMouseDragEvent(self, ev, axis=None):
        # most of this code is copied behavior mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif *= -1

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                 ev.modifiers() & QtCore.Qt.ControlModifier):
            # determine the amount of translation
            tr = dif
            tr = self.vb.mapToView(tr) - self.vb.mapToView(pg.Point(0, 0))
            x = tr.x()
            y = tr.y()
            self.vb.translateBy(x=x, y=y)
            if ev.start:
                self.range_changed_timer.start()
            if ev.isFinish():
                self.range_changed_timer.stop()
                self.emit_sig_range_changed()
        else:
            if ev.isFinish():  # This is the final move in the drag; change the view scale now
                self._auto_range = False
                self.vb.enableAutoRange(enable=False)
                self.vb.rbScaleBox.hide()
                ax = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                ax = self.vb.childGroup.mapRectFromParent(ax)
                self.vb.showAxRect(ax)
                self.vb.axHistoryPointer += 1
                self.vb.axHistory = self.vb.axHistory[:self.vb.axHistoryPointer] + [ax]
                self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
            else:
                # update shape of scale box
                self.vb.updateScaleBox(ev.buttonDownPos(), ev.pos())

    def emit_sig_range_changed(self):
        new_view_range = np.array(self.vb.viewRange())
        if not np.array_equal(self.last_view_range, new_view_range):
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
            self.last_view_range = new_view_range

    def myWheelEvent(self, ev, axis=None, *args):
        pg.ViewBox.wheelEvent(self.vb, ev, axis)
        self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
