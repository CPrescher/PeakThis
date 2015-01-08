# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import unittest

import numpy as np
from model.BackgroundModel import BackgroundModel


class BackgroundModelTest(unittest.TestCase):
    def setUp(self):
        self.bkg_model = BackgroundModel()
        self.add_points()

    def tearDown(self):
        pass

    def add_points(self):
        self.x = [2,3,4,5,6,7]
        self.y = [4,5,6,10,3, 5]

        for ind in range(len(self.x)):
            self.bkg_model.add_point(self.x[ind],self.y[ind])

    def test_adding_points_to_the_model(self):
        self.assertEqual(self.bkg_model.x, self.x)
        self.assertEqual(self.bkg_model.y, self.y)

    def test_deleting_points_from_the_model(self):
        #test a close point
        self.bkg_model.delete_point_close_to(3.2, 5.1)
        self.x.remove(3)
        self.y.remove(5)
        self.assertEqual(self.bkg_model.x, self.x)
        self.assertEqual(self.bkg_model.y, self.y)

        self.bkg_model.delete_point_close_to(1, 2)
        self.assertEqual(self.bkg_model.x, self.x)
        self.assertEqual(self.bkg_model.y, self.y)

    def test_getting_interpolated_values(self):
        x = np.linspace(0,10)
        bkg_y = self.bkg_model.data(x)
        self.assertEqual(bkg_y.shape, x.shape)

        # changing the model will change to a different function
        self.bkg_model.method = 'spline'
        bkg_y2 = self.bkg_model.data(x)
        self.assertNotAlmostEqual(np.sum(bkg_y-bkg_y2), 0)




