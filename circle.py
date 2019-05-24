'module docstring should be here'

import math
import numpy as np

import check
from epsilon import epsilon_distance, zero_in_practice, equal_in_practice
from error_array import get_indices_around_minimum_abs_error
from formatting import float_formatter

class Circle(object):
    def __init__(self, center, radius):
        check.array_type(center)
        check.length_is_equal_to_N(center, 2)
        if radius <= 0:
            raise ValueError("Value %g is out of range" % radius)
        self.center = np.array(center, np.float_)
        self.radius = radius
        return

    def __eq__(self, other, epsilon = epsilon_distance):
        return \
            equal_in_practice(self.center[0], other.center[0], epsilon) \
            and equal_in_practice(self.center[1], other.center[1], epsilon) \
            and equal_in_practice(self.radius, other.radius, epsilon)

    def __str__(self):
        return 'Circle(center={}, radius={})'.format(self.center, float_formatter(self.radius))

    def get_radius(self):
        return self.radius

    def get_center(self):
        return self.center
  
    def spy(self, message):
        print('{0}: {1}'.format(message, self))
        return

    def get_signed_distance_to_circumference(self, point):
        point_in_np = np.array(point, np.float_)
        return np.linalg.norm(self.center - point_in_np) - self.radius
  
    def point_is_on_circumference(self, point):
        DISTANCE = self.get_signed_distance_to_circumference(point)
        return zero_in_practice(DISTANCE)

    def get_MSE(self, points):
        check.array_type(points)
        check.not_empty(points)

        acc_squared_error = 0
        for point in points:
            error = self.get_signed_distance_to_circumference(point)
            squared_error = error*error
            acc_squared_error += squared_error
        return acc_squared_error / len(points)

    def get_mean_signed_distance(self, points):
        check.array_type(points)
        check.not_empty(points)

        acc_signed_distance = 0
        for point in points:
            acc_signed_distance += self.get_signed_distance_to_circumference(point)
        return acc_signed_distance / len(points)

def get_circle(points):
    """
    Code adapted from https://stackoverflow.com/questions/52990094
    on February 18, 2019
    """
    check.length_is_equal_to_N(points, 3)

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

    CENTER = [X, Y]
    RADIUS = math.sqrt((X - points[0][0])**2 + (Y - points[0][1])**2)

    return Circle(CENTER, RADIUS)

def get_y_min_and_y_max(points, x_center, radius):
    """
    Solving these equations:
      (x - x_p)^2 + (y - y_p)^2 = R^2, and
      line x = x_center
    we reach
      y = y_p +- sqrt(R^2 - (x_center - x_p)^2)
    Hence, we can establish
      y_min  = min { y_p - sqrt(R^2 - (x_center - x_p)^2) } for all point p, and
      y_max = max { y_p - sqrt(R^2 + (x_center - x_p)^2) } for all point p
    """
    y_min = float("inf")
    y_max = -float("inf")
    R_TIMES_R = radius**2

    for point in points:
        DISCRIMINANT = R_TIMES_R - (x_center - point[0])**2
        if zero_in_practice(DISCRIMINANT):
            continue
        if DISCRIMINANT < 0:
            raise ValueError('The given radius is too small to reach point')
        SQRT_DISCRIMINANT = math.sqrt(DISCRIMINANT)
        y_min = min(y_min, point[1] - SQRT_DISCRIMINANT)
        y_max = max(y_max, point[1] + SQRT_DISCRIMINANT)

    return y_min, y_max

def get_best_fit_circle(points, x_center, radius, use_MSE, num_samples): # num_samples = 9):
    check.array_type(points)
    check.length_is_greater_than_N(points, 3)

    y_min, y_max = get_y_min_and_y_max(points, x_center, radius)

    y = [0.] * num_samples
    error = [0.] * num_samples

    done = False
    i = 0
    idx_min = 0
    while not done:
      delta = (y_max - y_min)/(num_samples - 1.)
      for j in range(num_samples):
          y[j] = y_min + delta*j
          circle = Circle([x_center, y[j]], radius)
          error[j] = circle.get_MSE(points) if use_MSE else circle.get_mean_signed_distance(points)
          # print('i = {}, j = {} | y = {} | error = {}'.format(i, j, y[j], error[j]))
          if zero_in_practice(error[j]):
              return circle
      
      idx_min, idx_max = get_indices_around_minimum_abs_error(error)
      y_min, y_max = y[idx_min], y[idx_max]
      # print('idx_min = {}, idx_max = {}, y range: {} {}'.format(idx_min, idx_max, y_min, y_max))

      i = i + 1
      done =  equal_in_practice(y[idx_min], y[idx_max]) or equal_in_practice(error[idx_min], error[idx_max]) or i == 50

    return Circle([x_center, y[idx_min]], radius)

if __name__ == '__main__':
    CENTER = [1.1111, 2.2222]
    RADIUS = 3.3333
    CIRCLE = Circle(CENTER, RADIUS)
    print('CIRCLE is', CIRCLE)
    CIRCLE.spy('Spying CIRCLE')
