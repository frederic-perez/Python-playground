"""
Run the tests by executing:
$ python -m unittest -v test_sphere
"""

import math
import numpy as np
import unittest
from sphere import Sphere, get_sphere

class Test_Sphere(unittest.TestCase):

    def test_WHEN_setting_two_spheres_with_the_same_parameters_WHEN_comparing_them_THEN_result_is_true(self):
        point_A = np.array([1, 3, 6], np.float_)
        point_B = np.array([4, 3, 3], np.float_)
        point_C = np.array([1, 6, 3], np.float_)
        point_D = np.array([1, 0, 3], np.float_)
        self.assertEqual(Sphere(point_A, 3.), Sphere(point_A, 3.))
        sphere = Sphere(point_A, 3.)
        self.assertEqual(sphere, Sphere(point_A, 3.))

    def test_WHEN_setting_two_spheres_with_different_parameters_WHEN_comparing_them_THEN_result_is_false(self):
        point_A = np.array([1, 3, 6], np.float_)
        point_B = np.array([4, 3, 3], np.float_)
        point_C = np.array([1, 6, 3], np.float_)
        point_D = np.array([1, 0, 3], np.float_)
        self.assertNotEqual(Sphere(point_A, 3.), Sphere(point_B, 3.))
        self.assertNotEqual(Sphere(point_A, 3.), Sphere(point_A, 4.))

    def test_WHEN_setting_a_sphere_with_a_given_radius_R_WHEN_calling_get_radius_THEN_result_is_R(self):
        radius = 7
        sphere_A = Sphere(np.array([1, 2, 3], np.float_), radius)
        sphere_A.spy("sphere_A")
        self.assertEqual(sphere_A.get_radius(), radius)

class Test_get_sphere(unittest.TestCase):

    def test_WHEN_calling_get_sphere_with_a_wrong_sphere_WHEN_calling_get_sphere_THEN_its_radius_must_be_0(self):
        point_A = np.array([1, 3, 6], np.float_)
        self.assertEqual(get_sphere((point_A, point_A, point_A, point_A)).get_radius(), 0.)

    def test_WHEN_calling_get_sphere_with_31_136_12_106_data_THEN_result_must_be_equal_to_that_of_the_original_site(self):
        point_1 = np.array([-34.1186,  1.389,   8.5034], np.float_)
        point_2 = np.array([-34.3179,  1.3719, -29.432], np.float_)
        point_3 = np.array([-8.7948,  -0.1148, -10.462], np.float_)
        point_4 = np.array([-60.527,   5.8305, -10.423], np.float_)
        points = (point_1, point_2, point_3, point_4)
        sphere_31_136_12_106 = get_sphere(points)
        sphere_31_136_12_106.spy("sphere_31_136_12_106 (obtained with get_sphere)")
        center_31_136_12_106 = np.array([-21.9428099,113.523437, -10.5793414], np.float_)
        radius_31_136_12_106 = 114.39638
        self.assertEqual(sphere_31_136_12_106, Sphere(center_31_136_12_106, radius_31_136_12_106))

    def test_WHEN_calling_get_sphere_with_39_136_10_106_data_THEN_result_must_be_equal_to_that_of_the_original_site(self):
        point_1 = np.array([-34.5737, 0.5015,  10.377], np.float_)
        point_2 = np.array([-34.4944, 0.4966, -22.06], np.float_)
        point_3 = np.array([-8.2244,  0.5713,  -5.6182], np.float_)
        point_4 = np.array([-60.996,  4.412,   -5.7822], np.float_)
        points = (point_1, point_2, point_3, point_4)
        sphere_39_136_10_106 = get_sphere(points)
        sphere_39_136_10_106.spy("sphere_39_136_10_106 (obtained with get_sphere)")
        center_39_136_10_106 = np.array([-26.6817636, 111.423225, -5.83905964], np.float_)
        radius_39_136_10_106 = 112.378256
        self.assertEqual(sphere_39_136_10_106, Sphere(center_39_136_10_106, radius_39_136_10_106))

sphere_A = Sphere(np.array([1, 2, 3], np.float_), 7)

point = np.array([8, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point)
print "point", point, "on_surface?", on_surface

point = np.array([8.01, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point)
print "point", point, "on_surface?", on_surface

point = np.array([7.99, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point)
print "point", point, "on_surface?", on_surface

point = np.array([7.99999, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point)
print "point", point, "on_surface?", on_surface

print "\n"

if __name__ == '__main__':
    unittest.main()
