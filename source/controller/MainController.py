# -*- coding: utf8 -*-

import numpy as np
from PyQt4 import QtCore, QtGui

from view.MainWidget import MainWidget
from model.DataModel import DataModel
from model.PickModels import models_dict


__author__ = 'Clemens Prescher'


class MainController(object):
    def __init__(self):
        self.main_widget = MainWidget()
        self.data = DataModel()
        self.plot_some_data()
        self.create_subscriptions()

    def show_view(self):
        self.main_widget.show()

    def plot_some_data(self):
        x = np.linspace(0, 30, 1000)
        y = np.sin(x)+1
        self.data.spectrum._x = x
        self.data.spectrum._y = y
        self.main_widget.spectrum_widget.plot_data(x, y)

    def create_subscriptions(self):
        self.connect_click_function(self.main_widget.load_file_btn, self.load_data)

        self.data.spectrum_changed.connect(self.main_widget.spectrum_widget.plot_data_spectrum)
        self.data.background_changed.connect(self.main_widget.spectrum_widget.plot_background_spectrum)
        self.data.background_points_changed.connect(self.main_widget.spectrum_widget.plot_background_points_spectrum)

        self.data.model_added.connect(self.update_displayed_models)
        self.main_widget.control_widget.model_widget.model_selected_changed.connect(
            self.update_displayed_model_parameters
        )
        self.main_widget.control_widget.model_widget.model_parameters_changed.connect(
            self.data.update_model
        )
        self.data.model_parameters_changed.connect(
            self.main_widget.spectrum_widget.update_model_spectrum
        )
        self.data.model_parameters_changed.connect(
            self.update_displayed_model_parameters
        )
        self.data.model_sum_changed.connect(self.main_widget.spectrum_widget.plot_model_sum_spectrum)

        self.connect_click_function(self.main_widget.model_define_btn, self.start_model_picking)


        self.connect_click_function(self.main_widget.background_define_btn, self.start_background_picking)
        self.main_widget.background_method_cb.currentIndexChanged.connect(self.background_model_changed)

        self.main_widget.control_widget.model_widget.add_btn.clicked.connect(self.add_model_btn_clicked)
        self.main_widget.control_widget.model_widget.model_selector_dialog.accepted.connect(
            self.add_model_dialog_accepted
        )

    def connect_click_function(self, emitter, function):
        self.main_widget.connect(emitter, QtCore.SIGNAL('clicked()'), function)

    def disconnect_click_function(self, emitter, function):
        self.main_widget.disconnect(emitter, QtCore.SIGNAL('clicked()'), function)

    def start_background_picking(self):
        self.disconnect_click_function(self.main_widget.background_define_btn, self.start_background_picking)
        self.connect_click_function(self.main_widget.background_define_btn, self.end_background_picking)
        self.main_widget.background_define_btn.setText('Finish')

        self.main_widget.spectrum_widget.spectrum_plot.keyPressEvent = self.spectrum_key_press_event_background_picking
        self.main_widget.spectrum_widget.spectrum_plot.setFocus()

        self.main_widget.spectrum_widget.mouse_left_clicked.connect(self.data.background_model.add_point)

    def end_background_picking(self):
        self.connect_click_function(self.main_widget.background_define_btn, self.start_background_picking)
        self.disconnect_click_function(self.main_widget.background_define_btn, self.end_background_picking)
        self.main_widget.background_define_btn.setText('Define')

        self.main_widget.spectrum_widget.spectrum_plot.keyPressEvent = self.spectrum_key_press_event_empty
        self.main_widget.spectrum_widget.mouse_left_clicked.disconnect(self.data.background_model.add_point)

    def background_model_changed(self):
        self.data.background_model.set_method(str(self.main_widget.background_method_cb.currentText()))


    def spectrum_key_press_event_background_picking(self, QKeyEvent):
        if QKeyEvent.text() == 'x':
            mouse_x, mouse_y = self.main_widget.spectrum_widget.get_mouse_position()
            self.data.background_model.delete_point_close_to(mouse_x, mouse_y)

    def spectrum_key_press_event_empty(self, QKeyEvent):
        pass

    def add_model_btn_clicked(self, *args, **kwargs):
        self.main_widget.model_selector_dialog.populate_models(models_dict)
        self.main_widget.control_widget.model_widget.show_model_selector_dialog()

    def add_model_dialog_accepted(self):
        selected_name = self.main_widget.model_selector_dialog.get_selected_item_string()
        self.data.add_model(models_dict[selected_name]())
        self.main_widget.spectrum_widget.add_model(self.data.get_model_spectrum(-1))
        self.main_widget.control_widget.model_widget.model_list.setCurrentRow(len(self.data.models)-1)

    def update_displayed_models(self):
        self.main_widget.control_widget.model_widget.model_list.clear()
        for model in self.data.models:
            self.main_widget.control_widget.model_widget.model_list.addItem(model.name)

    def update_displayed_model_parameters(self, index):
        self.main_widget.control_widget.model_widget.update_parameters(self.data.models[index].parameters)

    def start_model_picking(self):
        self.disconnect_click_function(self.main_widget.model_define_btn, self.start_model_picking)
        self.connect_click_function(self.main_widget.model_define_btn, self.end_model_picking)
        self.main_widget.model_define_btn.setText("Finish")

        self.main_widget.spectrum_widget.mouse_moved.connect(self.update_model_parameters)
        self.main_widget.spectrum_widget.mouse_left_clicked.connect(self.pick_model_parameter)

    def update_model_parameters(self, x, y):
        cur_model_ind = int(self.main_widget.model_list.currentRow())
        self.data.update_model_parameter(cur_model_ind, x, y)

    def pick_model_parameter(self, x, y):
        cur_model_ind = int(self.main_widget.model_list.currentRow())
        more_parameters_available = self.data.pick_model_parameters(cur_model_ind, x, y)
        if not more_parameters_available:
            self.end_model_picking()

    def end_model_picking(self):
        self.connect_click_function(self.main_widget.model_define_btn, self.start_model_picking)
        self.disconnect_click_function(self.main_widget.model_define_btn, self.end_model_picking)
        self.main_widget.model_define_btn.setText("Define")
        self.main_widget.spectrum_widget.mouse_moved.disconnect(self.update_model_parameters)
        self.main_widget.spectrum_widget.mouse_left_clicked.disconnect(self.pick_model_parameter)

    def load_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_widget, "Load Data File",
                                                             ''))
        if filename is not '':
            self.data.load_data(filename)
