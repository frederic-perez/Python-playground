'module docstring should be here'

import math
import numpy as np

"""
TODO
class Point (?). Perhaps in numpy? In scipy?
"""

epsilon_distance = 1e-12

def zero_in_practice(float):
    return abs(float) <= epsilon_distance

def equal_in_practice(float_1, float_2):
    return abs(float_1 - float_2) <= epsilon_distance

class Circle(object):
    def __init__(self, center, radius):
        if not hasattr(center, "__len__"):
            raise TypeError('center should be an array')
        if center.__len__() != 2:
            raise TypeError('center should be an array of 2 elements')
        if radius <= 0:
            raise ValueError("Value %g is out of range" % radius)
        self.center = center
        self.radius = radius
        return

    def __eq__(self, other):
        return \
            equal_in_practice(self.center[0], other.center[0]) \
            and equal_in_practice(self.center[1], other.center[1]) \
            and equal_in_practice(self.radius, other.radius)

    def __str__(self):
        return 'Circle(center={0}, radius={1})'.format(self.center, self.radius)

    def get_radius(self):
        return self.radius

    def get_center(self):
        return self.center
  
    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

    def get_signed_distance_to_circumference(self, point):
        return np.linalg.norm(self.center-point) - self.radius
  
    def point_is_on_circumference(self, point):
        DISTANCE = self.get_signed_distance_to_circumference(point)
        return zero_in_practice(DISTANCE)

def get_circle(points):
    """
    Code adapted from https://stackoverflow.com/questions/52990094
    on February 18, 2019
    """
    assert len(points) == 3

    a = np.zeros((3, 3))
    for i in range(0, 3):
        a[i][0] = points[i][0]
        a[i][1] = points[i][1]
        a[i][2] = 1
    DETERMINANT = np.linalg.det(a)
    if (zero_in_practice(DETERMINANT)):
        raise ArithmeticError('It is impossible to divide by zero')

    temp = points[1][0]**2 + points[1][1]**2
    bc = (points[0][0]**2 + points[0][1]**2 - temp) / 2
    cd = (temp - points[2][0]**2 - points[2][1]**2) / 2

    # Center of circle
    X = (bc*(points[1][1] - points[2][1]) - cd*(points[0][1] - points[1][1])) / DETERMINANT
    Y = ((points[0][0] - points[1][0]) * cd - (points[1][0] - points[2][0]) * bc) / DETERMINANT

    CENTER = np.array([X, Y], np.float_)
    RADIUS = math.sqrt((X - points[0][0])**2 + (Y - points[0][1])**2)

    return Circle(CENTER, RADIUS)
