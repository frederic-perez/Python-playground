"""
Run the tests by executing:
$ python -m unittest -v test_optical_sphere
"""

import math
import numpy as np
import unittest
from sphere import Sphere, get_sphere, epsilon_distance
from optical_sphere import OpticalSphere

class Test_OpticalSphere(unittest.TestCase):

    def test_Given2OpticalSpheresCreatedEqually_WhenComparision_ThenReturnTrue(self):
        RADIUS = 3.
        self.assertEqual(OpticalSphere(RADIUS), OpticalSphere(RADIUS))
        OPTICAL_SPHERE = OpticalSphere(RADIUS)
        self.assertEqual(OPTICAL_SPHERE, OpticalSphere(RADIUS))

if __name__ == '__main__':
    unittest.main()
