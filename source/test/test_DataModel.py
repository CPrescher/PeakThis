# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from copy import copy

import numpy as np

from ..model.DataModel import DataModel
from ..model.PickModels import PickGaussianModel, PickQuadraticModel, PickLinearModel


class DataModelTest(unittest.TestCase):
    def setUp(self):
        self.data = DataModel()

    def tearDown(self):
        pass

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

    def create_peak(self, x, center, amplitude, sigma=0.2):
        gauss_curve = PickGaussianModel()
        gauss_curve.set_parameter_value('center', center)
        gauss_curve.set_parameter_value('amplitude', amplitude)
        gauss_curve.set_parameter_value('sigma', sigma)
        return gauss_curve.quick_eval(x)

    def test_add_models(self):
        self.data.add_model(PickGaussianModel())
        self.assertEqual(len(self.data.models), 1)
        self.data.add_model(PickQuadraticModel())
        self.data.add_model(PickQuadraticModel())
        self.data.add_model(PickQuadraticModel())
        self.data.add_model(PickQuadraticModel())
        self.assertEqual(len(self.data.models), 5)

    def test_delete_models(self):
        self.data.add_model(PickQuadraticModel())
        self.data.add_model(PickQuadraticModel())
        self.data.add_model(PickQuadraticModel())
        self.data.add_model(PickQuadraticModel())
        self.assertEqual(len(self.data.models), 4)
        self.data.del_model(3)
        self.assertEqual(len(self.data.models), 3)
        self.data.del_model()
        self.data.del_model()
        self.data.del_model()
        self.assertEqual(len(self.data.models), 0)

    def test_get_model_spectrum(self):
        # get_model_spectrum should give a spectrum on top of the current background spectrum
        # for a empty PickGaussianModel this results in the model spectrum being equal to the background spectrum
        self.data.add_model(PickGaussianModel())
        model_spectrum = self.data.get_model_spectrum(0)
        model_x, model_y = model_spectrum.data
        data_x, data_y = self.data.spectrum.data
        self.assertEqual(np.sum(model_y), 0)
        self.array_almost_equal(model_x, data_x)

    def test_updating_models(self):
        self.data.add_model(PickGaussianModel())
        spec = self.data.get_model_spectrum(0)
        spec_x, spec_y = spec.data
        bkg_x, bkg_y = self.data.get_model_spectrum(0).data
        self.array_almost_equal(spec_y, bkg_y)

        new_parameters = copy(self.data.models[0].parameters)
        new_parameters[self.data.models[0].prefix + 'amplitude'].value = 10

        self.data.update_model(0, new_parameters)
        new_spec = self.data.get_model_spectrum(0)
        new_spec_x, new_spec_y = new_spec.data

        pure_model_y = self.data.models[0].quick_eval(spec_x)

        self.array_almost_equal(new_spec_x, spec_x)
        self.array_almost_equal(new_spec_y, pure_model_y + bkg_y)

    def test_picking_model_parameters(self):
        self.data.add_model(PickGaussianModel())
        _, model_y = self.data.get_model_spectrum(0).data

        self.data.update_current_model_parameter(0, 1, 1)
        _, model_y1 = self.data.get_model_spectrum(0).data

        self.array_not_almost_equal(model_y, model_y1)
        self.data.pick_current_model_parameters(0, 1, 1)

        _, model_y2 = self.data.get_model_spectrum(0).data

        self.array_almost_equal(model_y1, model_y2)

    def test_fitting_model(self):
        self.data.add_model(PickLinearModel())
        slope = 1.4
        intercept = 0.1

        x = np.linspace(-3, 3., 100)
        y = intercept + slope * x + np.random.normal(0, 0.01, x.shape)
        self.data.spectrum.data = x, y

        self.data.fit_data()

        self.assertAlmostEqual(self.data.models[0].get_parameter_value('intercept'), intercept, places=2)
        self.assertAlmostEqual(self.data.models[0].get_parameter_value('slope'), slope, places=2)

    def test_fitting_different_models(self):
        self.data.add_model(PickLinearModel())
        self.data.add_model(PickGaussianModel())

        # create data
        x = np.linspace(-3, 3, 1000)

        slope = 1.4
        intercept = 0.1
        y = intercept + slope * x

        center = 0
        amplitude = 10
        sigma = 0.1
        y += self.create_peak(x, center, amplitude, sigma)

        self.data.pick_current_model_parameters(1, 0, 10)
        self.data.pick_current_model_parameters(1, 0.25, 0.02)

        self.data.spectrum.data = x, y
        self.data.fit_data()

        self.assertAlmostEqual(self.data.models[0].get_parameter_value('intercept'), intercept, places=7)
        self.assertAlmostEqual(self.data.models[0].get_parameter_value('slope'), slope, places=7)

        self.assertAlmostEqual(self.data.models[1].get_parameter_value('center'), center, places=7)
        self.assertAlmostEqual(self.data.models[1].get_parameter_value('amplitude'), amplitude, places=7)
        self.assertAlmostEqual(self.data.models[1].get_parameter_value('sigma'), sigma, places=7)

    def test_fitting_multiple_models_of_the_same_type(self):
        # create test data:
        x = np.linspace(0, 10, 100)

        center_1 = 3
        amplitude_1 = 10
        sigma_1 = 0.3

        center_2 = 7
        amplitude_2 = 6
        sigma_2 = 0.5

        y = self.create_peak(x, center_1, amplitude_1, sigma_1)
        y += self.create_peak(x, center_2, amplitude_2, sigma_2)

        # creating the models in the data
        self.data.add_model(PickGaussianModel())
        self.data.add_model(PickGaussianModel())

        # define some initial values for the peaks
        self.data.pick_current_model_parameters(0, 3, 10)
        self.data.pick_current_model_parameters(0, 3.25, 0.02)

        self.data.pick_current_model_parameters(1, 7, 6)
        self.data.pick_current_model_parameters(1, 7.25, 0.02)

        self.data.fit_data()

        self.assertEqual(len(self.data.models[0].parameters), 3)

    def test_using_background_model(self):
        # creating a dummy spectrum
        x = np.linspace(0, 10, 100)
        y = x**2
        self.data.set_spectrum_data(x, y)

        # creating the dummy background
        self.data.background_model.add_point(0,0)
        self.data.background_model.add_point(10,1)

        # spectrum should be unchanged
        x1, y1 = self.data.get_spectrum_data()
        self.array_almost_equal(x1, x)
        self.array_almost_equal(y1, y)

        # setting the set_background_subtracted_flag which should actually change all the
        self.data.set_background_subtracted(True)

        # data spectrum
        x2, y2 = self.data.get_spectrum_data()
        self.array_not_almost_equal(y2, y1)

        # background
        bkg_x, bkg_y = self.data.get_background_spectrum().data
        self.array_almost_equal(bkg_y, np.zeros(x.shape))

        # background_points
        bkg_x_points, bkg_y_points = self.data.get_background_points_spectrum().data
        self.array_almost_equal(bkg_y_points, np.zeros(bkg_x_points.shape))




