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
        self.data.add_model(PickGaussianModel())
        spec = self.data.get_model_spectrum(0)
        spec_x, spec_y = spec.data
        data_x, data_y = self.data.spectrum.data
        self.assertEqual(np.sum(spec_y), 0)
        self.array_almost_equal(spec_x, data_x)

    def test_updating_models(self):
        self.data.add_model(PickGaussianModel())
        spec = self.data.get_model_spectrum(0)
        spec_x, spec_y = spec.data
        self.assertEqual(np.sum(spec_y), 0)

        new_parameters = copy(self.data.models[0].parameters)
        new_parameters['amplitude'].value = 10

        self.data.update_model(0, new_parameters)
        new_spec = self.data.get_model_spectrum(0)
        new_spec_x, new_spec_y = new_spec.data

        self.array_almost_equal(new_spec_x, spec_x)
        self.array_not_almost_equal(new_spec_y, spec_y)







