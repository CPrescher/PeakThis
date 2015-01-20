# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
from copy import copy

import numpy as np

from model.DataModel import DataModel
from model.PickModels import PickGaussianModel, PickQuadraticModel


class DataModelTest(unittest.TestCase):
    def setUp(self):
        self.data = DataModel()

    def tearDown(self):
        pass

    def array_almost_equal(self, array1, array2):
        self.assertAlmostEqual(np.sum(array1 - array2), 0)

    def array_not_almost_equal(self, array1, array2):
        self.assertNotAlmostEqual(np.sum(array1 - array2), 0)

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
        new_parameters['amplitude'].value = 10

        self.data.update_model(0, new_parameters)
        new_spec = self.data.get_model_spectrum(0)
        new_spec_x, new_spec_y = new_spec.data

        pure_model_y = self.data.models[0].quick_eval(spec_x)

        self.array_almost_equal(new_spec_x, spec_x)
        self.array_almost_equal(new_spec_y, pure_model_y + bkg_y)

    def test_picking_model_paameters(self):
        self.data.add_model(PickGaussianModel())
        _, model_y = self.data.get_model_spectrum(0).data

        self.data.update_current_model_parameter(0, 1, 1)
        _, model_y1 = self.data.get_model_spectrum(0).data

        self.array_not_almost_equal(model_y, model_y1)
        self.data.pick_current_model_parameters(0, 1, 1)

        _, model_y2 = self.data.get_model_spectrum(0).data

        self.array_almost_equal(model_y1, model_y2)