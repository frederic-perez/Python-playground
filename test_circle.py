"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_circle.py
  or
  $ python test_circle.py

or, for individual test classes (sorted as appearing in this file):

  $ python -m unittest -v test_circle.Test_Circle
  $ python -m unittest -v test_circle.Test_Circle_get_mean_signed_distance
  $ python -m unittest -v test_circle.Test_Circle_get_mse
  $ python -m unittest -v test_circle.Test_get_best_fit_circle
  $ python -m unittest -v test_circle.Test_get_circle
"""

import math
import numpy as np
import unittest
from circle import Circle, get_circle, get_best_fit_circle
from epsilon import epsilon_distance, equal_in_practice, zero_in_practice


class Test_Circle(unittest.TestCase):

    def test_GivenAnEmptyCenter_When_Circle_ThenExceptionIsRaised(self):
        radius = 3.
        self.assertRaises(TypeError, Circle, center=None, radius=radius)

    def test_GivenA1DCenterPoint_When_Circle_ThenExceptionIsRaised(self):
        center_1_d = (1,)
        radius = 3.
        self.assertRaises(ValueError, Circle, center=center_1_d, radius=radius)

    def test_GivenAMissingRadius_When_Circle_ThenExceptionIsRaised(self):
        center = (1, 3)
        self.assertRaises(TypeError, Circle, center=center)

    def test_GivenAZeroRadius_When_Circle_ThenExceptionIsRaised(self):
        center = (1, 3)
        zero_radius = 0
        self.assertRaises(ValueError, Circle, center, zero_radius)

    def test_GivenANegativeRadius_When_Circle_ThenExceptionIsRaised(self):
        center = (1, 3)
        negative_radius = -7
        self.assertRaises(ValueError, Circle, center, negative_radius)

    def test_Given2CirclesCreatedEqually_WhenComparison_ThenReturnTrue(self):
        center = (1, 3)
        radius = 3.
        self.assertEqual(Circle(center, radius), Circle(center, radius))
        circle = Circle(center, radius)
        self.assertEqual(circle, Circle(center, radius))

    def test_Given2CirclesCreatedNotEqually_WhenComparison_ThenReturnFalse(self):
        center_a = (1, 3)
        radius = 3.
        self.assertNotEqual(Circle(center_a, radius), Circle(center_a, radius + 1.))
        center_b = (4, 3)
        self.assertNotEqual(Circle(center_a, radius), Circle(center_b, radius))

    def test_GivenCircleCreatedWithRadiusR_When_get_radius_ThenReturnR(self):
        center = (1, 2)
        radius = 7
        circle = Circle(center, radius)
        # circle.spy("circle")
        self.assertEqual(circle.get_radius(), radius)

    def test_GivenCircleCreatedWithCenterC_When_get_center_ThenReturnC(self):
        center = (1, 2)
        radius = 7
        circle = Circle(center, radius)
        returned_center = circle.get_center()
        equal_centers = equal_in_practice(center[0], returned_center[0]) \
            and equal_in_practice(center[1], returned_center[1])
        self.assertTrue(equal_centers)

    def test_GivenCircleAndPointEqualToCenterPlusRadiusForY_When_get_signed_distance_to_circumference_ThenReturnZero(
            self):
        center = (1, 2)
        radius = 8
        circle = Circle(center, radius)
        point = center + np.array([0, radius])
        self.assertTrue(zero_in_practice(circle.get_signed_distance_to_circumference(point)))

    def test_GivenCircleAndPointEqualToCenterPlus2RadiusForY_When_get_signed_distance_to_circumference_ThenReturnRadius(
            self):
        center = (1, 2)
        radius = 8
        circle = Circle(center, radius)
        point = center + np.array([0, 2*radius])
        self.assertTrue(equal_in_practice(circle.get_signed_distance_to_circumference(point), radius))

    def test_GivenCircleAndPointEqualToCenterPlusHalfRadiusForY_When_get_signed_distance_to_circumference_ThenReturnMinusHalfRadius(self):
        center = (1, 2)
        radius = 8
        half_radius = radius/2
        circle = Circle(center, radius)
        point = center + np.array([0, half_radius])
        self.assertTrue(equal_in_practice(circle.get_signed_distance_to_circumference(point), -half_radius))

    def test_GivenCircleAndPointEqualToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnTrue(self):
        center = (1, 2)
        radius = 7
        circle = Circle(center, radius)
        point = center + np.array([radius, 0], np.float_)
        self.assertTrue(circle.point_is_on_circumference(point))

    def test_GivenCircleAndPointAlmostEqualToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnTrue(self):
        center = (1, 2)
        radius = 7
        circle = Circle(center, radius)
        point = center + np.array([radius + epsilon_distance/2., 0], np.float_)
        self.assertTrue(circle.point_is_on_circumference(point))

    def test_GivenCircleAndPointFarEnoughToCenterPlusRadiusForX_When_point_is_on_circumference_ThenReturnFalse(self):
        center = (1, 2)
        radius = 7
        circle = Circle(center, radius)
        point = center + np.array([radius + 2. * epsilon_distance, 0], np.float_)
        self.assertFalse(circle.point_is_on_circumference(point))


def get_sample_points_on_the_circumference(circle):
    center = circle.get_center()
    radius = circle.get_radius()
    points = []
    angles_in_degrees = (0, 45, 90, 135, 180, 225, 270, 315)
    for phi_in_degrees in angles_in_degrees:
        phi = math.radians(phi_in_degrees)
        points.append([
            center[0] + radius*math.cos(phi),
            center[1] + radius*math.sin(phi)])
    return points


class Test_Circle_get_mse(unittest.TestCase):

    def test_GivenACircleAndZeroPoints_When_get_mse_ThenExceptionIsRaised(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        self.assertRaises(ValueError, circle.get_mse, ())

    def test_GivenACircleAndPointsOnCircumference_When_get_mse_ThenReturn0(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        points = get_sample_points_on_the_circumference(circle)
        self.assertTrue(zero_in_practice(circle.get_mse(points)))

    def test_GivenACircleAndPointsOn2xRadius_When_get_mse_ThenReturnRadiusSquared(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        two_radius = 2*radius
        points = get_sample_points_on_the_circumference(Circle(center, two_radius))
        self.assertTrue(equal_in_practice(circle.get_mse(points), radius * radius))


class Test_Circle_get_mean_signed_distance(unittest.TestCase):

    def test_GivenACircleAndZeroPoints_When_get_mean_signed_distance_ThenExceptionIsRaised(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        self.assertRaises(ValueError, circle.get_mean_signed_distance, ())

    def test_GivenACircleAndPointsOnCircumference_When_get_mean_signed_distance_ThenReturn0(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        points = get_sample_points_on_the_circumference(circle)
        self.assertTrue(zero_in_practice(circle.get_mean_signed_distance(points)))

    def test_GivenACircleAndPointsOn2xRadius_When_get_mean_signed_distance_ThenReturnRadius(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        two_radius = 2*radius
        points = get_sample_points_on_the_circumference(Circle(center, two_radius))
        self.assertTrue(equal_in_practice(circle.get_mean_signed_distance(points), radius))

    def test_GivenACircleAndPointsOnHalfRadius_When_get_mean_signed_distance_ThenReturnMinusHalfRadius(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)
        half_radius = .5*radius
        points = get_sample_points_on_the_circumference(Circle(center, half_radius))
        self.assertTrue(equal_in_practice(circle.get_mean_signed_distance(points), -half_radius))


class Test_get_circle(unittest.TestCase):

    def test_GivenNotExactly3Points_When_get_circle_ThenExceptionIsRaised(self):
        point = [1, 3]
        self.assertRaises(ValueError, get_circle, [point])
        self.assertRaises(ValueError, get_circle, [point, point])
        self.assertRaises(ValueError, get_circle, [point, point, point, point])

    def test_GivenAPointP_3x_When_get_circle_ThenExceptionIsRaised(self):
        point = [1, 3]
        points = [point, point, point]
        self.assertRaises(ArithmeticError, get_circle, points)

    def test_Given3CollinearPoints_When_get_circle_ThenExceptionIsRaised(self):
        delta = 1.5
        points = []
        for i in [1, 2, 3]:
            points.append([i*delta, 0])
        self.assertRaises(ArithmeticError, get_circle, points)

    def test_Given3ChosenPoints_When_get_circle_ThenReturnExpectedResult(self):
        center = (2.7, -1.3)
        radius = 3.4
        circle = Circle(center, radius)

        points = []
        for angle in [30, 45, 60]:
            radians = math.radians(angle)
            points.append([center[0] + radius*math.cos(radians), center[1] + radius*math.sin(radians)])

        self.assertEqual(get_circle(points), circle)


class Test_get_best_fit_circle(unittest.TestCase):

    def test_GivenLessThan4Points_When_get_best_fit_circle_ThenExceptionIsRaised(self):
        point = [1, 3]
        x_center = 0
        radius = 3.4
        points = []
        for _ in range(3):
            points.append(point)
            for use_mse in [True, False]:
                for num_samples in range(4, 10):
                    self.assertRaises(ValueError, get_best_fit_circle, points, x_center, radius, use_mse, num_samples)

    def test_Given4PointsInTopOfCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        center = (0, 0)
        radius = 1
        circle = Circle(center, radius)
        x_center = center[0]

        points = []
        for angle in (30, 60, 120, 150):
            radians = math.radians(angle)
            points.append([center[0] + radius*math.cos(radians), center[1] + radius*math.sin(radians)])

        for use_mse in (True, False):
            for num_samples in range(4, 10):
                result = get_best_fit_circle(points, x_center, radius, use_mse, num_samples)
                self.assertEqual(circle, result)

    def test_Given4PointsInBottomOfCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        center = (0, 0)
        radius = 1
        circle = Circle(center, radius)
        x_center = center[0]

        points = []
        for angle in (-30, -60, -120, -150):
            radians = math.radians(angle)
            points.append([center[0] + radius*math.cos(radians), center[1] + radius*math.sin(radians)])

        for use_mse in (True, False):
            for num_samples in range(4, 10):
                result = get_best_fit_circle(points, x_center, radius, use_mse, num_samples)
                self.assertEqual(circle, result)

    def test_Given8PointsAroundCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        center = (0, 0)
        radius = 1
        circle = Circle(center, radius)
        x_center = center[0]

        points = []
        for angle in (30, 60, 120, 150, -30, -60, -120, -150):
            radians = math.radians(angle)
            points.append([center[0] + radius*math.cos(radians), center[1] + radius*math.sin(radians)])

        for use_mse in [True, False]:
            for num_samples in range(4, 10):
                result = get_best_fit_circle(points, x_center, radius, use_mse, num_samples)
                epsilon = 1e-5
                self.assertTrue(circle.__eq__(result, epsilon))

    def test_Given8PointsAroundTopOfCircleC_When_get_best_fit_circle_ThenResultIsC(self):
        center = (3, 6)
        radius = 1
        circle = Circle(center, radius)
        x_center = center[0]
        delta_y = 0.001

        points = []
        for angle in (5, 60, 120, 185):
            radians = math.radians(angle)
            points.append([center[0] + radius*math.cos(radians), center[1] + radius*math.sin(radians) + delta_y])
            points.append([center[0] + radius*math.cos(radians), center[1] + radius*math.sin(radians) - delta_y])

        for use_mse in (True, False):
            for num_samples in range(8, 10):
                result = get_best_fit_circle(points, x_center, radius, use_mse, num_samples)
                epsilon = 1e-6
                self.assertTrue(circle.__eq__(result, epsilon))


if __name__ == '__main__':
    unittest.main()
