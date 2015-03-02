# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import tempfile

import numpy as np
from scipy.interpolate import PchipInterpolator
from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui

from ..controller.MainController import MainController
from ..model.PickModels import PickGaussianModel


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
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(click1_pos[0], click1_pos[1])
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(click2_pos[0], click2_pos[1])

    def copy_model(self, click1_pos, click2_pos):
        QTest.mouseClick(self.main_widget.model_copy_btn, QtCore.Qt.LeftButton)
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(click1_pos[0], click1_pos[1])
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(click2_pos[0], click2_pos[1])


    def create_spectrum(self):
        self.x = np.linspace(0, 10, 1000)
        self.y = np.zeros(self.x.shape)

        # creating the background:
        bkg_x = [0, 3, 7, 10]
        bkg_y = [1, 1.2, 1.1, 1]
        pchip_interpolator = PchipInterpolator(bkg_x, bkg_y, extrapolate=True)
        self.y += pchip_interpolator(self.x)

        # creating the models
        def create_peak(x, center, amplitude, sigma=0.2):
            gauss_curve = PickGaussianModel()
            gauss_curve.set_parameter_value('center', center)
            gauss_curve.set_parameter_value('amplitude', amplitude)
            gauss_curve.set_parameter_value('sigma', sigma)
            return gauss_curve.quick_eval(x)

        self.y += create_peak(self.x, 1, 10)
        self.y += create_peak(self.x, 3, 5)
        self.y += create_peak(self.x, 6, 2)
        self.y += create_peak(self.x, 7.5, 3)
        self.y += create_peak(self.x, 9, 8)

        #adding noise
        self.y += np.random.normal(0, 0.03 * np.max(self.y), self.y.shape)

        self.temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        np.savetxt(self.temp_file, np.dstack((self.x, self.y))[0])
        self.temp_file.close()


    def test_use_case_for_raman_fitting(self):
        # Edith opens PeakThis sees the open file button and loads her spectrum into the program
        # she clicks the button and loads a spectrum
        self.controller.load_data(self.temp_file.name)

        # Edith notices that the spectrum is immediately shown in the graph window
        QtGui.QApplication.processEvents()
        x, y = self.main_widget.spectrum_widget.get_plot_data()

        self.array_almost_equal(x, self.x)
        self.array_almost_equal(y, self.y)

        # then she sees that she can define a background for her Data
        # she chooses that the standard pchip should be fine to model her data
        # and clicks define and sees that she can add points by clicking into the spectrum

        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        bkg_click_points_x = [0, 3, 5]
        bkg_click_points_y = [1, 1.2, 6]

        for ind in range(len(bkg_click_points_x)):
            self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(bkg_click_points_x[ind],
                                                                                  bkg_click_points_y[ind])

        bkg_points_x, bkg_points_y = self.main_widget.spectrum_widget.get_background_points_data()

        self.array_almost_equal(bkg_points_x, bkg_click_points_x)
        self.array_almost_equal(bkg_points_y, bkg_click_points_y)

        # every time she clicks in the spectrum after the first three clicks she sees that the background changes
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(7, 1.1)

        x, bkg_y1 = self.main_widget.spectrum_widget.get_background_plot_data()
        self.array_almost_equal(self.x, x)

        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(10, 1)
        x, bkg_y2 = self.main_widget.spectrum_widget.get_background_plot_data()

        self.array_not_almost_equal(bkg_y1, bkg_y2)

        # after inspecting her data and background model she thinks that 'pchip' is maybe not the best way to
        # approximate the background so she tries the spline model, and she notices how the background is change

        self.main_widget.background_method_cb.setCurrentIndex(1)

        x, bkg_y3 = self.main_widget.spectrum_widget.get_background_plot_data()
        self.array_not_almost_equal(bkg_y2, bkg_y3)

        # then she sees that spline is actually worse and goes back to pchip
        self.main_widget.background_method_cb.setCurrentIndex(0)
        x, bkg_y4 = self.main_widget.spectrum_widget.get_background_plot_data()
        self.array_almost_equal(bkg_y4, bkg_y2)

        # Edith decides that she is finished with the background and clicks the button to finish it

        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        # she notices that clicking into the spectrum now does not effect background any more...
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(10, 10)
        x, bkg_y5 = self.main_widget.spectrum_widget.get_background_plot_data()
        self.array_almost_equal(bkg_y5, bkg_y4)

        # while playing and being happy that everything works she realizes that there is one point which might be
        # better deleted
        # She clicks the define button again and moves to the point and tries to delete by pressing x
        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)


        class DummyKeyPressEvent():
            def __init__(self, text):
                self._text = text

            def text(self):
                return self._text


        self.main_widget.spectrum_widget._spectrum_plot_set_current_mouse_position(6.2, 4.5)
        self.main_widget.spectrum_widget._spectrum_plot_send_keypress_event(DummyKeyPressEvent('x'))

        bkg_scatter_x, bkg_scatter_y = self.main_widget.spectrum_widget.get_background_points_data()
        self.array_almost_equal(bkg_scatter_x, [0, 3, 7, 10])
        self.array_almost_equal(bkg_scatter_y, [1, 1.2, 1.1, 1])

        # Now she is satisfied with the result and finishes the background determination process
        QTest.mouseClick(self.main_widget.background_define_btn, QtCore.Qt.LeftButton)

        # she notices that pressing x does not delete points anymore
        self.main_widget.spectrum_widget._spectrum_plot_send_keypress_event(DummyKeyPressEvent('x'))
        bkg_scatter_x, bkg_scatter_y = self.main_widget.spectrum_widget.get_background_points_data()
        self.array_almost_equal(bkg_scatter_x, [0, 3, 7, 10])
        self.array_almost_equal(bkg_scatter_y, [1, 1.2, 1.1, 1])

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
        start_x, start_y = self.main_widget.spectrum_widget.get_model_plot_data(0)
        self.model_widget.parameter_table.item(0, 1).setText('20')
        self.model_widget.parameter_table.item(1, 1).setText('3')
        self.model_widget.parameter_table.item(2, 1).setText('19')
        after_x, after_y = self.main_widget.spectrum_widget.get_model_plot_data(0)
        self.array_almost_equal(start_x, after_x)
        self.array_not_almost_equal(start_y, after_y)

        # then she sees the "Define" and wonders, if this also makes it possible to visually define the model, like
        # she did before with the Background

        QTest.mouseClick(self.main_widget.model_define_btn, QtCore.Qt.LeftButton)
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(1, 10)
        self.main_widget.spectrum_widget._spectrum_plot_emit_mouse_click_event(1.3, 4.5)

        after_define_x, after_define_y = self.main_widget.spectrum_widget.get_model_plot_data(0)
        self.array_not_almost_equal(after_define_y, after_y)


        # She decides to add some other peaks for fitting all the peaks she sees:
        self.add_peak(0, (3, 5), (3.3, 9.5))
        self.add_peak(0, (6, 2), (6.2, 14.6))
        self.add_peak(0, (7.5, 3), (7.8, 8))
        self.add_peak(0, (9, 8), (9.4, 11))

        self.assertEqual(self.main_widget.model_list.count(), 5)
        self.assertEqual(self.main_widget.spectrum_widget.get_number_of_model_plots(), 5)

        # she sees that there is a copy button and wonders if this will just take of the hassle to always use the
        # model selector
        QTest.mouseClick(self.main_widget.model_copy_btn, QtCore.Qt.LeftButton)

        self.assertEqual(self.main_widget.model_list.count(), 6)
        self.assertEqual(self.main_widget.spectrum_widget.get_number_of_model_plots(), 6)

        # then she sees that the last peak is doubled now and should be removed from the list

        QTest.mouseClick(self.main_widget.model_delete_btn, QtCore.Qt.LeftButton)
        self.assertEqual(self.main_widget.model_list.count(), 5)
        self.assertEqual(self.main_widget.spectrum_widget.get_number_of_model_plots(), 5)

        # now she is satisfied with the initial model and wants to fit the peaks:
        before_x, before_y = self.main_widget.spectrum_widget.get_model_plot_data(0)
        QTest.mouseClick(self.main_widget.fit_btn, QtCore.Qt.LeftButton)

        after_x, after_y = self.main_widget.spectrum_widget.get_model_plot_data(0)
        self.array_not_almost_equal(before_y, after_y)

        # and she sees that the lower graph now also shows the residual
        residual_x, residual_y = self.main_widget.spectrum_widget.get_residual_plot_data()
        self.array_almost_equal(after_x, residual_x)
        self.assertNotEqual(np.sum(residual_y), 0)

        # self.fail("Finish the Test!")