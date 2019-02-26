"""
Run the tests by executing:
$ python -m unittest -v test_optical_sphere
"""

import unittest
from epsilon import equal_in_practice
from optical_sphere import OpticalSphere

class Test_OpticalSphere(unittest.TestCase):

    def test_Given2OpticalSpheresCreatedEqually_WhenComparision_ThenReturnTrue(self):
        BASE = 1.
        self.assertEqual(OpticalSphere(BASE), OpticalSphere(BASE))
        OPTICAL_SPHERE = OpticalSphere(BASE)
        self.assertEqual(OPTICAL_SPHERE, OpticalSphere(BASE))

    def test_GivenOpticalSphereWithBase1_When_get_radius_ThenReturn530(self):
        # 530 mm is the radius of a 1 diopter curve
        BASE = 1.
        OPTICAL_SPHERE = OpticalSphere(BASE)
        self.assertTrue(equal_in_practice(OPTICAL_SPHERE.get_radius(), 530))

if __name__ == '__main__':
    unittest.main()
