'module docstring should be here'

import numpy as np
from sphere import Sphere, get_sphere

sphere_A = Sphere(np.array([1, 2, 3], np.float_), 7)
sphere_A.spy("sphere_A")

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

print

point_1 = np.array([-34.1186,  1.389,   8.5034], np.float_)
point_2 = np.array([-34.3179,  1.3719, -29.432], np.float_)
point_3 = np.array([-8.7948,  -0.1148, -10.462], np.float_)
point_4 = np.array([-60.527,   5.8305, -10.423], np.float_)
points = (point_1, point_2, point_3, point_4)
sphere_31_136_12_106 = get_sphere(points)
sphere_31_136_12_106.spy("sphere_31_136_12_106 (obtained with get_sphere)")
center_31_136_12_106 = np.array([-21.9428099,113.523437, -10.5793414], np.float_)
radius_31_136_12_106 = 114.39638
assert sphere_31_136_12_106 == Sphere(center_31_136_12_106, radius_31_136_12_106)

point_1 = np.array([-34.5737, 0.5015,  10.377], np.float_)
point_2 = np.array([-34.4944, 0.4966, -22.06], np.float_)
point_3 = np.array([-8.2244,  0.5713,  -5.6182], np.float_)
point_4 = np.array([-60.996,  4.412,   -5.7822], np.float_)
points = (point_1, point_2, point_3, point_4)
sphere_39_136_10_106 = get_sphere(points)
sphere_39_136_10_106.spy("sphere_39_136_10_106 (obtained with get_sphere)")
center_39_136_10_106 = np.array([-26.6817636, 111.423225, -5.83905964], np.float_)
radius_39_136_10_106 = 112.378256
assert sphere_39_136_10_106 == Sphere(center_39_136_10_106, radius_39_136_10_106)

print "\nFinished."
