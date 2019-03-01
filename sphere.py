'module docstring should be here'

import math
import numpy as np
from epsilon import epsilon_distance, zero_in_practice, equal_in_practice

class Sphere(object):
    def __init__(self, center, radius):
        if not hasattr(center, "__len__"):
            raise TypeError('center should be an array')
        if center.__len__() != 3:
            raise TypeError('center should be an array of 3 elements')
        if radius <= 0:
            raise ValueError("Value %g is out of range" % radius)
        self.center = np.array(center, np.float_)
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

    def get_center(self):
        return self.center
  
    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

    def get_signed_distance_to_surface(self, point):
        point_in_np = np.array(point, np.float_)
        return np.linalg.norm(self.center - point_in_np) - self.radius
  
    def point_is_on_surface(self, point):
        DISTANCE = self.get_signed_distance_to_surface(point)
        return zero_in_practice(DISTANCE)

    def get_MSE(self, points):
        if not hasattr(points, "__len__"):
            raise TypeError('points should be an array')

        NUM_POINTS = len(points)
        if NUM_POINTS < 1:
            raise ValueError('points should not be empty')

        acc_squared_error = 0
        for point in points:
            error = self.get_signed_distance_to_surface(point)
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
            acc_signed_distance += self.get_signed_distance_to_surface(point)
        return acc_signed_distance / NUM_POINTS

def get_sphere(points):
    """
    Translation of code from http://www.convertalot.com/sphere_solver.html
    on December 21, 2018, and then simplified
    """
    if len(points) != 4:
        raise ValueError('4 points are required')

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
    CENTER = [X, Y, Z]
    RADIUS = math.sqrt(X*X + Y*Y + Z*Z - MINOR_15/MINOR_11)
    return Sphere(CENTER, RADIUS)

def get_y_low_and_y_high(points, x_center, z_center, radius):
    """
    Solving these equations:
      (x - x_p)^2 + (y - y_p)^2 + (z - z_p)^2 = R^2, and
      line x, z = x_center, z_center
    we reach
      y = y_p +- sqrt(R^2 - (x_center - x_p)^2 - (z_center - z_p)^2)
    Hence, we can establish
      y_low  = min { y_p - sqrt(R^2 - (x_center - x_p)^2 - (z_center - z_p)^2) } for all point p, and
      y_high = max { y_p - sqrt(R^2 + (x_center - x_p)^2 - (z_center - z_p)^2) } for all point p
    """
    y_low = float("inf")
    y_high = -float("inf")
    R_TIMES_R = radius**2

    for point in points:
        DISCRIMINANT = R_TIMES_R - (x_center - point[0])**2 - (z_center - point[2])**2
        if zero_in_practice(DISCRIMINANT):
            continue
        if DISCRIMINANT < 0:
            raise ValueError('The given radius is too small to reach point')
        SQRT_DISCRIMINANT = math.sqrt(DISCRIMINANT)
        y_low = min(y_low, point[1] - SQRT_DISCRIMINANT)
        y_high = max(y_high, point[1] + SQRT_DISCRIMINANT)

    return y_low, y_high

def get_best_fit_sphere(points, x_center, z_center, radius, use_MSE = False):
    if not hasattr(points, "__len__"):
        raise TypeError('points should be an array')

    NUM_POINTS = len(points)
    if NUM_POINTS <= 4:
        raise ValueError('points should have at least 5 elements')

    # HACK y_low, y_high = get_y_low_and_y_high(points, x_center, z_center, radius)
    y_low = 0. # HACK
    y_high = 500. # HACK
    # print "y_low is", y_low, "| y_high is", y_high

    bottom_sphere = Sphere([x_center, y_low, z_center], radius)
    error_for_bottom_sphere = bottom_sphere.get_MSE(points) if use_MSE else bottom_sphere.get_mean_signed_distance(points)
    if zero_in_practice(error_for_bottom_sphere):
        return bottom_sphere

    top_sphere = Sphere([x_center, y_high, z_center], radius)
    error_for_top_sphere = top_sphere.get_MSE(points) if use_MSE else top_sphere.get_mean_signed_distance(points)
    if zero_in_practice(error_for_top_sphere):
        return top_sphere

    done = False
    i = 0
    y_cut = y_low + (y_high - y_low)/2
    while not done:
        cut_sphere = Sphere([x_center, y_cut, z_center], radius)
        error_for_cut_sphere = cut_sphere.get_MSE(points) if use_MSE else cut_sphere.get_mean_signed_distance(points)
        # print "iteration #", i, "| y_cut is", y_cut, 'and error_for_cut_circle is', error_for_cut_circle
        if zero_in_practice(error_for_cut_sphere):
            return cut_sphere

        done = abs(error_for_cut_sphere) < epsilon_distance
        if not done:
            if abs(error_for_top_sphere) > abs(error_for_bottom_sphere):
                # print "resetting top"
                y_high, error_for_top_sphere = y_cut, error_for_cut_sphere
            else:
                # print "resetting bottom"
                y_low, error_for_bottom_sphere = y_cut, error_for_cut_sphere
        previous_y_cut = y_cut
        y_cut = y_low + .5*(y_high - y_low)
        i = i + 1
        done = equal_in_practice(y_cut, previous_y_cut) or i == 50

    return Sphere([x_center, y_cut, z_center], radius)

def get_best_fit_sphere_for_radius_range(points, x_center, z_center, radius_range, use_MSE = False):
    if not hasattr(points, "__len__"):
        raise TypeError('points should be an array')

    NUM_POINTS = len(points)
    if NUM_POINTS <= 4:
        raise ValueError('points should have at least 5 elements')

    if len(radius_range) != 2:
        raise ValueError('radius_range should have 2 elements')

    MIN_RADIUS = radius_range[0]
    MAX_RADIUS = radius_range[1]

    min_radius_sphere = get_best_fit_sphere(points, x_center, z_center, MIN_RADIUS)
    error_for_min_radius_sphere = min_radius_sphere.get_MSE(points) if use_MSE else min_radius_sphere.get_mean_signed_distance(points)
    if zero_in_practice(error_for_min_radius_sphere):
        return min_radius_sphere

    max_radius_sphere = get_best_fit_sphere(points, x_center, z_center, MAX_RADIUS)
    error_for_max_radius_sphere = max_radius_sphere.get_MSE(points) if use_MSE else max_radius_sphere.get_mean_signed_distance(points)
    if zero_in_practice(error_for_max_radius_sphere):
        return max_radius_sphere

    done = False
    i = 0
    cut_radius = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS)/2
    while not done:
        cut_sphere = get_best_fit_sphere(points, x_center, z_center, cut_radius)
        error_for_cut_sphere = cut_sphere.get_MSE(points) if use_MSE else cut_sphere.get_mean_signed_distance(points)
        # print "iteration #", i, "| cut_radius is", cut_radius, 'and error_for_cut_sphere is', error_for_cut_sphere
        if zero_in_practice(error_for_cut_sphere):
            return cut_sphere

        done = abs(error_for_cut_sphere) < epsilon_distance
        if not done:
            if abs(error_for_max_radius_sphere) > abs(error_for_min_radius_sphere):
                # print "resetting max"
                MAX_RADIUS, error_for_max_radius_sphere = cut_radius, error_for_cut_sphere
            else:
                # print "resetting mins"
                MIN_RADIUS, error_for_min_radius_sphere = cut_radius, error_for_cut_sphere
        previous_cut_radius = cut_radius
        cut_radius = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS)/2
        i = i + 1
        done = equal_in_practice(cut_radius, previous_cut_radius) or i == 50

    return cut_sphere
