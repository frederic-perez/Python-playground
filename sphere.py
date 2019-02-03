'module docstring should be here'

import math
import numpy as np

"""
TODO
class Point (?). Perhaps in numpy? In scipy?
"""

epsilon_distance = 1e-12

class Sphere(object):
    def __init__(self, center, radius):
        if not center:
            raise ValueError('center should not be empty')
        if not radius:
            raise ValueError('radius should not be empty')
        self.center = center
        self.radius = radius
        return

    def __eq__(self, other):
        return \
            abs(self.center[0] - other.center[0]) < epsilon_distance \
            and abs(self.center[1] - other.center[1]) < epsilon_distance \
            and abs(self.center[2] - other.center[2]) < epsilon_distance \
            and abs(self.radius - other.radius) < epsilon_distance

    def __str__(self):
        return 'Sphere(center={0}, radius={1})'.format(self.center, self.radius)

    def get_radius(self):
        return self.radius

    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

    def point_is_on_surface(self, point):
        DISTANCE = np.linalg.norm(self.center-point) - self.radius
        return abs(DISTANCE) <= epsilon_distance

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
    if (MINOR_11 == 0):
        return Sphere(np.array([0, 0, 0], np.float_), 0.)

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
