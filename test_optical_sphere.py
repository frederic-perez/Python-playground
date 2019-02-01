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
        POINT = np.array([1, 3, 6], np.float_)
        RADIUS = 3.
        N = 1.5
        self.assertEqual(OpticalSphere(POINT, RADIUS, N), OpticalSphere(POINT, RADIUS, N))
        OPTICAL_SPHERE = OpticalSphere(POINT, RADIUS, N)
        self.assertEqual(OPTICAL_SPHERE, OpticalSphere(POINT, RADIUS, N))

if __name__ == '__main__':
    unittest.main()
