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

    def get_MSE(self, points):
        if not hasattr(points, "__len__"):
            raise TypeError('points should be an array')

        NUM_POINTS = len(points)
        if NUM_POINTS < 1:
            raise ValueError('points should not be empty')

        acc_squared_error = 0
        for point in points:
            error = self.get_signed_distance_to_circumference(point)
            squared_error = error*error
            acc_squared_error += squared_error
        return acc_squared_error / NUM_POINTS

def get_circle(points):
    """
    Code adapted from https://stackoverflow.com/questions/52990094
    on February 18, 2019
    """
    if len(points) != 3:
        raise ValueError('3 points are required')

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

def get_best_fit_circle(points, x_0, radius):
    if not hasattr(points, "__len__"):
        raise TypeError('points should be an array')

    NUM_POINTS = len(points)
    if NUM_POINTS <= 3:
        raise ValueError('points should have at least 4 elements')

    y_min = float("inf")
    y_max = -float("inf")
    print "y_min initial is", y_min
    print "y_max initial is", y_max
    RADIUS_SQR = radius * radius

    for point in points:
        print "point is", point
        DISCRIMINANT = RADIUS_SQR - math.pow(x_0 - point[0], 2)
        SQR_DISCRIMINANT = math.sqrt(DISCRIMINANT)
        CURRENT_POSSIBLE_Y_MIN = point[1] - SQR_DISCRIMINANT
        CURRENT_POSSIBLE_Y_MAX = point[1] + SQR_DISCRIMINANT
        print "CURRENT_POSSIBLE_Y_MIN is", CURRENT_POSSIBLE_Y_MIN
        print "CURRENT_POSSIBLE_Y_MAX is", CURRENT_POSSIBLE_Y_MAX
        if y_min > CURRENT_POSSIBLE_Y_MIN:
            y_min = CURRENT_POSSIBLE_Y_MIN
        if y_max < CURRENT_POSSIBLE_Y_MAX:
            y_max = CURRENT_POSSIBLE_Y_MAX

    print 'y_min is', y_min
    print 'y_max is', y_max

    bottom_circle = Circle((x_0, y_min), radius)
    mse_for_bottom_circle = bottom_circle.get_MSE(points)
    print 'mse_for_bottom_circle is', mse_for_bottom_circle
    if zero_in_practice(mse_for_bottom_circle):
        return bottom_circle

    top_circle = Circle((x_0, y_max), radius)
    mse_for_top_circle = top_circle.get_MSE(points)
    print 'mse_for_top_circle is', mse_for_top_circle

    done = False
    i = 0
    while not done:
        y_middle = y_min + (y_max - y_min)/2
        mse_for_middle_circle = Circle((x_0, y_middle), radius).get_MSE(points)
        print "iteration #", i, "| y_middle is", y_middle, 'and mse_for_middle_circle is', mse_for_middle_circle

        done = mse_for_middle_circle < epsilon_distance
        if not done:
            if mse_for_top_circle > mse_for_bottom_circle: # reset top
                print "resetting top"
                y_max = y_middle
                mse_for_top_circle = mse_for_middle_circle
            else: # reset bottom
                print "resetting bottom"
                y_min = y_middle
                mse_for_bottom_circle = mse_for_middle_circle 
        i = i + 1
        done = i == 20

    return Circle((x_0, y_middle), radius)