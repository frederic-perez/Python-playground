"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_sphere

or, for individual test classes (sorted as appearing in this file):

  $ python -m unittest -v test_sphere.Test_Sphere
  $ python -m unittest -v test_sphere.Test_get_sphere
"""

import numpy as np
import unittest
from epsilon import epsilon_distance, equal_in_practice, zero_in_practice
from sphere import Sphere, get_sphere

class Test_Sphere(unittest.TestCase):

    def test_GivenAnEmptyCenter_When_Sphere_ThenExceptionIsRaised(self):
        RADIUS = 3.
        self.assertRaises(TypeError, Sphere, None, RADIUS)

    def test_GivenA2DCenterPoint_When_Sphere_ThenExceptionIsRaised(self):
        CENTER_2D = [1, 3]
        RADIUS = 3.
        self.assertRaises(TypeError, Sphere, CENTER_2D, RADIUS)

    def test_GivenAMissingRadius_When_Sphere_ThenExceptionIsRaised(self):
        CENTER = [1, 3, 6]
        self.assertRaises(TypeError, Sphere, CENTER)

    def test_GivenAZeroRadius_When_Sphere_ThenExceptionIsRaised(self):
        CENTER = [1, 3, 6]
        ZERO_RADIUS = 0
        self.assertRaises(ValueError, Sphere, CENTER, ZERO_RADIUS)

    def test_GivenANegativeRadius_When_Sphere_ThenExceptionIsRaised(self):
        CENTER = [1, 3, 6]
        NEGATIVE_RADIUS = -7
        self.assertRaises(ValueError, Sphere, CENTER, NEGATIVE_RADIUS)

    def test_Given2SpheresCreatedEqually_WhenComparision_ThenReturnTrue(self):
        CENTER = [1, 3, 6]
        RADIUS = 3.
        self.assertEqual(Sphere(CENTER, RADIUS), Sphere(CENTER, RADIUS))
        SPHERE = Sphere(CENTER, RADIUS)
        self.assertEqual(SPHERE, Sphere(CENTER, RADIUS))

    def test_Given2SpheresCreatedNotEqually_WhenComparision_ThenReturnFalse(self):
        POINT_A = [1, 3, 6]
        RADIUS = 3.
        self.assertNotEqual(Sphere(POINT_A, RADIUS), Sphere(POINT_A, RADIUS + 1.))
        POINT_B = [4, 3, 3]
        self.assertNotEqual(Sphere(POINT_A, RADIUS), Sphere(POINT_B, RADIUS))

    def test_GivenSphereCreatedWithRadiusR_When_get_radius_ThenReturnR(self):
        CENTER = [1, 2, 3]
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        # SPHERE.spy("SPHERE")
        self.assertEqual(SPHERE.get_radius(), RADIUS)

    def test_GivenCircleCreatedWithCenterC_When_get_center_ThenReturnC(self):
        CENTER = [1, 2, 3]
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        RETURNED_CENTER = SPHERE.get_center()
        EQUAL_CENTERS = equal_in_practice(CENTER[0], RETURNED_CENTER[0]) \
            and equal_in_practice(CENTER[1], RETURNED_CENTER[1]) \
            and equal_in_practice(CENTER[2], RETURNED_CENTER[2])
        self.assertTrue(EQUAL_CENTERS)

    def test_GivenSphereAndPointEqualToCenterPlusRadiusForZ_When_get_signed_distance_to_surface_ThenReturnZero(self):
        CENTER = [1, 2, 3]
        RADIUS = 8
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([0, 0, RADIUS])
        self.assertTrue(zero_in_practice(SPHERE.get_signed_distance_to_surface(POINT)))

    def test_GivenSphereAndPointEqualToCenterPlus2RadiusForZ_When_get_signed_distance_to_surface_ThenReturnRadius(self):
        CENTER = [1, 2, 3]
        RADIUS = 8
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([0, 0, 2*RADIUS])
        self.assertTrue(equal_in_practice(SPHERE.get_signed_distance_to_surface(POINT), RADIUS))

    def test_GivenSphereAndPointEqualToCenterPlusHalfRadiusForZ_When_get_signed_distance_to_surface_ThenReturnMinusHalfRadius(self):
        CENTER = [1, 2, 3]
        RADIUS = 8
        HALF_RADIUS = RADIUS/2
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([0, 0, HALF_RADIUS])
        self.assertTrue(equal_in_practice(SPHERE.get_signed_distance_to_surface(POINT), -HALF_RADIUS))

    def test_GivenSphereAndPointEqualToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnTrue(self):
        CENTER = [1, 2, 3]
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS, 0, 0])
        self.assertTrue(SPHERE.point_is_on_surface(POINT))

    def test_GivenSphereAndPointAlmostEqualToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnTrue(self):
        CENTER = [1, 2, 3]
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + epsilon_distance/2., 0, 0])
        self.assertTrue(SPHERE.point_is_on_surface(POINT))

    def test_GivenSphereAndPointFarEnoughToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnFalse(self):
        CENTER = [1, 2, 3]
        RADIUS = 7
        SPHERE = Sphere(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + 2. * epsilon_distance, 0, 0])
        self.assertFalse(SPHERE.point_is_on_surface(POINT))

class Test_get_sphere(unittest.TestCase):

    def test_GivenNotExactly4Points_When_get_sphere_ThenExceptionIsRaised(self):
        POINT = [1, 3]
        self.assertRaises(ValueError, get_sphere, [POINT])
        self.assertRaises(ValueError, get_sphere, [POINT, POINT])
        self.assertRaises(ValueError, get_sphere, [POINT, POINT, POINT])
        self.assertRaises(ValueError, get_sphere, [POINT, POINT, POINT, POINT, POINT])

    def test_GivenAPointP_4x_When_get_sphere_ThenExceptionIsRaised(self):
        POINT = [1, 3, 6]
        POINTS = (POINT, POINT, POINT, POINT)
        self.assertRaises(ArithmeticError, get_sphere, POINTS)

    def test_Given4CollinealPoints_When_get_sphere_ThenExceptionIsRaised(self):
        DELTA = 1.5
        points = []
        for i in [1, 2, 3, 4]:
            points.append([i*DELTA, 0, 0])
        self.assertRaises(ArithmeticError, get_sphere, points)

    def test_Given4CoplanarPoints_When_get_sphere_ThenExceptionIsRaised(self):
        DELTA = 1.5
        points = []
        for i in [1, 2]:
            points.append([i*DELTA, i, 0])
            points.append([i*DELTA, i + 1., 0])
        self.assertRaises(ArithmeticError, get_sphere, points)

    def test_Given4PointsFrom_31_136_12_106_When_get_sphere_ThenReturnTheSitesResult(self):
        POINT_1 = [-34.1186,  1.389,   8.5034]
        POINT_2 = [-34.3179,  1.3719, -29.432]
        POINT_3 = [-8.7948,  -0.1148, -10.462]
        POINT_4 = [-60.527,   5.8305, -10.423]
        POINTS = [POINT_1, POINT_2, POINT_3, POINT_4]
        SPHERE_31_136_12_106 = get_sphere(POINTS)

        CENTER_FROM_SITE = [-21.942809924607257, 113.52343730620188,-10.579341367428881]
        RADIUS_FROM_SITE = 114.39638504793206
        SPHERE_FROM_SITE = Sphere(CENTER_FROM_SITE, RADIUS_FROM_SITE)

        self.assertEqual(SPHERE_31_136_12_106, SPHERE_FROM_SITE)

    def test_Given4PointsFrom_39_136_10_106_When_get_sphere_ThenReturnTheSitesResult(self):
        POINT_1 = [-34.5737, 0.5015,  10.377]
        POINT_2 = [-34.4944, 0.4966, -22.06]
        POINT_3 = [-8.2244,  0.5713,  -5.6182]
        POINT_4 = [-60.996,  4.412,   -5.7822]
        POINTS = [POINT_1, POINT_2, POINT_3, POINT_4]
        SPHERE_39_136_10_106 = get_sphere(POINTS)

        CENTER_FROM_SITE = [-26.681763623168056, 111.42322500511179, -5.8390596432420425]
        RADIUS_FROM_SITE = 112.37825558460493
        SPHERE_FROM_SITE = Sphere(CENTER_FROM_SITE, RADIUS_FROM_SITE)

        self.assertEqual(SPHERE_39_136_10_106, SPHERE_FROM_SITE)

if __name__ == '__main__':
    unittest.main()
