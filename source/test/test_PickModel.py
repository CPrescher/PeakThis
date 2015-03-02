# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest
import copy
import numpy as np

from ..model.PickModels import PickConstantModel, PickLinearModel, PickQuadraticModel, PickGaussianModel


class PickModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_model_value(self, model, x):
        return model.quick_eval(np.array([x]))[0]

    def test_constant_model(self):
        model = PickConstantModel()
        model.pick_parameter(2, 3)

        model_y = model.quick_eval(np.linspace(0, 10, 100))

        self.assertEqual(model_y[3], 3)
        self.assertTrue(np.array_equal(model_y, np.ones(100) * 3))

    def test_linear_model(self):
        model = PickLinearModel()
        model.pick_parameter(1., 2.)

        model_y = model.quick_eval(np.linspace(0, 10, 100))
        self.assertEqual(model_y[3], 2)
        self.assertTrue(np.array_equal(model_y, np.ones(100) * 2))

        model.pick_parameter(-1., 1.)
        self.assertEqual(self.get_model_value(model, 0), 1.5)

    def test_quadratic_model(self):
        model = PickQuadraticModel()
        model.pick_parameter(1., 2.)

        model_y = model.quick_eval(np.linspace(0, 10, 100))
        self.assertEqual(model_y[3], 2)
        self.assertTrue(np.array_equal(model_y, np.ones(100) * 2))

        model.pick_parameter(-1., 1.)
        self.assertEqual(self.get_model_value(model, 0), 1.5)

        model.pick_parameter(-3, 2)
        self.assertAlmostEqual(self.get_model_value(model, 0),
                               self.get_model_value(model, -2))

    def test_gaussian_model(self):
        model = PickGaussianModel()
        model.pick_parameter(1, 10)

        self.assertAlmostEqual(self.get_model_value(model, 1), 10, places=2)

        model.pick_parameter(3, 5)
        self.assertAlmostEqual(self.get_model_value(model, 1), 10, places=2)
        self.assertAlmostEqual(self.get_model_value(model, 3), 5, places=2)

    def test_copying_models_results_in_a_different_prefix(self):
        model1 = PickGaussianModel()
        model2 = copy.deepcopy(model1)

        self.assertNotEqual(model1.prefix, model2.prefix)
