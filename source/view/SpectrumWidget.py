# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore

import pyqtgraph as pg
import numpy as np

pg.setConfigOption('useOpenGL', False)
pg.setConfigOption('leftButtonPan', False)
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')
pg.setConfigOption('antialias', True)

plot_colors = {
    'data_pen': '#ffffff',
    'data_brush': '#FFF',
    'background_plot': 'r',
    'background_scatter_pen': 'r',
    'background_scatter_brush': 'w',
    'residual_pen': 'r',
    'residual_brush': '#DDD',
    'model': '#AA6633',
    'model-active':'#FFAA77',
    'model-sum':'#22FF77',
}


class SpectrumWidget(QtGui.QWidget):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    range_changed = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(SpectrumWidget, self).__init__(parent)

        self._layout = QtGui.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._create_spectrum()
        self._create_mouse_position_widget()

        self.setLayout(self._layout)

        self._create_plot_items()

        self._spectrum_plot.connect_mouse_move_event()
        self._residual_plot.connect_mouse_move_event()

        self._spectrum_plot.mouse_moved.connect(self.update_mouse_position_widget)
        self._residual_plot.mouse_moved.connect(self.update_mouse_position_widget)

        self._spectrum_plot.mouse_left_clicked.connect(self.mouse_left_clicked.emit)
        self._data_plot_item.sigClicked.connect(self.data_plot_item_clicked)

        self._spectrum_plot.mouse_moved.connect(self.mouse_moved.emit)

    def _create_spectrum(self):
        self._pg_layout_widget = pg.GraphicsLayoutWidget()
        self._pg_layout = pg.GraphicsLayout()
        self._pg_layout.setContentsMargins(0, 0, 0, 0)
        self._pg_layout_widget.setContentsMargins(0, 0, 0, 0)

        self._spectrum_plot = ModifiedPlotItem()
        self._residual_plot = ModifiedPlotItem()

        self._pg_layout.addItem(self._spectrum_plot, 0, 0)
        self._pg_layout.addItem(self._residual_plot, 1, 0)

        self._residual_plot.setXLink(self._spectrum_plot)
        self._residual_plot.hideAxis('bottom')

        self._pg_layout.layout.setRowStretchFactor(0, 10)
        self._pg_layout.layout.setRowStretchFactor(1, 2)

        self._pg_layout_widget.addItem(self._pg_layout)
        self._layout.addWidget(self._pg_layout_widget)

    def _create_mouse_position_widget(self):
        self._pos_layout = QtGui.QHBoxLayout()
        self.x_lbl = QtGui.QLabel('x:')
        self.y_lbl = QtGui.QLabel('y:')

        self.x_lbl.setMinimumWidth(60)
        self.y_lbl.setMinimumWidth(60)

        self._pos_layout.addSpacerItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                                        QtGui.QSizePolicy.Fixed))
        self._pos_layout.addWidget(self.x_lbl)
        self._pos_layout.addWidget(self.y_lbl)

        self._layout.addLayout(self._pos_layout)


    def data_plot_item_clicked(self):
        """
        this function is called when the data plot item is clicked and just emits the mouse_left_clicked signal
        x, y values to
        mouse_left_clicked. Otherwise the Data plot item blocks the signal...
        """
        x, y = self._spectrum_plot.get_mouse_position()
        self.mouse_left_clicked.emit(x,y)

    def update_mouse_position_widget(self, x, y):
        self.x_lbl.setText('x: {:02.4f}'.format(x))
        self.y_lbl.setText('y: {:02.4f}'.format(y))

    def _create_plot_items(self):
        self.current_selected_model = 0
        self._data_plot_item = pg.ScatterPlotItem(pen=pg.mkPen(plot_colors['data_pen'], width=1),
                                                  brush=pg.mkBrush(plot_colors['data_brush']),
                                                  size=5,
                                                  symbol ='x',
                                                  downsample=5,
                                                  clipToView=True)


        self._background_plot_item = pg.PlotDataItem(pen=pg.mkPen(plot_colors['background_plot'],
                                                                  width=1.5))

        self._background_scatter_item = pg.ScatterPlotItem(pen=pg.mkPen(plot_colors['background_scatter_pen'], width=1),
                                                          brush=pg.mkBrush(plot_colors['background_scatter_brush']),
                                                          size=8,
                                                          symbol='d')

        self._residual_plot_item = pg.ScatterPlotItem(pen=pg.mkPen(plot_colors['residual_pen'],
                                                                width=1),
                                                   brush=pg.mkBrush(plot_colors['residual_brush']),
                                                   size = 2,
                                                   symbol='o')

        self._model_sum_plot_item = pg.PlotDataItem(pen=pg.mkPen(plot_colors['model-sum'],
                                                                 width=2.5))

        self._model_plot_items = []

        self._spectrum_plot.addItem(self._data_plot_item)
        self._spectrum_plot.addItem(self._background_plot_item)
        self._spectrum_plot.addItem(self._model_sum_plot_item)
        self._spectrum_plot.addItem(self._background_scatter_item)
        self._residual_plot.addItem(self._residual_plot_item)

    def plot_data(self, x, y):
        self._data_plot_item.setData(x, y)
        self.set_limits(x, y)

    def set_limits(self, x, y, spacing=0.25):
        x_min = np.min(x)
        x_max = np.max(x)
        y_min = np.min(y)
        y_max = np.max(y)
        x_range = x_max - x_min
        x_space = spacing * x_range
        y_range = y_max - y_min
        y_space = spacing * y_range
        self._spectrum_plot.setLimits(xMin=x_min - x_space,
                                     xMax=x_max + x_space,
                                     yMin=y_min - y_space,
                                     yMax=y_max + y_space)


    def plot_data_spectrum(self, spectrum):
        x, y = spectrum.data
        self.plot_data(x, y)

    def get_plot_data(self):
        return self._data_plot_item.getData()

    def plot_background(self, x, y):
        self._background_plot_item.setData(x, y)

    def plot_background_spectrum(self, spectrum):
        x, y = spectrum.data
        self.plot_background(x, y)

    def plot_background_points(self, x, y):
        self._background_scatter_item.setData(x, y)

    def plot_background_points_spectrum(self, spectrum):
        x, y = spectrum.data
        self.plot_background_points(x, y)

    def get_background_plot_data(self):
        return self._background_plot_item.getData()

    def get_background_points_data(self):
        return self._background_scatter_item.getData()

    def plot_residual(self, x, y):
        self._residual_plot_item.setData(x, y)

    def plot_residual_spectrum(self, spectrum):
        x, y = spectrum.data
        self.plot_residual(x, y)

    def get_residual_plot_data(self):
        return self._residual_plot_item.getData()

    def plot_model_sum(self, x, y):
        self._model_sum_plot_item.setData(x,y)

    def plot_model_sum_spectrum(self, spectrum):
        x, y = spectrum.data
        self.plot_model_sum(x, y)

    def get_model_sum_plot_data(self):
        return self._model_sum_plot_item.getData()

    def add_model(self, spectrum=None):
        self._model_plot_items.append(pg.PlotDataItem(pen=pg.mkPen(plot_colors['model'], width=1.5)))
        # self.activate_model_spectrum(len(self.model_plot_items)-1)
        self._spectrum_plot.addItem(self._model_plot_items[-1])
        if spectrum is not None:
            self.update_model_spectrum(-1, spectrum)

    def update_model(self, ind, x, y):
        self._model_plot_items[ind].setData(x, y)

    def update_model_spectrum(self, ind, spectrum):
        x, y = spectrum.data
        self.update_model(ind, x, y)

    def activate_model_spectrum(self, ind):
        if len(self._model_plot_items):
            self._model_plot_items[self.current_selected_model].setPen(pg.mkPen(plot_colors['model'], width=1.5))
            self._model_plot_items[ind].setPen(pg.mkPen(plot_colors['model-active'], width=2))
            self.current_selected_model=ind

    def del_model(self, index=-1):
        self._spectrum_plot.removeItem(self._model_plot_items[index])
        del self._model_plot_items[index]

    def get_model_plot_data(self, index):
        return self._model_plot_items[index].getData()

    def get_number_of_model_plots(self):
        return len(self._model_plot_items)

    def get_mouse_position(self):
        return self._spectrum_plot.get_mouse_position()


    def set_spectrum_plot_keypress_callback(self, fcn_callback):
        self._spectrum_plot.keyPressEvent = fcn_callback

    def set_spectrum_plot_focus(self):
        self._spectrum_plot.setFocus()


    ### Function for testing the GUI:
    def _spectrum_plot_emit_mouse_click_event(self, x, y):
        self._spectrum_plot.mouse_left_clicked.emit(x, y)

    def _spectrum_plot_set_current_mouse_position(self, x, y):
        self._spectrum_plot.update_cur_mouse_position(x, y)

    def _spectrum_plot_send_keypress_event(self, evt):
        self._spectrum_plot.keyPressEvent(evt)


