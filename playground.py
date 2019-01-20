'module docstring should be here'

import math
import numpy as np

def average(*numbers):
    """Self-explanatory"""
    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))

assert average(1) == 1
assert average(math.pi) == math.pi
assert average(1, 2) == 1.5

assert np.linalg.det(np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])) == 1

"""
TODO
class Point (?). Perhaps in numpy? In scipy?
"""

class Sphere(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        return

    def get_radius(self):
        return self.radius

    def spy(self, message):
        print "Sphere", message, \
            "\n  center =", self.center, \
            "\n  radius =", self.radius
        return

    def point_is_on_surface(self, point, epsilon_distance):
        distance = np.linalg.norm(self.center-point) - self.radius
        return abs(distance) <= epsilon_distance

def get_sphere(points):
    """
    Translation from code retrieved from
    http://www.convertalot.com/sphere_solver.html
    on December 21, 2018
    """
    assert len(points) == 4
    a = np.zeros((4, 4))
    for i in range(0, 4):
        a[i][0] = points[i][0]
        a[i][1] = points[i][1]
        a[i][2] = points[i][2]
        a[i][3] = 1
    minor_11 = np.linalg.det(a)
    if (minor_11 == 0):
        return Sphere(np.array([0, 0, 0], np.float_), 0.)

    for i in range(0, 4):
        a[i][0] = points[i][0]**2 + points[i][1]**2 + points[i][2]**2

    for i in range(0, 4):
        a[i][1] = points[i][1]
        a[i][2] = points[i][2]
        a[i][3] = 1
    minor_12 = np.linalg.det(a)
    
    for i in range(0, 4):
        a[i][1] = points[i][0]
        a[i][2] = points[i][2]
        a[i][3] = 1
    minor_13 = np.linalg.det(a)
    
    for i in range(0, 4):
        a[i][1] = points[i][0]
        a[i][2] = points[i][1]
        a[i][3] = 1
    minor_14 = np.linalg.det(a)
    
    for i in range(0, 4):
        a[i][1] = points[i][0]
        a[i][2] = points[i][1]
        a[i][3] = points[i][2]
    minor_15 = np.linalg.det(a)
    
    x = .5 * minor_12 / minor_11
    y = -.5 * minor_13 / minor_11
    z = .5 * minor_14 / minor_11
    r = math.sqrt(x*x + y*y + z*z - minor_15/minor_11)
    return Sphere(np.array([x, y, z], np.float_), r)

point_A = np.array([1, 3, 6], np.float_)
point_B = np.array([1, 3, 0], np.float_)
point_C = np.array([1, 6, 3], np.float_)
point_D = np.array([1, 0, 0], np.float_)
center_ABCD = np.array([1, 3, 3], np.float_)
radius_ABCD = 3.

assert Sphere(point_A, 3.) == Sphere(point_A, 3.)
assert Sphere(point_A, 3.) != Sphere(point_B, 3.)
assert Sphere(point_A, 3.) == Sphere(point_A, 4.)

assert get_sphere((point_A, point_A, point_A, point_A)).get_radius() == 0.
assert get_sphere((point_A, point_B, point_C, point_D)) == Sphere(center_ABCD, radius_ABCD)

epsilon = 0.001

sphere_A = Sphere(np.array([1, 2, 3], np.float_), 7)
sphere_A.spy("sphere_A")

point = np.array([8, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point, epsilon)
print "point", point, "on_surface?", on_surface

point = np.array([8.01, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point, epsilon)
print "point", point, "on_surface?", on_surface

point = np.array([7.99, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point, epsilon)
print "point", point, "on_surface?", on_surface

point = np.array([7.99999, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point, epsilon)
print "point", point, "on_surface?", on_surface

print

point_1 = np.array([1, 2, 3], np.float_)
point_2 = np.array([1, 2, 3], np.float_)
point_3 = np.array([1, 2, 3], np.float_)
point_4 = np.array([1, 2, 3], np.float_)
points = (point_1, point_2, point_3, point_4)
sphere_B = get_sphere(points)
sphere_B.spy("sphere_B (obtained with get_sphere)")

print "\nFinished."
