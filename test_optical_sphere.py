"""
Run the tests by executing:
$ python -m unittest -v test_optical_sphere
"""

import unittest
from epsilon import equal_in_practice
from optical_sphere import OpticalSphere

class Test_OpticalSphere(unittest.TestCase):

    def test_Given2OpticalSpheresCreatedEqually_WhenComparision_ThenReturnTrue(self):
        RADIUS = 1.
        self.assertEqual(OpticalSphere(RADIUS), OpticalSphere(RADIUS))
        OPTICAL_SPHERE = OpticalSphere(RADIUS)
        self.assertEqual(OPTICAL_SPHERE, OpticalSphere(RADIUS))

    def test_GivenOpticalSphereWithRadius530_When_get_base_curve_ThenReturn1(self):
        RADIUS = 530 # 530 mm is the radius of a 1 diopter curve
        OPTICAL_SPHERE = OpticalSphere(RADIUS)
        self.assertTrue(equal_in_practice(OPTICAL_SPHERE.get_base_curve(), 1))

    def test_GivenOpticalSphereWithRadius106_When_get_radius_ThenReturn5(self):
        RADIUS = 106
        OPTICAL_SPHERE = OpticalSphere(RADIUS)
        self.assertTrue(equal_in_practice(OPTICAL_SPHERE.get_base_curve(), 5))

if __name__ == '__main__':
    unittest.main()
