"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_circle

or, for individual test classes (sorted as appearing in this file):

  $ python -m unittest -v test_circle.Test_Circle
  $ python -m unittest -v test_circle.Test_get_circle
  $ python -m unittest -v test_circle.Test_get_MSE
  $ python -m unittest -v test_circle.Test_get_mean_signed_distance
  $ python -m unittest -v test_circle.Test_get_best_fit_circle
"""

import math
import numpy as np
import unittest
from circle import Circle, get_circle, get_best_fit_circle
from epsilon import epsilon_distance, equal_in_practice, zero_in_practice

class Test_Circle(unittest.TestCase):

    def test_GivenAnEmptyCenter_When_Circle_ThenExceptionIsRaised(self):
        RADIUS = 3.
        self.assertRaises(TypeError, Circle, None, RADIUS)

    def test_GivenA1DCenterPoint_When_Circle_ThenExceptionIsRaised(self):
        CENTER_1D = [1]
        RADIUS = 3.
        self.assertRaises(TypeError, Circle, CENTER_1D, RADIUS)

    def test_GivenAMissingRadius_When_Circle_ThenExceptionIsRaised(self):
        CENTER = [1, 3]
        self.assertRaises(TypeError, Circle, CENTER)

    def test_GivenAZeroRadius_When_Circle_ThenExceptionIsRaised(self):
        CENTER = [1, 3]
        ZERO_RADIUS = 0
        self.assertRaises(ValueError, Circle, CENTER, ZERO_RADIUS)

    def test_GivenANegativeRadius_When_Circle_ThenExceptionIsRaised(self):
        CENTER = [1, 3]
        NEGATIVE_RADIUS = -7
        self.assertRaises(ValueError, Circle, CENTER, NEGATIVE_RADIUS)

    def test_Given2CirclesCreatedEqually_WhenComparision_ThenReturnTrue(self):
        CENTER = [1, 3]
        RADIUS = 3.
        self.assertEqual(Circle(CENTER, RADIUS), Circle(CENTER, RADIUS))
        CIRCLE = Circle(CENTER, RADIUS)
        self.assertEqual(CIRCLE, Circle(CENTER, RADIUS))

    def test_Given2CirclesCreatedNotEqually_WhenComparision_ThenReturnFalse(self):
        POINT_A = [1, 3]
        RADIUS = 3.
        self.assertNotEqual(Circle(POINT_A, RADIUS), Circle(POINT_A, RADIUS + 1.))
        POINT_B = [4, 3]
        self.assertNotEqual(Circle(POINT_A, RADIUS), Circle(POINT_B, RADIUS))

    def test_GivenCircleCreatedWithRadiusR_When_get_radius_ThenReturnR(self):
        CENTER = [1, 2]
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        # CIRCLE.spy("CIRCLE")
        self.assertEqual(CIRCLE.get_radius(), RADIUS)

    def test_GivenCircleCreatedWithCenterC_When_get_center_ThenReturnC(self):
        CENTER = [1, 2]
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        RETURNED_CENTER = CIRCLE.get_center()
        EQUAL_CENTERS = equal_in_practice(CENTER[0], RETURNED_CENTER[0]) \
            and equal_in_practice(CENTER[1], RETURNED_CENTER[1])
        self.assertTrue(EQUAL_CENTERS)

    def test_GivenCircleAndPointEqualToCenterPlusRadiusForY_When_get_signed_distance_to_circumference_ThenReturnZero(self):
        CENTER = [1, 2]
        RADIUS = 8
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([0, RADIUS])
        self.assertTrue(zero_in_practice(CIRCLE.get_signed_distance_to_circumference(POINT)))

    def test_GivenCircleAndPointEqualToCenterPlus2RadiusForY_When_get_signed_distance_to_circumference_ThenReturnRadius(self):
        CENTER = [1, 2]
        RADIUS = 8
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([0, 2*RADIUS])
        self.assertTrue(equal_in_practice(CIRCLE.get_signed_distance_to_circumference(POINT), RADIUS))

    def test_GivenCircleAndPointEqualToCenterPlusHalfRadiusForY_When_get_signed_distance_to_circumference_ThenReturnMinusHalfRadius(self):
        CENTER = [1, 2]
        RADIUS = 8
        HALF_RADIUS = RADIUS/2
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([0, HALF_RADIUS])
        self.assertTrue(equal_in_practice(CIRCLE.get_signed_distance_to_circumference(POINT), -HALF_RADIUS))

    def test_GivenCircleAndPointEqualToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnTrue(self):
        CENTER = [1, 2]
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS, 0], np.float_)
        self.assertTrue(CIRCLE.point_is_on_circumference(POINT))

    def test_GivenCircleAndPointAlmostEqualToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnTrue(self):
        CENTER = [1, 2]
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + epsilon_distance/2., 0], np.float_)
        self.assertTrue(CIRCLE.point_is_on_circumference(POINT))

    def test_GivenCircleAndPointFarEnoughToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnFalse(self):
        CENTER = [1, 2]
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + 2. * epsilon_distance, 0], np.float_)
        self.assertFalse(CIRCLE.point_is_on_circumference(POINT))

class Test_get_circle(unittest.TestCase):

    def test_GivenNotExactly3Points_When_get_circle_ThenExceptionIsRaised(self):
        POINT = [1, 3]
        self.assertRaises(ValueError, get_circle, [POINT])
        self.assertRaises(ValueError, get_circle, [POINT, POINT])
        self.assertRaises(ValueError, get_circle, [POINT, POINT, POINT, POINT])

    def test_GivenAPointP_3x_When_get_circle_ThenExceptionIsRaised(self):
        POINT = [1, 3]
        POINTS = [POINT, POINT, POINT]
        self.assertRaises(ArithmeticError, get_circle, POINTS)

    def test_Given3CollinealPoints_When_get_circle_ThenExceptionIsRaised(self):
        DELTA = 1.5
        points = []
        for i in [1, 2, 3]:
            points.append([i*DELTA, 0])
        self.assertRaises(ArithmeticError, get_circle, points)

    def test_Given3ChosenPoints_When_get_circle_ThenReturnExpectedResult(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)

        points = []
        for angle in [30, 45, 60]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)])

        self.assertEqual(get_circle(points), CIRCLE)

class Test_get_MSE(unittest.TestCase):

    def test_GivenACircleAndZeroPoints_When_get_MSE_ThenExceptionIsRaised(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)
        self.assertRaises(ValueError, CIRCLE.get_MSE, ())

    def test_GivenACircleAndPointsOnCircumference_When_get_MSE_ThenReturn0(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)

        points = []
        for angle in [0, 90, 180, 270]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)])

        self.assertTrue(zero_in_practice(CIRCLE.get_MSE(points)))

    def test_GivenACircleAndPointsOn2xRadius_When_get_MSE_ThenReturnRadiusSquared(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)
        TWO_RADIUS = 2*RADIUS

        points = []
        for angle in [0, 90, 180, 270]:
            radians = math.radians(angle)
            points.append([CENTER[0] + TWO_RADIUS*math.cos(radians), CENTER[1] + TWO_RADIUS*math.sin(radians)])

        self.assertTrue(equal_in_practice(CIRCLE.get_MSE(points), RADIUS*RADIUS))

class Test_get_mean_signed_distance(unittest.TestCase):

    def test_GivenACircleAndZeroPoints_When_get_mean_signed_distance_ThenExceptionIsRaised(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)
        self.assertRaises(ValueError, CIRCLE.get_mean_signed_distance, ())

    def test_GivenACircleAndPointsOnCircumference_When_get_mean_signed_distance_ThenReturn0(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)

        points = []
        for angle in [0, 90, 180, 270]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)])

        self.assertTrue(zero_in_practice(CIRCLE.get_mean_signed_distance(points)))

    def test_GivenACircleAndPointsOn2xRadius_When_get_mean_signed_distance_ThenReturnRadius(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)
        TWO_RADIUS = 2*RADIUS

        points = []
        for angle in [0, 90, 180, 270]:
            radians = math.radians(angle)
            points.append([CENTER[0] + TWO_RADIUS*math.cos(radians), CENTER[1] + TWO_RADIUS*math.sin(radians)])

        self.assertTrue(equal_in_practice(CIRCLE.get_mean_signed_distance(points), RADIUS))

    def test_GivenACircleAndPointsOnHalfRadius_When_get_mean_signed_distance_ThenReturnMinusHalfRadius(self):
        CENTER = [2.7, -1.3]
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)
        HALF_RADIUS = .5*RADIUS

        points = []
        for angle in [0, 90, 180, 270]:
            radians = math.radians(angle)
            points.append([CENTER[0] + HALF_RADIUS*math.cos(radians), CENTER[1] + HALF_RADIUS*math.sin(radians)])

        self.assertTrue(equal_in_practice(CIRCLE.get_mean_signed_distance(points), -HALF_RADIUS))

class Test_get_best_fit_circle(unittest.TestCase):

    def test_GivenLessThan4Points_When_get_best_fit_circle_ThenExceptionIsRaised(self):
        POINT = [1, 3]
        X_CENTER = 0
        RADIUS = 3.4
        points = []
        for _ in range(3):
            points.append(POINT)
            self.assertRaises(ValueError, get_best_fit_circle, points, X_CENTER, RADIUS)

    def test_Given4PointsInTopOfCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        CENTER = [0, 0]
        RADIUS = 1
        CIRCLE = Circle(CENTER, RADIUS)
        X_CENTER = CENTER[0]

        points = []
        for angle in [30, 60, 120, 150]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)])

        RESULT = get_best_fit_circle(points, X_CENTER, RADIUS)
        self.assertEqual(CIRCLE, RESULT)

    def test_Given4PointsInBottomOfCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        CENTER = [0, 0]
        RADIUS = 1
        CIRCLE = Circle(CENTER, RADIUS)
        X_CENTER = CENTER[0]

        points = []
        for angle in [-30, -60, -120, -150]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)])

        RESULT = get_best_fit_circle(points, X_CENTER, RADIUS)
        self.assertEqual(CIRCLE, RESULT)

    def test_Given8PointAroundCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        CENTER = [0, 0]
        RADIUS = 1
        CIRCLE = Circle(CENTER, RADIUS)
        X_CENTER = CENTER[0]

        points = []
        for angle in [30, 60, 120, 150, -30, -60, -120, -150]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)])

        RESULT = get_best_fit_circle(points, X_CENTER, RADIUS)
        self.assertEqual(CIRCLE, RESULT)

    def test_Given8PointsAroundTopOfCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        CENTER = [3, 6]
        RADIUS = 1
        CIRCLE = Circle(CENTER, RADIUS)
        X_CENTER = CENTER[0]
        DELTA_Y = 0.001

        points = []
        for angle in [30, 60, 120, 150]:
            radians = math.radians(angle)
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians) + DELTA_Y])
            points.append([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians) - DELTA_Y])

        print "CIRCLE is", CIRCLE
        EPSILON = 1e-6
        for use_MSE in [True, False]:
            RESULT = get_best_fit_circle(points, X_CENTER, RADIUS, use_MSE)
            print "RESULT when use_MSE is", use_MSE, "is", RESULT
            self.assertTrue(equal_in_practice(CENTER[1], RESULT.get_center()[1], EPSILON))

if __name__ == '__main__':
    unittest.main()
