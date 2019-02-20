'module docstring should be here'

import math
import numpy as np

"""
TODO
class Point (?). Perhaps in numpy? In scipy?
"""

epsilon_distance = 1e-12

def zero_in_practice(float, epsilon = epsilon_distance):
    return abs(float) <= epsilon

def equal_in_practice(float_1, float_2, epsilon = epsilon_distance):
    return abs(float_1 - float_2) <= epsilon

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

    def get_mean_signed_distance(self, points):
        if not hasattr(points, "__len__"):
            raise TypeError('points should be an array')

        NUM_POINTS = len(points)
        if NUM_POINTS < 1:
            raise ValueError('points should not be empty')

        acc_signed_distance = 0
        for point in points:
            acc_signed_distance += self.get_signed_distance_to_circumference(point)
        return acc_signed_distance / NUM_POINTS

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

def get_y_low_and_y_high(points, x_center, radius):
    """
    Solving these equations:
      (x - x_p)^2 + (y - y_p)^2 = R^2, and
      line x = x_center
    we reach
      y = y_p +- sqrt(R^2 - (x_center - x_p)^2)
    Hence, we can establish
      y_low  = min { y_p - sqrt(R^2 - (x_center - x_p)^2) } for all point p, and
      y_high = max { y_p - sqrt(R^2 + (x_center - x_p)^2) } for all point p
    """
    y_low = float("inf")
    y_high = -float("inf")
    R_TIMES_R = radius * radius

    for point in points:
        DISCRIMINANT = R_TIMES_R - math.pow(x_center - point[0], 2)
        if DISCRIMINANT < 0:
            raise ValueError('The given radius is too small to reach point')
        SQRT_DISCRIMINANT = math.sqrt(DISCRIMINANT)
        y_low = min(y_low, point[1] - SQRT_DISCRIMINANT)
        y_high = max(y_high, point[1] + SQRT_DISCRIMINANT)

    return y_low, y_high

def get_best_fit_circle(points, x_center, radius, use_MSE = False):
    if not hasattr(points, "__len__"):
        raise TypeError('points should be an array')

    NUM_POINTS = len(points)
    if NUM_POINTS <= 3:
        raise ValueError('points should have at least 4 elements')

    y_low, y_high = get_y_low_and_y_high(points, x_center, radius)

    bottom_circle = Circle((x_center, y_low), radius)
    error_for_bottom_circle = bottom_circle.get_MSE(points) if use_MSE else bottom_circle.get_mean_signed_distance(points)
    if zero_in_practice(error_for_bottom_circle):
        return bottom_circle

    top_circle = Circle((x_center, y_high), radius)
    error_for_top_circle = top_circle.get_MSE(points) if use_MSE else top_circle.get_mean_signed_distance(points)
    if zero_in_practice(error_for_top_circle):
        return top_circle

    done = False
    i = 0
    y_cut = y_low + (y_high - y_low)/2
    while not done:
        cut_circle = Circle((x_center, y_cut), radius)
        error_for_cut_circle = cut_circle.get_MSE(points) if use_MSE else cut_circle.get_mean_signed_distance(points)
        # print "iteration #", i, "| y_cut is", y_cut, 'and error_for_cut_circle is', error_for_cut_circle
        if zero_in_practice(error_for_cut_circle):
            return cut_circle

        done = abs(error_for_cut_circle) < epsilon_distance
        if not done:
            if abs(error_for_top_circle) > abs(error_for_bottom_circle):
                # print "resetting top"
                y_high, error_for_top_circle = y_cut, error_for_cut_circle
            else:
                # print "resetting bottom"
                y_low, error_for_bottom_circle = y_cut, error_for_cut_circle
        previous_y_cut = y_cut
        y_cut = y_low + .5*(y_high - y_low)
        i = i + 1
        done = equal_in_practice(y_cut, previous_y_cut) or i == 50

    return Circle((x_center, y_cut), radius)