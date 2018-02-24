# -*- coding: utf8 -*-

import copy
import os

import numpy as np
from ..widget.qt import QtGui, QtWidgets

from ..widget.MainWidget import MainWidget
from ..model.DataModel import DataModel
from ..model.PickModels import models_dict

__author__ = 'Clemens Prescher'


class MainController(object):
    def __init__(self):
        self.main_widget = MainWidget()
        self.data = DataModel()
        self.plot_some_data()
        self.create_subscriptions()

        self.save_data_path = ''

    def show_view(self):
        self.main_widget.show()

    def plot_some_data(self):
        x = np.linspace(0, 30, 1000)
        y = np.sin(x) + 1
        self.data.spectrum._x = x
        self.data.spectrum._y = y
        self.main_widget.spectrum_widget.plot_data(x, y)

    def create_subscriptions(self):
        ######################################
        # File Signals
        self.main_widget.load_file_btn.clicked.connect(self.load_data)
        self.main_widget.save_data_btn.clicked.connect(self.save_data)

        ######################################
        # Data signals
        self.data.spectrum_changed.connect(self.plot_data_spectrum)
        self.data.background_changed.connect(self.main_widget.spectrum_widget.plot_background_spectrum)
        self.data.background_points_changed.connect(self.main_widget.spectrum_widget.plot_background_points_spectrum)

        self.data.model_added.connect(self.update_displayed_models)

        #####################################
        # Gui Model signals

        # Adding models
        self.main_widget.model_add_btn.clicked.connect(self.add_model_btn_clicked)
        self.main_widget.control_widget.model_widget.model_selector_dialog.accepted.connect(
            self.add_model_dialog_accepted
        )
        self.main_widget.model_copy_btn.clicked.connect(self.copy_model_btn_clicked)

        # updating models in Gui and spectrum
        self.main_widget.control_widget.model_widget.model_selected_changed.connect(
            self.update_displayed_model_parameters
        )
        self.main_widget.control_widget.model_widget.model_selected_changed.connect(
            self.main_widget.spectrum_widget.activate_model_spectrum
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
        self.main_widget.model_define_btn.clicked.connect(self.start_model_picking)

        # deleting models
        self.main_widget.model_delete_btn.clicked.connect(self.del_model_btn_clicked)


        # Fitting signals
        self.main_widget.fit_btn.clicked.connect(self.data.fit_data)
        self.data.residual_changed.connect(self.main_widget.spectrum_widget.plot_residual_spectrum)

        # ROI Signals
        self.main_widget.spectrum_widget.linear_region_item.sigRegionChanged.connect(self.roi_item_changed)

        ##############################################
        # Background widget controls
        self.main_widget.background_define_btn.clicked.connect(self.start_background_picking)
        self.main_widget.background_method_cb.currentIndexChanged.connect(self.background_model_changed)
        self.main_widget.background_subtract_btn.toggled.connect(self.data.set_background_subtracted)

        self.main_widget.closeEvent = self.close_event

    def plot_data_spectrum(self):
        self.main_widget.spectrum_widget.plot_data(*self.data.get_whole_spectrum().data)
        self.main_widget.spectrum_widget.plot_roi_data(*self.data.get_spectrum().data)

    def start_background_picking(self):
        self.main_widget.background_define_btn.clicked.disconnect(self.start_background_picking)
        self.main_widget.background_define_btn.clicked.connect(self.end_background_picking)

        self.main_widget.background_define_btn.setText('Finish')
        self.main_widget.control_widget.disable(except_widgets=[self.main_widget.background_define_btn,
                                                                self.main_widget.background_subtract_btn,
                                                                self.main_widget.background_method_cb])

        self.main_widget.spectrum_widget.set_spectrum_plot_keypress_callback(
            self.spectrum_key_press_event_background_picking)
        self.main_widget.spectrum_widget.set_spectrum_plot_focus()

        self.main_widget.spectrum_widget.mouse_left_clicked.connect(self.data.add_background_model_point)

    def end_background_picking(self):
        self.main_widget.background_define_btn.clicked.connect(self.start_background_picking)
        self.main_widget.background_define_btn.clicked.disconnect(self.end_background_picking)

        self.main_widget.background_define_btn.setText('Define')
        self.main_widget.control_widget.enable()

        self.main_widget.spectrum_widget.set_spectrum_plot_keypress_callback(
            self.spectrum_key_press_event_empty)

        self.main_widget.spectrum_widget.mouse_left_clicked.disconnect(self.data.add_background_model_point)

    def background_model_changed(self):
        self.data.background_model.set_method(str(self.main_widget.background_method_cb.currentText()))


    def spectrum_key_press_event_background_picking(self, QKeyEvent):
        if QKeyEvent.text() == 'x':
            mouse_x, mouse_y = self.main_widget.spectrum_widget.get_mouse_position()
            self.data.remove_background_model_point_close_to(mouse_x, mouse_y)

    def spectrum_key_press_event_empty(self, QKeyEvent):
        pass

    def add_model_btn_clicked(self):
        self.main_widget.model_selector_dialog.populate_models(models_dict)
        self.main_widget.control_widget.model_widget.show_model_selector_dialog()


    def del_model_btn_clicked(self):
        cur_ind = self.main_widget.model_list.currentRow()
        if cur_ind != -1:
            self.main_widget.model_list.takeItem(cur_ind)
            self.main_widget.spectrum_widget.del_model(cur_ind)
            self.data.del_model(cur_ind)

    def add_model_dialog_accepted(self):
        selected_name = self.main_widget.model_selector_dialog.get_selected_item_string()
        self.data.add_model(models_dict[selected_name]())
        self.main_widget.spectrum_widget.add_model(self.data.get_model_spectrum(-1))
        self.main_widget.control_widget.model_widget.model_list.setCurrentRow(len(self.data.models) - 1)

    def copy_model_btn_clicked(self):
        cur_ind = self.main_widget.model_list.currentRow()
        if cur_ind != -1:
            self.data.add_model(copy.deepcopy(self.data.models[cur_ind]))
            self.main_widget.spectrum_widget.add_model(self.data.get_model_spectrum(-1))
            self.main_widget.control_widget.model_widget.model_list.setCurrentRow(len(self.data.models) - 1)

    def update_displayed_models(self):
        self.main_widget.model_list.blockSignals(True)
        self.main_widget.control_widget.model_widget.model_list.clear()
        for model in self.data.models:
            self.main_widget.control_widget.model_widget.model_list.addItem(model.name)
        self.main_widget.model_list.blockSignals(False)

    def update_displayed_model_parameters(self, index):
        self.main_widget.control_widget.model_widget.update_parameters(self.data.models[index].parameters)

    def start_model_picking(self):
        if self.main_widget.model_list.currentRow()==-1:
            return
        self.main_widget.model_define_btn.clicked.disconnect(self.start_model_picking)
        self.main_widget.model_define_btn.clicked.connect(self.end_model_picking)
        self.main_widget.model_define_btn.setText("Finish")
        self.main_widget.control_widget.disable(except_widgets=[self.main_widget.model_define_btn])

        self.main_widget.spectrum_widget.mouse_moved.connect(self.update_model_parameters)
        self.main_widget.spectrum_widget.mouse_left_clicked.connect(self.pick_model_parameter)


    def end_model_picking(self):
        self.main_widget.model_define_btn.clicked.connect(self.start_model_picking)
        self.main_widget.model_define_btn.clicked.disconnect(self.end_model_picking)
        self.main_widget.model_define_btn.setText("Define")
        self.main_widget.model_define_btn.setChecked(False)
        self.main_widget.control_widget.enable()
        self.main_widget.spectrum_widget.mouse_moved.disconnect(self.update_model_parameters)
        self.main_widget.spectrum_widget.mouse_left_clicked.disconnect(self.pick_model_parameter)

    def update_model_parameters(self, x, y):
        cur_model_ind = int(self.main_widget.model_list.currentRow())
        self.data.update_current_model_parameter(cur_model_ind, x, y)

    def pick_model_parameter(self, x, y):
        cur_model_ind = int(self.main_widget.model_list.currentRow())
        more_parameters_available = self.data.pick_current_model_parameters(cur_model_ind, x, y)
        if not more_parameters_available:
            self.end_model_picking()


    def load_data(self, filename=None):
        if filename is None:
            filename = str(QtWidgets.QFileDialog.getOpenFileName(self.main_widget, "Load Data File",
                                                             ''))
        if filename is not '':
            self.data.load_data(filename)

    def save_data(self, filename=None):
        if filename is None:
            save_file_dialog = QtWidgets.QFileDialog()
            save_file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            save_file_dialog.setNameFilters(['Data (*.txt)'])
            save_file_dialog.selectFile(os.path.join(self.save_data_path,
                                                     self.data.spectrum.name+".txt"))

            if save_file_dialog.exec_():
                filename = str(save_file_dialog.selectedFiles()[0])
            else:
                filename = ''

        if filename is not '':
            self.data.save_data(filename)
            self.save_data_path = os.path.dirname(filename)



    def roi_item_changed(self):
        x_min, x_max = self.main_widget.spectrum_widget.linear_region_item.getRegion()
        self.data.roi = (x_min, x_max)

    def close_event(self, _):
        QtWidgets.QApplication.closeAllWindows()
        QtWidgets.QApplication.quit()