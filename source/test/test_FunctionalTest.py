# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest

import numpy as np

from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt

import tempfile

from controller.MainController import MainController
from model.PickModels import PickGaussianModel


class PeakThisFunctionalTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.controller = MainController()
        self.main_widget = self.controller.main_widget
        self.model_widget = self.controller.main_widget.control_widget.model_widget
        self.create_spectrum()

    def tearDown(self):
        del self.app


    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def add_peak(self, type_number, click1_pos, click2_pos):
        QTest.mouseClick(self.main_widget.model_add_btn, QtCore.Qt.LeftButton)
        self.main_widget.model_selector_dialog.model_list.setCurrentRow(type_number)
        QTest.mouseClick(self.main_widget.model_selector_dialog.ok_btn, QtCore.Qt.LeftButton)
        QTest.mouseClick(self.main_widget.model_define_btn, QtCore.Qt.LeftButton)
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(click1_pos[0], click1_pos[1])
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(click2_pos[0], click2_pos[1])

    def create_spectrum(self):
        self.x = np.linspace(0, 10, 145)
        self.y = np.zeros(self.x.shape)
        gauss_curve = PickGaussianModel()
        gauss_curve.parameters['center'].value = 6
        gauss_curve.parameters['amplitude'].value = 10
        self.y += gauss_curve.quick_eval(self.x)
        gauss_curve.parameters['center'].value = 2
        gauss_curve.parameters['amplitude'].value = 6
        self.y += gauss_curve.quick_eval(self.x)

        self.temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        np.savetxt(self.temp_file, np.dstack((self.x, self.y))[0])
        self.temp_file.close()


    def test_use_case_for_raman_fitting(self):
        # Edith opens PeakThis sees the open file button and loads her spectrum into the program
        # she clicks the button and loads a spectrum
        self.controller.load_data(self.temp_file.name)

        # Edith notices that the spectrum is immediately shown in the graph window
        QtGui.QApplication.processEvents()
        x, y = self.main_widget.spectrum_widget.data_plot_item.getData()

        self.array_almost_equal(x, self.x)
        self.array_almost_equal(y, self.y)

        # then she sees that she can define a background for her Data
        # she chooses that the standard pchip should be fine to model her data
        # and clicks define and sees that she can add points by clicking into the spectrum

        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        click_points_x = [2, 4, 5]
        click_points_y = [3, 4, 5]

        for ind in range(len(click_points_x)):
            self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(click_points_x[ind],
                                                                                   click_points_y[ind])

        bkg_points_x, bkg_points_y = self.main_widget.spectrum_widget.background_scatter_item.getData()

        self.array_almost_equal(bkg_points_x, click_points_x)
        self.array_almost_equal(bkg_points_y, click_points_y)

        # every time she clicks in the spectrum after the first three clicks she sees that the background changes
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(5.4, 2.4)

        x, bkg_y1 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_almost_equal(self.x, x)

        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(6.3, 2.5)
        x, bkg_y2 = self.main_widget.spectrum_widget.background_plot_item.getData()

        self.array_not_almost_equal(bkg_y1, bkg_y2)

        # after inspecting her data and background model she thinks that 'pchip' is maybe not the best way to
        # approximate the background so she tries the spline model, and she notices how the background is change

        self.main_widget.background_method_cb.setCurrentIndex(1)

        x, bkg_y3 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_not_almost_equal(bkg_y2, bkg_y3)

        # then she sees that spline is actually worse and goes back to pchip
        self.main_widget.background_method_cb.setCurrentIndex(0)
        x, bkg_y4 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_almost_equal(bkg_y4, bkg_y2)

        # Edith decides that she is finished with the background and clicks the button to finish it

        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        # she notices that clicking into the spectrum now does not effect background any more...
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(10,10)
        x, bkg_y5 = self.main_widget.spectrum_widget.background_plot_item.getData()
        self.array_almost_equal(bkg_y5, bkg_y4)

        # while playing and being happy that everything works she realizes that there is one point which might be
        # better a little bit lower
        # She clicks the define button again and moves to the point and tries to delete by pressing x
        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)


        class DummyKeyPressEvent():
            def __init__(self, text):
                self._text = text
            def text(self):
                return self._text


        self.main_widget.spectrum_widget.spectrum_plot.update_cur_mouse_position(6.2, 2.6)
        self.main_widget.spectrum_widget.spectrum_plot.keyPressEvent(DummyKeyPressEvent('x'))

        x_click, y_click = self.main_widget.spectrum_widget.background_scatter_item.getData()
        self.array_almost_equal(x_click, [2, 4, 5, 5.4])
        self.array_almost_equal(y_click, [3, 4, 5, 2.4])

        # Now she is satisfied with the result and finishes the background determination process
        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        # she notices that pressing x does not delete points anymore
        self.main_widget.spectrum_widget.spectrum_plot.keyPressEvent(DummyKeyPressEvent('x'))
        x_click, y_click = self.main_widget.spectrum_widget.background_scatter_item.getData()
        self.array_almost_equal(x_click, [2, 4, 5, 5.4])
        self.array_almost_equal(y_click, [3, 4, 5, 2.4])

        # As Edith is now happy with the background she decides to add a peak, because that's what she is here for,
        # right?
        # She sees that there is an add button an presses it
        QTest.mouseClick(self.main_widget.model_add_btn, QtCore.Qt.LeftButton)

        # a small dialog appears where she can choose the model she wants to add. She Sees that there are several
        # possible she thinks her peaks are
        # Gaussian shape like she chooses the Gaussian entry
        self.main_widget.model_selector_dialog.model_list.setCurrentRow(0)
        QTest.mouseClick(self.main_widget.model_selector_dialog.ok_btn, QtCore.Qt.LeftButton)

        # then she sees that a model appears in the list below the add button and that there is a table with
        # parameters available for the model

        self.assertGreater(self.main_widget.model_list.count(), 0)
        self.assertGreater(self.main_widget.model_parameter_table.rowCount(), 0)

        # she wonders if it is possible to change the parameters in the text boxes of the parameter table, and sees
        # that the spectrum is changing
        start_x, start_y = self.main_widget.spectrum_widget.model_plot_items[0].getData()
        self.model_widget.parameter_table.item(0,1).setText('20')
        self.model_widget.parameter_table.item(2,1).setText('19')
        after_x, after_y = self.main_widget.spectrum_widget.model_plot_items[0].getData()
        self.array_almost_equal(start_x, after_x)
        self.array_not_almost_equal(start_y, after_y)

        # then she sees the "Define" and wonders, if this also makes it possible to visually define the model, like
        # she did before with the Background

        QTest.mouseClick(self.main_widget.model_define_btn, QtCore.Qt.LeftButton)
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(5, 3)
        self.main_widget.spectrum_widget.spectrum_plot.mouse_left_clicked.emit(4, 3.5)

        after_define_x, after_define_y = self.main_widget.spectrum_widget.model_plot_items[0].getData()
        self.array_not_almost_equal(after_define_y, after_y)


        # She decides to add some other peaks for fitting all the peaks she sees:
        self.add_peak(0, (6,5), (2, 4.5))
        self.add_peak(0, (4,8), (2, 9.5))
        self.add_peak(0, (6,15), (2, 14.6))

        self.assertEqual(self.main_widget.model_list.count(), 4)
        self.assertEqual(len(self.main_widget.spectrum_widget.model_plot_items), 4)

        # then she sees that may be one peak should be removed from the list
        # she selects the second peak and clicks the delete button

        self.main_widget.model_list.setCurrentRow(1)
        QTest.mouseClick(self.main_widget.model_delete_btn, QtCore.Qt.LeftButton)

        self.assertEqual(self.main_widget.model_list.count(), 3)
        self.assertEqual(len(self.main_widget.spectrum_widget.model_plot_items), 3)



        # self.fail("Finish the Test!")