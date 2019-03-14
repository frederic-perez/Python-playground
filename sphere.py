'module docstring should be here'

import math
import numpy as np
from epsilon import epsilon_distance, zero_in_practice, equal_in_practice
from error_array import check_array_type, get_indices_around_minimum_abs_error

class Sphere(object):
    def __init__(self, center, radius):
        check_array_type(center)
        if center.__len__() != 3:
            raise TypeError('center should be an array of 3 elements')
        if radius <= 0:
            raise ValueError("Value %g is out of range" % radius)
        self.center = np.array(center, np.float_)
        self.radius = radius
        return

    def __eq__(self, other, epsilon = epsilon_distance):
        return \
            equal_in_practice(self.center[0], other.center[0], epsilon) \
            and equal_in_practice(self.center[1], other.center[1], epsilon) \
            and equal_in_practice(self.center[2], other.center[2], epsilon) \
            and equal_in_practice(self.radius, other.radius, epsilon)

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
        check_array_type(points)

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
        check_array_type(points)

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

def get_best_fit_sphere(points, center_x_and_z, y_range, radius, use_MSE, num_samples = 9):
    check_array_type(points)

    NUM_POINTS = len(points)
    if NUM_POINTS <= 4:
        raise ValueError('points should have at least 5 elements')

    if len(center_x_and_z) != 2:
        raise ValueError('center_x_and_z should have 2 elements')

    if len(y_range) != 2:
        raise ValueError('y_range should have 2 elements')

    x_center = center_x_and_z[0]
    z_center = center_x_and_z[1]

    y_min = y_range[0]
    y_max = y_range[1]

    y = [0.] * num_samples
    error = [0.] * num_samples

    done = False
    i = 0
    idx_min = 0
    while not done:
      delta = (y_max - y_min)/(num_samples - 1.)
      for j in range(num_samples):
          y[j] = y_min + delta*j
          sphere = Sphere([x_center, y[j], z_center], radius)
          error[j] = sphere.get_MSE(points) if use_MSE else sphere.get_mean_signed_distance(points)
          # print "i =", i, "j =", j, "| y =", y[j], "| error =", error[j]
          if zero_in_practice(error[j]):
              return sphere
      
      idx_min, idx_max = get_indices_around_minimum_abs_error(error)
      y_min, y_max = y[idx_min], y[idx_max]
      # print "i =", i, "| idx_min is", idx_min, "idx_max is", idx_max, "y range:", y_min, y_max

      i = i + 1
      done =  equal_in_practice(y[idx_min], y[idx_max]) or equal_in_practice(error[idx_min], error[idx_max]) or i == 50

    # raise ValueError('WIP')

    return Sphere([x_center, y[idx_min], z_center], radius)

def get_best_fit_sphere_for_radius_range(points, x_center, z_center, y_range, radius_range, use_MSE, num_samples = 9):
    check_array_type(points)

    NUM_POINTS = len(points)
    if NUM_POINTS <= 4:
        raise ValueError('points should have at least 5 elements')

    if len(y_range) != 2:
        raise ValueError('y_range should have 2 elements')

    if len(radius_range) != 2:
        raise ValueError('radius_range should have 2 elements')

    radius_min = radius_range[0]
    radius_max = radius_range[1]

    radius = [0.] * num_samples
    error = [0.] * num_samples

    done = False
    i = 0
    idx_min = 0
    while not done:
      delta = (radius_max - radius_min)/(num_samples - 1.)
      for j in range(num_samples):
          radius[j] = radius_min + delta*j
          sphere = get_best_fit_sphere(points, x_center, z_center, y_range, radius[j], use_MSE, num_samples)
          error[j] = sphere.get_MSE(points) if use_MSE else sphere.get_mean_signed_distance(points)
          # print "i =", i, "j =", j, "| radius =", radius[j], "| error =", error[j]
          if zero_in_practice(error[j]):
              return sphere
      
      idx_min, idx_max = get_indices_around_minimum_abs_error(error)
      radius_min, radius_max = radius[idx_min], radius[idx_max]
      # print "idx_min is", idx_min, "idx_max is", idx_max, "radius range:", radius_min, radius_max

      i = i + 1
      done =  equal_in_practice(radius[idx_min], radius[idx_max]) or equal_in_practice(error[idx_min], error[idx_max]) or i == 50

    return get_best_fit_sphere(points, x_center, z_center, y_range, radius[idx_min], use_MSE, num_samples)
