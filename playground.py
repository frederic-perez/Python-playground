'module docstring should be here'

import math

from numpy import matrix
from numpy import linalg

def average(*numbers):
    """Self-explanatory"""
    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))

assert average(1) == 1
assert average(math.pi) == math.pi
assert average(1, 2) == 1.5

assert linalg.det(matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])) == 1

"""
TODO
class Point (?). Perhaps in numpy? In scipy?
"""

class Sphere(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def spy(self, message):
        print "Sphere", message, \
            "\n  center =", self.center, \
            "\n  radius =", self.radius

    def point_is_on_surface(self, point, epsilon_distance):
        """TODO"""
        return False

def get_sphere():
    """TODO: Input: 4 points"""
    sphere = Sphere((0, 0, 0), 0)
    return sphere

sphere_A = Sphere((1, 2, 3), 7)
sphere_A.spy("sphere_A")

sphere_B = get_sphere()
sphere_B.spy("sphere_B")


print "\nFinished."
