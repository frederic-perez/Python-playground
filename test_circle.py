"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_circle

or, for individual test classes:

  $ python -m unittest -v test_circle.Test_Circle
  $ python -m unittest -v test_circle.Test_equal_in_practice
  $ python -m unittest -v test_circle.Test_get_circle
  $ python -m unittest -v test_circle.Test_zero_in_practice
"""

import math
import numpy as np
import unittest
from circle import \
    Circle, get_circle, get_best_fit_circle, epsilon_distance, equal_in_practice, zero_in_practice

class Test_zero_in_practice(unittest.TestCase):

    def test_GivenAFloatVeryCloseToZero_When_zero_in_practice_ThenReturnTrue(self):
        F = epsilon_distance/2.
        self.assertTrue(zero_in_practice(F))
 
    def test_GivenAFarEnoughFromZero_When_zero_in_practice_ThenReturnFalse(self):
        F = 2.*epsilon_distance
        self.assertFalse(zero_in_practice(F))

class Test_equal_in_practice(unittest.TestCase):

    def test_GivenAFloat_When_test_equal_in_practice_ThenReturnTrue(self):
        F = 3.
        self.assertTrue(equal_in_practice(F, F))

    def test_GivenAFloatAndA2ndVeryClose_When_test_equal_in_practice_ThenReturnTrue(self):
        F_1 = 3.
        F_2 = F_1 + epsilon_distance/2.
        self.assertTrue(equal_in_practice(F_1, F_2))
 
    def test_GivenAFloatAndA2ndFarEnough_When_test_equal_in_practice_ThenReturnFalse(self):
        F_1 = 3.
        F_2 = F_1 + 2.*epsilon_distance
        self.assertFalse(equal_in_practice(F_1, F_2))

class Test_Circle(unittest.TestCase):

    def test_GivenAnEmptyCenter_When_Circle_ThenExceptionIsRaised(self):
        RADIUS = 3.
        self.assertRaises(TypeError, Circle, None, RADIUS)

    def test_GivenA1DCenterPoint_When_Circle_ThenExceptionIsRaised(self):
        CENTER_1D = np.array([1], np.float_)
        RADIUS = 3.
        self.assertRaises(TypeError, Circle, CENTER_1D, RADIUS)

    def test_GivenAMissingRadius_When_Circle_ThenExceptionIsRaised(self):
        CENTER = np.array([1, 3], np.float_)
        self.assertRaises(TypeError, Circle, CENTER)

    def test_GivenAZeroRadius_When_Circle_ThenExceptionIsRaised(self):
        CENTER = np.array([1, 3], np.float_)
        ZERO_RADIUS = 0
        self.assertRaises(ValueError, Circle, CENTER, ZERO_RADIUS)

    def test_GivenANegativeRadius_When_Circle_ThenExceptionIsRaised(self):
        CENTER = np.array([1, 3], np.float_)
        NEGATIVE_RADIUS = -7
        self.assertRaises(ValueError, Circle, CENTER, NEGATIVE_RADIUS)

    def test_Given2CirclesCreatedEqually_WhenComparision_ThenReturnTrue(self):
        CENTER = np.array([1, 3], np.float_)
        RADIUS = 3.
        self.assertEqual(Circle(CENTER, RADIUS), Circle(CENTER, RADIUS))
        CIRCLE = Circle(CENTER, RADIUS)
        self.assertEqual(CIRCLE, Circle(CENTER, RADIUS))

    def test_Given2CirclesCreatedNotEqually_WhenComparision_ThenReturnFalse(self):
        POINT_A = np.array([1, 3], np.float_)
        RADIUS = 3.
        self.assertNotEqual(Circle(POINT_A, RADIUS), Circle(POINT_A, RADIUS + 1.))
        POINT_B = np.array([4, 3], np.float_)
        self.assertNotEqual(Circle(POINT_A, RADIUS), Circle(POINT_B, RADIUS))

    def test_GivenCircleCreatedWithRadiusR_When_get_radius_ThenReturnR(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        # CIRCLE.spy("CIRCLE")
        self.assertEqual(CIRCLE.get_radius(), RADIUS)

    def test_GivenCircleCreatedWithCenterC_When_get_center_ThenReturnC(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        RETURNED_CENTER = CIRCLE.get_center()
        EQUAL_CENTERS = equal_in_practice(CENTER[0], RETURNED_CENTER[0]) \
            and equal_in_practice(CENTER[1], RETURNED_CENTER[1])
        self.assertTrue(EQUAL_CENTERS)

    def test_GivenCircleAndPointEqualToCenterPlusRadiusForY_When_get_signed_distance_to_circumference_ThenReturnZero(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 8
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([0, RADIUS], np.float_)
        self.assertTrue(zero_in_practice(CIRCLE.get_signed_distance_to_circumference(POINT)))

    def test_GivenCircleAndPointEqualToCenterPlus2RadiusForY_When_get_signed_distance_to_circumference_ThenReturnRadius(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 8
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([0, 2*RADIUS], np.float_)
        self.assertTrue(equal_in_practice(CIRCLE.get_signed_distance_to_circumference(POINT), RADIUS))

    def test_GivenCircleAndPointEqualToCenterPlusHalfRadiusForY_When_get_signed_distance_to_circumference_ThenReturnMinusHalfRadius(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 8
        HALF_RADIUS = RADIUS/2
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([0, HALF_RADIUS], np.float_)
        self.assertTrue(equal_in_practice(CIRCLE.get_signed_distance_to_circumference(POINT), -HALF_RADIUS))

    def test_GivenCircleAndPointEqualToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnTrue(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS, 0], np.float_)
        self.assertTrue(CIRCLE.point_is_on_circumference(POINT))

    def test_GivenCircleAndPointAlmostEqualToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnTrue(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + epsilon_distance/2., 0], np.float_)
        self.assertTrue(CIRCLE.point_is_on_circumference(POINT))

    def test_GivenCircleAndPointFarEnoughToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnFalse(self):
        CENTER = np.array([1, 2], np.float_)
        RADIUS = 7
        CIRCLE = Circle(CENTER, RADIUS)
        POINT = CENTER + np.array([RADIUS + 2. * epsilon_distance, 0], np.float_)
        self.assertFalse(CIRCLE.point_is_on_circumference(POINT))

class Test_get_circle(unittest.TestCase):

    def test_GivenNotExactly3Points_When_get_circle_ThenExceptionIsRaised(self):
        POINT = np.array([1, 3], np.float_)
        self.assertRaises(ValueError, get_circle, (POINT))
        self.assertRaises(ValueError, get_circle, (POINT, POINT))
        self.assertRaises(ValueError, get_circle, (POINT, POINT, POINT, POINT))

    def test_GivenAPointP_3x_When_get_circle_ThenExceptionIsRaised(self):
        POINT = np.array([1, 3], np.float_)
        POINTS = (POINT, POINT, POINT)
        self.assertRaises(ArithmeticError, get_circle, POINTS)

    def test_Given3CollinealPoints_When_get_circle_ThenExceptionIsRaised(self):
        DELTA = 1.5
        POINT_1 = np.array([1*DELTA, 0], np.float_)
        POINT_2 = np.array([2*DELTA, 0], np.float_)
        POINT_3 = np.array([3*DELTA, 0], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3)
        self.assertRaises(ArithmeticError, get_circle, POINTS)

    def test_Given3ChosenPoints_When_get_circle_ThenReturnExpectedResult(self):
        CENTER = np.array([2.7, -1.3], np.float_)
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)

        POINT_1 = np.array([CENTER[0] + RADIUS, CENTER[1]], np.float_)
        POINT_2 = np.array([CENTER[0],          CENTER[1] + RADIUS], np.float_)
        POINT_3 = np.array([CENTER[0] - RADIUS, CENTER[1]], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3)

        self.assertEqual(get_circle(POINTS), CIRCLE)

class Test_get_MSE(unittest.TestCase):

    def test_GivenACircleAndZeroPoints_When_get_MSE_ThenExceptionIsRaised(self):
        CENTER = np.array([2.7, -1.3], np.float_)
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)
        self.assertRaises(ValueError, CIRCLE.get_MSE, ())

    def test_GivenACircleAndPointsOnCircumference_When_get_MSE_ThenReturn0(self):
        CENTER = np.array([2.7, -1.3], np.float_)
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)

        POINT_1 = np.array([CENTER[0] + RADIUS, CENTER[1]], np.float_)
        POINT_2 = np.array([CENTER[0],          CENTER[1] + RADIUS], np.float_)
        POINT_3 = np.array([CENTER[0] - RADIUS, CENTER[1]], np.float_)
        POINT_4 = np.array([CENTER[0],          CENTER[1] - RADIUS], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)

        self.assertTrue(zero_in_practice(CIRCLE.get_MSE(POINTS)))

    def test_GivenACircleAndPointsOn2xRadius_When_get_MSE_ThenReturnRadiusSquared(self):
        CENTER = np.array([2.7, -1.3], np.float_)
        RADIUS = 3.4
        CIRCLE = Circle(CENTER, RADIUS)

        POINT_1 = np.array([CENTER[0] + 2*RADIUS, CENTER[1]], np.float_)
        POINT_2 = np.array([CENTER[0],            CENTER[1] + 2*RADIUS], np.float_)
        POINT_3 = np.array([CENTER[0] - 2*RADIUS, CENTER[1]], np.float_)
        POINT_4 = np.array([CENTER[0],            CENTER[1] - 2*RADIUS], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)

        self.assertTrue(equal_in_practice(CIRCLE.get_MSE(POINTS), RADIUS*RADIUS))

class Test_get_best_fit_circle(unittest.TestCase):

    def test_GivenLessThan4Points_When_get_best_fit_circle_ThenExceptionIsRaised(self):
        POINT = np.array([1, 3], np.float_)
        X_0 = 0
        RADIUS = 3.4
        self.assertRaises(ValueError, get_best_fit_circle, (POINT), X_0, RADIUS)
        self.assertRaises(ValueError, get_best_fit_circle, (POINT, POINT), X_0, RADIUS)
        self.assertRaises(ValueError, get_best_fit_circle, (POINT, POINT, POINT), X_0, RADIUS)

    def test_Given4PointsInCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        CENTER = np.array([0, 0], np.float_)
        RADIUS = 1
        CIRCLE = Circle(CENTER, RADIUS)
        X_0 = CENTER[0]

        radians = math.radians(30)
        POINT_1 = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        radians = math.radians(60)
        POINT_2 = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        radians = math.radians(90 + 30)
        POINT_3 = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        radians = math.radians(90 + 60)
        POINT_4 = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
        print "POINTS is", POINTS

        RESULT = get_best_fit_circle(POINTS, X_0, RADIUS)
        self.assertEqual(CIRCLE, RESULT)

    def test_Given8PointsAroundCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        CENTER = np.array([0, 0], np.float_)
        RADIUS = 1
        CIRCLE = Circle(CENTER, RADIUS)
        X_0 = CENTER[0]
        DELTA_Y = 0.1

        radians = math.radians(30)
        point = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        POINT_1_A = np.array([point[0], point[1] + DELTA_Y], np.float_)
        POINT_1_B = np.array([point[0], point[1] - DELTA_Y], np.float_)
        radians = math.radians(60)
        point = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        POINT_2_A = np.array([point[0], point[1] + DELTA_Y], np.float_)
        POINT_2_B = np.array([point[0], point[1] - DELTA_Y], np.float_)
        radians = math.radians(90 + 30)
        point = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        POINT_3_A = np.array([point[0], point[1] + DELTA_Y], np.float_)
        POINT_3_B = np.array([point[0], point[1] - DELTA_Y], np.float_)
        radians = math.radians(90 + 60)
        point = np.array([CENTER[0] + RADIUS*math.cos(radians), CENTER[1] + RADIUS*math.sin(radians)], np.float_)
        POINT_4_A = np.array([point[0], point[1] + DELTA_Y], np.float_)
        POINT_4_B = np.array([point[0], point[1] - DELTA_Y], np.float_)
        POINTS = (POINT_1_A, POINT_1_B, POINT_2_A, POINT_2_B, POINT_3_A, POINT_3_B, POINT_4_A, POINT_4_B)
        print "POINTS is", POINTS

        RESULT = get_best_fit_circle(POINTS, X_0, RADIUS)
        print "CIRCLE is", CIRCLE
        print "RESULT is", RESULT
        self.assertEqual(CIRCLE, RESULT)

if __name__ == '__main__':
    unittest.main()
