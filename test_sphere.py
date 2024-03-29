"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_sphere.py
  or
  $ python test_sphere.py

or, for individual test classes (sorted as appearing in this file):

  $ python -m unittest -v test_sphere.Test_Sphere
  $ python -m unittest -v test_sphere.Test_Sphere_get_mse
  $ python -m unittest -v test_sphere.Test_Sphere_get_mean_signed_distance
  $ python -m unittest -v test_sphere.Test_get_sphere
  $ python -m unittest -v test_sphere.Test_get_best_fit_sphere
  $ python -m unittest -v test_sphere.Test_get_best_fit_sphere_for_radius_range
"""

import math
import numpy as np
import unittest

from epsilon import epsilon_distance, equal_in_practice, zero_in_practice
from sphere import as_tuple_of_3_floats, get_sphere, get_best_fit_sphere, get_best_fit_sphere_for_radius_range, Sphere
from typing import Final, TypeAlias


class Test_Sphere(unittest.TestCase):

    def test_GivenAnEmptyCenter_When_Sphere_ThenExceptionIsRaised(self):
        radius: Final = 3.
        self.assertRaises(TypeError, Sphere, None, radius)

    def test_GivenA2DCenterPoint_When_Sphere_ThenExceptionIsRaised(self):
        center_2_d: Final = 1, 3
        radius: Final = 3.
        self.assertRaises(ValueError, Sphere, center_2_d, radius)

    def test_GivenAMissingRadius_When_Sphere_ThenExceptionIsRaised(self):
        center: Final = 1, 3, 6
        self.assertRaises(TypeError, Sphere, center)

    def test_GivenAZeroRadius_When_Sphere_ThenExceptionIsRaised(self):
        center: Final = 1, 3, 6
        zero_radius: Final = 0
        self.assertRaises(ValueError, Sphere, center, zero_radius)

    def test_GivenANegativeRadius_When_Sphere_ThenExceptionIsRaised(self):
        center: Final = 1, 3, 6
        negative_radius: Final = -7
        self.assertRaises(ValueError, Sphere, center, negative_radius)

    def test_Given2SpheresCreatedEqually_WhenComparison_ThenReturnTrue(self):
        center: Final = 1, 3, 6
        radius: Final = 3.
        self.assertEqual(Sphere(center, radius), Sphere(center, radius))
        sphere: Final = Sphere(center, radius)
        self.assertEqual(sphere, Sphere(center, radius))

    def test_Given2SpheresCreatedNotEqually_WhenComparison_ThenReturnFalse(self):
        center_a: Final = 1, 3, 6
        radius: Final = 3.
        self.assertNotEqual(Sphere(center_a, radius), Sphere(center_a, radius + 1.))
        center_b: Final = 4, 3, 3
        self.assertNotEqual(Sphere(center_a, radius), Sphere(center_b, radius))

    def test_GivenSphereCreatedWithRadiusR_When_get_radius_ThenReturnR(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        # sphere.spy("sphere")
        self.assertEqual(sphere.get_radius(), radius)

    def test_GivenCircleCreatedWithCenterC_When_get_center_ThenReturnC(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        returned_center: Final = sphere.get_center()
        equal_centers: Final = (equal_in_practice(center[0], returned_center[0])
                                and equal_in_practice(center[1], returned_center[1])
                                and equal_in_practice(center[2], returned_center[2]))
        self.assertTrue(equal_centers)

    def test_GivenSphereAndPointEqualToCenterPlusRadiusForZ_When_get_signed_distance_to_surface_ThenReturnZero(self):
        center: Final = 1, 2, 3
        radius: Final = 8
        sphere: Final = Sphere(center, radius)
        point: Final = as_tuple_of_3_floats(center + np.array([0, 0, radius]))
        self.assertTrue(zero_in_practice(sphere.get_signed_distance_to_surface(point)))

    def test_GivenSphereAndPointEqualToCenterPlus2RadiusForZ_When_get_signed_distance_to_surface_ThenReturnRadius(self):
        center: Final = 1, 2, 3
        radius: Final = 8
        sphere: Final = Sphere(center, radius)
        point: Final = as_tuple_of_3_floats(center + np.array([0, 0, 2*radius]))
        self.assertTrue(equal_in_practice(sphere.get_signed_distance_to_surface(point), radius))

    def test_GivenSphereAndPointEqualToCenterPlusHalfRadiusForZ_When_get_signed_distance_to_surface_ThenReturnMinusHalfRadius(self):
        center: Final = 1, 2, 3
        radius: Final = 8
        half_radius: Final = radius/2
        sphere: Final = Sphere(center, radius)
        point: Final = as_tuple_of_3_floats(center + np.array([0, 0, half_radius]))
        self.assertTrue(equal_in_practice(sphere.get_signed_distance_to_surface(point), -half_radius))

    def test_GivenSphereAndPointEqualToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnTrue(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        point: Final = as_tuple_of_3_floats(center + np.array([radius, 0, 0]))
        self.assertTrue(sphere.point_is_on_surface(point))

    def test_GivenSphereAndPointAlmostEqualToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnTrue(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        point: Final = as_tuple_of_3_floats(center + np.array([radius + epsilon_distance/2., 0, 0]))
        self.assertTrue(sphere.point_is_on_surface(point))

    def test_GivenSphereAndPointFarEnoughToCenterPlusRadiusForX_When_point_is_on_surface_ThenReturnFalse(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        point: Final = as_tuple_of_3_floats(center + np.array([radius + 2. * epsilon_distance, 0, 0]))
        self.assertFalse(sphere.point_is_on_surface(point))


TupleOf3Floats: TypeAlias = tuple[float, float, float]


def get_sample_points_on_the_surface(sphere: Sphere) -> list[TupleOf3Floats]:
    # https://en.wikipedia.org/wiki/List_of_common_coordinate_transformations#From_spherical_coordinates
    center: Final = sphere.get_center()
    radius: Final = sphere.get_radius()
    points: list[TupleOf3Floats] = []
    angles_in_degrees: Final = 0, 45, 90, 135, 180, 225, 270, 315
    for theta_in_degrees in angles_in_degrees:
        theta = math.radians(theta_in_degrees)
        for phi_in_degrees in angles_in_degrees:
            phi = math.radians(phi_in_degrees)
            points.append((
                center[0] + radius*math.sin(theta)*math.cos(phi),
                center[1] + radius*math.sin(theta)*math.sin(phi),
                center[2] + radius*math.cos(theta)))
    return points


class Test_Sphere_get_mse(unittest.TestCase):

    def test_GivenASphereAndZeroPoints_When_get_mse_ThenExceptionIsRaised(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        self.assertRaises(ValueError, sphere.get_mse, ())

    def test_GivenASphereAndPointsOnSurface_When_get_mse_ThenReturn0(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        points: Final = get_sample_points_on_the_surface(sphere)
        self.assertTrue(zero_in_practice(sphere.get_mse(points)))

    def test_GivenASphereAndPointsOn2xRadius_When_get_mse_ThenReturnRadiusSquared(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        two_radius: Final = 2*radius
        points: Final = get_sample_points_on_the_surface(Sphere(center, two_radius))
        self.assertTrue(equal_in_practice(sphere.get_mse(points), radius * radius))


class Test_Sphere_get_mean_signed_distance(unittest.TestCase):

    def test_GivenASphereAndZeroPoints_When_get_mean_signed_distance_ThenExceptionIsRaised(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        self.assertRaises(ValueError, sphere.get_mean_signed_distance, ())

    def test_GivenASphereAndPointsOnSurface_When_get_mean_signed_distance_ThenReturn0(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        points: Final = get_sample_points_on_the_surface(sphere)
        self.assertTrue(zero_in_practice(sphere.get_mean_signed_distance(points)))

    def test_GivenASphereAndPointsOn2xRadius_When_get_mean_signed_distance_ThenReturnRadius(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        two_radius: Final = 2*radius
        points: Final = get_sample_points_on_the_surface(Sphere(center, two_radius))
        self.assertTrue(equal_in_practice(sphere.get_mean_signed_distance(points), radius))

    def test_GivenASphereAndPointsOnHalfRadius_When_get_mean_signed_distance_ThenReturnMinusHalfRadius(self):
        center: Final = 1, 2, 3
        radius: Final = 7
        sphere: Final = Sphere(center, radius)
        half_radius: Final = .5*radius
        points: Final = get_sample_points_on_the_surface(Sphere(center, half_radius))
        self.assertTrue(equal_in_practice(sphere.get_mean_signed_distance(points), -half_radius))


class Test_get_sphere(unittest.TestCase):

    def test_GivenNotExactly4Points_When_get_sphere_ThenExceptionIsRaised(self):
        point: Final = 1, 3
        self.assertRaises(ValueError, get_sphere, [point])
        self.assertRaises(ValueError, get_sphere, [point, point])
        self.assertRaises(ValueError, get_sphere, [point, point, point])
        self.assertRaises(ValueError, get_sphere, [point, point, point, point, point])

    def test_GivenAPointP_4x_When_get_sphere_ThenExceptionIsRaised(self):
        point: Final = 1, 3, 6
        points: Final = point, point, point, point
        self.assertRaises(ArithmeticError, get_sphere, points)

    def test_Given4CollinearPoints_When_get_sphere_ThenExceptionIsRaised(self):
        delta = 1.5
        points: list[TupleOf3Floats] = []
        for i in 1, 2, 3, 4:
            points.append((i*delta, 0, 0))
        self.assertRaises(ArithmeticError, get_sphere, points)

    def test_Given4CoplanarPoints_When_get_sphere_ThenExceptionIsRaised(self):
        delta: Final = 1.5
        points: list[TupleOf3Floats] = []
        for i in 1., 2.:
            points.append((i*delta, i, 0.))
            points.append((i*delta, i + 1., 0.))
        self.assertRaises(ArithmeticError, get_sphere, points)

    def test_Given4PointsFrom_31_136_12_106_When_get_sphere_ThenReturnTheSitesResult(self):
        point_1: Final = -34.1186,  1.389,   8.5034
        point_2: Final = -34.3179,  1.3719, -29.432
        point_3: Final = -8.7948,  -0.1148, -10.462
        point_4: Final = -60.527,   5.8305, -10.423
        points: Final = point_1, point_2, point_3, point_4
        sphere_31_136_12_106 = get_sphere(points)

        center_from_site: Final = -21.942809924607257, 113.52343730620188, -10.579341367428881
        radius_from_site: Final = 114.39638504793206
        sphere_from_site: Final = Sphere(center_from_site, radius_from_site)

        self.assertEqual(sphere_31_136_12_106, sphere_from_site)

    def test_Given4PointsFrom_39_136_10_106_When_get_sphere_ThenReturnTheSitesResult(self):
        point_1: Final = -34.5737, 0.5015,  10.377
        point_2: Final = -34.4944, 0.4966, -22.06
        point_3: Final = -8.2244,  0.5713,  -5.6182
        point_4: Final = -60.996,  4.412,   -5.7822
        points: Final = point_1, point_2, point_3, point_4
        sphere_39_136_10_106 = get_sphere(points)

        center_from_site: Final = -26.681763623168056, 111.42322500511179, -5.8390596432420425
        radius_from_site: Final = 112.37825558460493
        sphere_from_site: Final = Sphere(center_from_site, radius_from_site)

        self.assertEqual(sphere_39_136_10_106, sphere_from_site)


class Test_get_best_fit_sphere(unittest.TestCase):

    def test_GivenLessThan5Points_When_get_best_fit_sphere_ThenExceptionIsRaised(self):
        point: Final = 1, 2, 3
        center_x_and_z: Final = 0, 0
        y_range: Final = 0, 500
        radius: Final = 3.4
        points: list[TupleOf3Floats] = []
        for _ in range(4):
            points.append(point)
            for use_mse in True, False:
                for num_samples in range(4, 10):
                    self.assertRaises(
                        ValueError, get_best_fit_sphere, points, center_x_and_z, y_range, radius, use_mse, num_samples)

    def test_Given4PointsInTopOfSphereS_When_get_best_fit_sphere_ThenResultIsS(self):
        center: Final = 0, 0, 0
        radius: Final = 3.4
        sphere: Final = Sphere(center, radius)
        center_x_and_z: Final = center[0], center[2]
        y_range: Final = -1, 3

        points: list[TupleOf3Floats] = []
        for theta_in_degrees in 30, 60:
            theta = math.radians(theta_in_degrees)
            for phi_in_degrees in 0, 45, 90, 135, 180, 225, 270, 315:
                phi = math.radians(phi_in_degrees)
                points.append((
                    center[0] + radius*math.sin(theta)*math.cos(phi),
                    center[1] + radius*math.cos(theta),
                    center[2] + radius*math.sin(theta)*math.sin(phi)))

        for use_mse in True, False:
            for num_samples in range(4, 10):
                result = get_best_fit_sphere(points, center_x_and_z, y_range, radius, use_mse, num_samples)
                another_epsilon_distance = 1e-5
                self.assertTrue(sphere.__eq__(result, another_epsilon_distance))

    def test_Given4PointsInBottomOfSphereS_When_get_best_fit_sphere_ThenResultIsS(self):
        center: Final = 0, 0, 0
        radius: Final = 3.4
        sphere: Final = Sphere(center, radius)
        center_x_and_z: Final = center[0], center[2]
        y_range: Final = -1, 10

        points: list[TupleOf3Floats] = []
        for theta_in_degrees in 120, 160:
            theta = math.radians(theta_in_degrees)
            for phi_in_degrees in 0, 45, 90, 135, 180, 225, 270, 315:
                phi = math.radians(phi_in_degrees)
                points.append((
                    center[0] + radius*math.sin(theta)*math.cos(phi),
                    center[1] + radius*math.cos(theta),
                    center[2] + radius*math.sin(theta)*math.sin(phi)))

        for use_mse in True, False:
            for num_samples in range(4, 10):
                result = get_best_fit_sphere(points, center_x_and_z, y_range, radius, use_mse, num_samples)
                another_epsilon_distance = 1e-5
                self.assertTrue(sphere.__eq__(result, another_epsilon_distance))

    def test_GivenNPointsAroundSphereS_When_get_best_fit_sphere_ThenResultIsS(self):
        center: Final = 0, 0, 0
        radius: Final = 3.4
        sphere: Final = Sphere(center, radius)
        center_x_and_z: Final = center[0], center[2]
        y_range: Final = -10, 20
        points: Final = get_sample_points_on_the_surface(sphere)
        for use_mse in True, False:
            for num_samples in range(4, 10):
                result = get_best_fit_sphere(points, center_x_and_z, y_range, radius, use_mse, num_samples)
                another_epsilon_distance = 1e-4
                self.assertTrue(sphere.__eq__(result, another_epsilon_distance))


class Test_get_best_fit_sphere_for_radius_range(unittest.TestCase):

    def test_GivenLessThan5Points_When_get_best_fit_sphere_for_radius_range_ThenExceptionIsRaised(self):
        point: Final = 1, 2, 3
        center_x_and_z: Final = 0, 0
        y_range: Final = 0, 500
        radius_range: Final = 3.1, 3.9
        points: list[TupleOf3Floats] = []
        for _ in range(4):
            points.append(point)
            for use_mse in True, False:
                for num_samples in range(4, 10):
                    self.assertRaises(ValueError, get_best_fit_sphere_for_radius_range, points, center_x_and_z, y_range,
                                      radius_range, use_mse, num_samples)


if __name__ == '__main__':
    unittest.main()
