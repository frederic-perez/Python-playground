"""module docstring should be here"""

import math
import numpy as np

import check
from epsilon import epsilon_distance, zero_in_practice, equal_in_practice
from error_array import get_indices_around_minimum_abs_error
from formatting import format_float
from typing import Sequence, TypeAlias


Number: TypeAlias = int | float
TupleOf2Floats: TypeAlias = tuple[float, float]
TupleOf2Numbers: TypeAlias = tuple[Number, Number]


def as_tuple_of_2_floats(a: np.ndarray) -> TupleOf2Floats:
    # Ensure the input has exactly two elements
    if len(a) != 2:
        raise ValueError("The input array-like must have exactly two elements.")

    # Convert each element to float if possible
    try:
        result = (float(a[0]), float(a[1]))
    except ValueError:
        raise ValueError("Both elements of the input array-like must be convertible to floats.")

    return result


class Circle(object):
    center: TupleOf2Floats
    radius: float

    def __new__(cls, center: TupleOf2Numbers, radius: Number) -> 'Circle':
        check.tuple_type(center)
        check.length_is_equal_to_n(center, 2)
        if radius <= 0:
            raise ValueError(f'Radius value {format_float(radius)} is out of range')
        return object.__new__(cls)

    def __init__(self, center: TupleOf2Numbers, radius: Number) -> None:
        self.center = float(center[0]), float(center[1])
        self.radius = float(radius)

    def __eq__(self, other, epsilon: float = epsilon_distance) -> bool:
        return \
            equal_in_practice(self.center[0], other.center[0], epsilon) \
            and equal_in_practice(self.center[1], other.center[1], epsilon) \
            and equal_in_practice(self.radius, other.radius, epsilon)

    def __str__(self) -> str:
        c_x = format_float(self.center[0])
        c_y = format_float(self.center[1])
        r = format_float(self.radius)
        return f'Circle(center=({c_x}, {c_y}), radius={r})'

    def get_radius(self) -> float:
        return self.radius

    def get_center(self) -> TupleOf2Floats:
        return self.center
  
    def spy(self, message: str) -> None:
        print(f'{message}: {self}')

    def get_signed_distance_to_circumference(self, point: TupleOf2Numbers) -> float:
        point_in_np = np.array(point, np.float_)
        return float(np.linalg.norm(self.center - point_in_np)) - self.radius
  
    def point_is_on_circumference(self, point: TupleOf2Numbers) -> bool:
        distance = self.get_signed_distance_to_circumference(point)
        return zero_in_practice(distance)

    def get_mse(self, points: Sequence[TupleOf2Numbers]) -> float:
        check.array_type(points)
        check.not_empty(points)

        acc_squared_error: float = 0
        for point in points:
            error = self.get_signed_distance_to_circumference(point)
            squared_error = error*error
            acc_squared_error += squared_error
        return acc_squared_error / len(points)

    def get_mean_signed_distance(self, points: Sequence[TupleOf2Numbers]) -> float:
        check.array_type(points)
        check.not_empty(points)

        acc_signed_distance: float = 0
        for point in points:
            acc_signed_distance += self.get_signed_distance_to_circumference(point)
        return acc_signed_distance / len(points)


def get_circle(points: Sequence[TupleOf2Numbers]) -> Circle:
    """
    Code adapted from https://stackoverflow.com/questions/52990094
    on February 18, 2019
    """
    check.length_is_equal_to_n(points, 3)

    a = np.zeros((3, 3))
    for i in range(0, 3):
        a[i][0] = points[i][0]
        a[i][1] = points[i][1]
        a[i][2] = 1
    determinant = np.linalg.det(a)
    if zero_in_practice(determinant):
        raise ArithmeticError('It is impossible to divide by zero')

    temp = points[1][0]**2 + points[1][1]**2
    bc = (points[0][0]**2 + points[0][1]**2 - temp) / 2
    cd = (temp - points[2][0]**2 - points[2][1]**2) / 2

    # Center of circle
    x: float = (bc*(points[1][1] - points[2][1]) - cd*(points[0][1] - points[1][1])) / determinant
    y: float = ((points[0][0] - points[1][0]) * cd - (points[1][0] - points[2][0]) * bc) / determinant

    center: TupleOf2Floats = x, y
    radius: float = math.sqrt((x - points[0][0]) ** 2 + (y - points[0][1]) ** 2)

    return Circle(center, radius)


def get_y_min_and_y_max(points: Sequence[TupleOf2Numbers], x_center: Number, radius: Number) -> TupleOf2Floats:
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
    r_times_r = radius**2

    for point in points:
        discriminant = r_times_r - (x_center - point[0])**2
        if zero_in_practice(discriminant):
            continue
        if discriminant < 0:
            raise ValueError('The given radius is too small to reach point')
        sqrt_discriminant = math.sqrt(discriminant)
        y_min = min(y_min, point[1] - sqrt_discriminant)
        y_max = max(y_max, point[1] + sqrt_discriminant)

    return y_min, y_max


def get_best_fit_circle(points: Sequence[TupleOf2Numbers], x_center: Number, radius: Number, use_mse: bool,
                        num_samples: int) -> Circle:  # num_samples = 9):
    check.array_type(points)
    check.length_is_greater_than_n(points, 3)

    y_min, y_max = get_y_min_and_y_max(points, x_center, radius)

    y = [0.] * num_samples
    error = [0.] * num_samples

    done: bool = False
    i: int = 0
    idx_min: int = 0
    while not done:
        delta = (y_max - y_min)/(num_samples - 1.)
        for j in range(num_samples):
            y[j] = y_min + delta*j
            circle = Circle((x_center, y[j]), radius)
            error[j] = circle.get_mse(points) if use_mse else circle.get_mean_signed_distance(points)
            # print(f'i = {i}, j = {j} | y = {y[j]} | error = {error[j]}')
            if zero_in_practice(error[j]):
                return circle
      
        idx_min, idx_max = get_indices_around_minimum_abs_error(error)
        y_min, y_max = y[idx_min], y[idx_max]
        # print(f"idx_min = {idx_min}, idx_max = {idx_max}, y range: {y_min} {y_max}")

        i = i + 1
        done = equal_in_practice(y[idx_min], y[idx_max]) or equal_in_practice(error[idx_min], error[idx_max]) or i == 50

    return Circle((x_center, y[idx_min]), radius)


def main():
    center = 1.1111, 2.2222
    radius = 3.3333
    circle = Circle(center, radius)
    print(f'circle is {circle}')
    circle.spy('Spying circle')

    try:
        negative_radius = -1.23456
        Circle(center, negative_radius)
    except ValueError as error:
        print(f'ValueError exception was expected: {error}')


if __name__ == '__main__':
    main()
