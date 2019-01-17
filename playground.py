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

    def spy(self, message):
        print "Sphere", message, \
            "\n  center =", self.center, \
            "\n  radius =", self.radius
        return

    def point_is_on_surface(self, point, epsilon_distance):
        distance = np.linalg.norm(self.center-point)
        return distance <= epsilon_distance

def get_sphere():
    """TODO: Input: 4 points"""
    sphere = Sphere(np.array([0, 0, 0], np.float_), 1.)
    return sphere

epsilon = 0.001

sphere_A = Sphere(np.array([1, 2, 3], np.float_), 7)
sphere_A.spy("sphere_A")

point = np.array([1, 2, 3], np.float_)
on_surface = sphere_A.point_is_on_surface(point, epsilon)
print "point", point, "on_surface?", on_surface

point = np.array([1, 2, 3.1], np.float_)
on_surface = sphere_A.point_is_on_surface(point, epsilon)
print "point", point, "on_surface?", on_surface

print

sphere_B = get_sphere()
sphere_B.spy("sphere_B (obtained with get_sphere)")

print "\nFinished."
