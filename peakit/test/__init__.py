# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import os

test_path = os.path.dirname(__file__)
data_path = os.path.join(test_path, 'data')

def get_data_path(filename):
    return os.path.join(data_path, filename)