"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_optical_sphere.py
  or
  $ python test_optical_sphere.py
"""

import unittest
from epsilon import equal_in_practice
from optical_sphere import OpticalSphere


class Test_OpticalSphere(unittest.TestCase):

    def test_Given2OpticalSpheresCreatedEqually_WhenComparison_ThenReturnTrue(self):
        radius = 1.
        self.assertEqual(OpticalSphere(radius), OpticalSphere(radius))
        optical_sphere = OpticalSphere(radius)
        self.assertEqual(optical_sphere, OpticalSphere(radius))

    def test_GivenOpticalSphereWithRadius530_When_get_base_curve_ThenReturn1(self):
        radius = 530  # 530 mm is the radius of a 1 diopter curve
        optical_sphere = OpticalSphere(radius)
        self.assertTrue(equal_in_practice(optical_sphere.get_base_curve(), 1))

    def test_GivenOpticalSphereWithRadius106_When_get_radius_ThenReturn5(self):
        radius = 106
        optical_sphere = OpticalSphere(radius)
        self.assertTrue(equal_in_practice(optical_sphere.get_base_curve(), 5))


if __name__ == '__main__':
    unittest.main()
