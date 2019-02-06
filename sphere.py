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

class Sphere(object):
    def __init__(self, center, radius):
        if not hasattr(center, "__len__"):
            raise TypeError('center should be an array')
        if center.__len__() != 3:
            raise TypeError('center should be an array of 3 elements')
        if not radius:
            raise ValueError('radius should not be empty')
        self.center = center
        self.radius = radius
        return

    def __eq__(self, other):
        return \
            equal_in_practice(self.center[0], other.center[0]) \
            and equal_in_practice(self.center[1], other.center[1]) \
            and equal_in_practice(self.center[2], other.center[2]) \
            and equal_in_practice(self.radius, other.radius)

    def __str__(self):
        return 'Sphere(center={0}, radius={1})'.format(self.center, self.radius)

    def get_radius(self):
        return self.radius

    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

    def get_signed_distance_to_surface(self, point):
        return np.linalg.norm(self.center-point) - self.radius
  
    def point_is_on_surface(self, point):
        DISTANCE = self.get_signed_distance_to_surface(point)
        return zero_in_practice(DISTANCE)

def get_sphere(points):
    """
    Translation of code from http://www.convertalot.com/sphere_solver.html
    on December 21, 2018, and then simplified
    """
    assert len(points) == 4
    a = np.zeros((4, 4))
    for i in range(0, 4):
        a[i][0] = points[i][0]
        a[i][1] = points[i][1]
        a[i][2] = points[i][2]
        a[i][3] = 1
    MINOR_11 = np.linalg.det(a)
    if (zero_in_practice(MINOR_11)):
        raise ArithmeticError('It is impossible to divide by zero')

    for i in range(0, 4):
        a[i][0] = points[i][0]**2 + points[i][1]**2 + points[i][2]**2
    MINOR_12 = np.linalg.det(a)

    for i in range(0, 4):
        a[i][1] = points[i][0]
    MINOR_13 = np.linalg.det(a)

    for i in range(0, 4):
        a[i][2] = points[i][1]
    MINOR_14 = np.linalg.det(a)

    for i in range(0, 4):
        a[i][3] = points[i][2]
    MINOR_15 = np.linalg.det(a)

    X = .5 * MINOR_12 / MINOR_11
    Y = -.5 * MINOR_13 / MINOR_11
    Z = .5 * MINOR_14 / MINOR_11
    CENTER = np.array([X, Y, Z], np.float_)
    RADIUS = math.sqrt(X*X + Y*Y + Z*Z - MINOR_15/MINOR_11)
    return Sphere(CENTER, RADIUS)
