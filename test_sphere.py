"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_sphere

or, for individual test classes:

  $ python -m unittest -v test_sphere.Test_Sphere
  $ python -m unittest -v test_sphere.Test_get_sphere
"""

import math
import numpy as np
import unittest
from sphere import Sphere, get_sphere, epsilon_distance

class Test_Sphere(unittest.TestCase):

    def test_GivenAnEmptyCenter_When_Sphere_ThenExceptionIsRaised(self):
        RADIUS = 3.
        self.assertRaises(TypeError, Sphere, None, RADIUS)

    def test_GivenA2DCenterPoint_When_Sphere_ThenExceptionIsRaised(self):
        CENTER = np.array([1, 3], np.float_)
        RADIUS = 3.
        self.assertRaises(TypeError, Sphere, CENTER, RADIUS)

    def test_GivenAMissingRadius_When_Sphere_ThenExceptionIsRaised(self):
        CENTER = np.array([1, 3, 6], np.float_)
        self.assertRaises(TypeError, Sphere, CENTER)

    def test_Given2SpheresCreatedEqually_WhenComparision_ThenReturnTrue(self):
        CENTER = np.array([1, 3, 6], np.float_)
        RADIUS = 3.
        self.assertEqual(Sphere(CENTER, RADIUS), Sphere(CENTER, RADIUS))
        SPHERE = Sphere(CENTER, RADIUS)
        self.assertEqual(SPHERE, Sphere(CENTER, RADIUS))

    def test_Given2SpheresCreatedNotEqually_WhenComparision_ThenReturnFalse(self):
        POINT_A = np.array([1, 3, 6], np.float_)
        RADIUS = 3.
        self.assertNotEqual(Sphere(POINT_A, RADIUS), Sphere(POINT_A, RADIUS + 1.))
        POINT_B = np.array([4, 3, 3], np.float_)
        self.assertNotEqual(Sphere(POINT_A, RADIUS), Sphere(POINT_B, RADIUS))

    def test_GivenSphereCreatedWithRadiusR_When_get_radius_ThenReturnR(self):
        CENTER = np.array([1, 2, 3], np.float_)
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        # SPHERE.spy("SPHERE")
        self.assertEqual(SPHERE.get_radius(), RADIUS)

    def test_GivenSphereAndPointEqualToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnTrue(self):
        CENTER = np.array([1, 2, 3], np.float_)
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS, 0, 0], np.float_)
        self.assertTrue(SPHERE.point_is_on_surface(POINT))

    def test_GivenSphereAndPointAlmostEqualToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnTrue(self):
        CENTER = np.array([1, 2, 3], np.float_)
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + epsilon_distance/2., 0, 0], np.float_)
        self.assertTrue(SPHERE.point_is_on_surface(POINT))

    def test_GivenSphereAndPointFarEnoughToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnFalse(self):
        CENTER = np.array([1, 2, 3], np.float_)
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + 2. * epsilon_distance, 0, 0], np.float_)
        self.assertFalse(SPHERE.point_is_on_surface(POINT))

class Test_get_sphere(unittest.TestCase):

    def test_GivenAPointP_When_get_sphere_WithP4x_and_get_radius_ThenExceptionIsRaised(self):
        POINT = np.array([1, 3, 6], np.float_)
        POINTS = (POINT, POINT, POINT, POINT)
        self.assertRaises(ArithmeticError, get_sphere, POINTS)

    def test_Given4PointsFrom_31_136_12_106_When_get_sphere_ThenReturnTheSitesResult(self):
        POINT_1 = np.array([-34.1186,  1.389,   8.5034], np.float_)
        POINT_2 = np.array([-34.3179,  1.3719, -29.432], np.float_)
        POINT_3 = np.array([-8.7948,  -0.1148, -10.462], np.float_)
        POINT_4 = np.array([-60.527,   5.8305, -10.423], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
        SPHERE_31_136_12_106 = get_sphere(POINTS)

        CENTER_FROM_SITE = np.array([-21.942809924607257, 113.52343730620188,-10.579341367428881], np.float_)
        RADIUS_FROM_SITE = 114.39638504793206
        SPHERE_FROM_SITE = Sphere(CENTER_FROM_SITE, RADIUS_FROM_SITE)

        self.assertEqual(SPHERE_31_136_12_106, SPHERE_FROM_SITE)

    def test_Given4PointsFrom_39_136_10_106_When_get_sphere_ThenReturnTheSitesResult(self):
        POINT_1 = np.array([-34.5737, 0.5015,  10.377], np.float_)
        POINT_2 = np.array([-34.4944, 0.4966, -22.06], np.float_)
        POINT_3 = np.array([-8.2244,  0.5713,  -5.6182], np.float_)
        POINT_4 = np.array([-60.996,  4.412,   -5.7822], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
        SPHERE_39_136_10_106 = get_sphere(POINTS)

        CENTER_FROM_SITE = np.array([-26.681763623168056, 111.42322500511179, -5.8390596432420425], np.float_)
        RADIUS_FROM_SITE = 112.37825558460493
        SPHERE_FROM_SITE = Sphere(CENTER_FROM_SITE, RADIUS_FROM_SITE)

        self.assertEqual(SPHERE_39_136_10_106, SPHERE_FROM_SITE)

if __name__ == '__main__':
    unittest.main()