class ModifiedPlotItem(pg.PlotItem):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    range_changed = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(ModifiedPlotItem, self).__init__(*args, **kwargs)

        self.modify_mouse_behavior()

    def modify_mouse_behavior(self):
        self.vb.mouseClickEvent = self.mouse_click_event
        self.vb.mouseDragEvent = self.mouse_drag_event
        self.vb.mouseDoubleClickEvent = self.mouse_double_click_event
        self.vb.wheelEvent = self.wheel_event
        self.range_changed_timer = QtCore.QTimer()
        self.range_changed_timer.timeout.connect(self.emit_sig_range_changed)
        self.range_changed_timer.setInterval(30)

        self.cur_mouse_position_x = 0
        self.cur_mouse_position_y = 0

        self.mouse_moved.connect(self.update_cur_mouse_position)
        self.last_view_range = np.array(self.vb.viewRange())

    def connect_mouse_move_event(self):
        self.scene().sigMouseMoved.connect(self.mouse_move_event)

    def mouse_move_event(self, pos):
        if self.sceneBoundingRect().contains(pos):
            pos = self.vb.mapSceneToView(pos)
            self.mouse_moved.emit(pos.x(), pos.y())

    def mouse_click_event(self, ev):
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

    def update_cur_mouse_position(self, x, y):
        self.cur_mouse_position_x = x
        self.cur_mouse_position_y = y

    def get_mouse_position(self):
        return self.cur_mouse_position_x, self.cur_mouse_position_y

    def mouse_double_click_event(self, ev):
        if (ev.button() == QtCore.Qt.RightButton) or (ev.button() == QtCore.Qt.LeftButton and
                                                              ev.modifiers() & QtCore.Qt.ControlModifier):
            self.vb.autoRange()
            self.vb.enableAutoRange()
            self._auto_range = True
            self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])

    def mouse_drag_event(self, ev, axis=None):
        # most of this code is copied behavior mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        last_pos = ev.lastPos()
        dif = pos - last_pos
        dif *= -1

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and ev.modifiers() & QtCore.Qt.ControlModifier):
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

    def wheel_event(self, ev, axis=None, *args):
        pg.ViewBox.wheelEvent(self.vb, ev, axis)
        self.vb.sigRangeChangedManually.emit(self.vb.state['mouseEnabled'])
