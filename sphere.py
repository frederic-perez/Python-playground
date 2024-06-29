"""module docstring should be here"""

import math
import numpy as np

import check
from epsilon import epsilon_distance, zero_in_practice, equal_in_practice
from error_array import get_indices_around_minimum_abs_error, get_range_length
from formatting import format_float
from typing import Final, Sequence, TypeAlias

Number: TypeAlias = int | float
TupleOf2Floats: TypeAlias = tuple[float, float]
TupleOf3Floats: TypeAlias = tuple[float, float, float]
TupleOf3Numbers: TypeAlias = tuple[Number, Number, Number]


def as_tuple_of_3_floats(a: np.ndarray) -> TupleOf3Floats:
    # Ensure the input has exactly two elements
    if len(a) != 3:
        raise ValueError("The input array-like must have exactly three elements.")

    # Convert each element to float if possible
    try:
        result: Final = float(a[0]), float(a[1]), float(a[2])
    except ValueError:
        raise ValueError("Both elements of the input array-like must be convertible to floats.")

    return result


class Sphere(object):
    center: Final[TupleOf3Floats]
    radius: Final[float]

    def __new__(cls, center: TupleOf3Numbers, radius: Number) -> 'Sphere':
        check.tuple_type(center)
        check.length_is_equal_to_n(center, 3)
        if radius <= 0:
            raise ValueError(f'Radius value {format_float(radius)} is out of range')
        return object.__new__(cls)

    def __init__(self, center: TupleOf3Numbers, radius: Number) -> None:
        self.center = float(center[0]), float(center[1]), float(center[2])
        self.radius = float(radius)

    def __eq__(self, other, epsilon: float = epsilon_distance) -> bool:
        return \
            equal_in_practice(self.center[0], other.center[0], epsilon) \
            and equal_in_practice(self.center[1], other.center[1], epsilon) \
            and equal_in_practice(self.center[2], other.center[2], epsilon) \
            and equal_in_practice(self.radius, other.radius, epsilon)

    def __str__(self) -> str:
        c_x: Final[str] = format_float(self.center[0])
        c_y: Final[str] = format_float(self.center[1])
        c_z: Final[str] = format_float(self.center[2])
        r: Final[str] = format_float(self.radius)
        return f'Sphere(center=({c_x}, {c_y}, {c_z}), radius={r})'

    def get_radius(self) -> float:
        return self.radius

    def get_center(self) -> TupleOf3Floats:
        return self.center

    def spy(self, message: str) -> None:
        print(f'{message}: {self}')

    def get_signed_distance_to_surface(self, point: TupleOf3Numbers) -> float:
        point_in_np: Final = np.array(point, np.float64)
        return float(np.linalg.norm(self.center - point_in_np)) - self.radius

    def point_is_on_surface(self, point: TupleOf3Numbers) -> bool:
        distance: Final = self.get_signed_distance_to_surface(point)
        return zero_in_practice(distance)

    def get_mse(self, points: Sequence[TupleOf3Numbers]) -> float:
        check.arrangement_type(points)
        check.not_empty(points)

        acc_squared_error: float = 0
        for point in points:
            error = self.get_signed_distance_to_surface(point)
            squared_error = error*error
            acc_squared_error += squared_error
        return acc_squared_error / len(points)

    def get_mean_signed_distance(self, points: Sequence[TupleOf3Numbers]) -> float:
        check.arrangement_type(points)
        check.not_empty(points)

        acc_signed_distance: float = 0
        for point in points:
            acc_signed_distance += self.get_signed_distance_to_surface(point)
        return acc_signed_distance / len(points)


def get_sphere(points: Sequence[TupleOf3Numbers]) -> 'Sphere':
    """
    Translation of code from http://www.convertalot.com/sphere_solver.html
    on December 21, 2018, and then simplified
    """
    check.arrangement_type(points)
    check.length_is_equal_to_n(points, 4)

    a = np.zeros((4, 4))
    for i in range(0, 4):
        a[i][0] = points[i][0]
        a[i][1] = points[i][1]
        a[i][2] = points[i][2]
        a[i][3] = 1
    minor_11: Final = np.linalg.det(a)
    if zero_in_practice(minor_11):
        raise ArithmeticError('It is impossible to divide by zero')

    for i in range(0, 4):
        a[i][0] = points[i][0]**2 + points[i][1]**2 + points[i][2]**2
    minor_12: Final = np.linalg.det(a)

    for i in range(0, 4):
        a[i][1] = points[i][0]
    minor_13: Final = np.linalg.det(a)

    for i in range(0, 4):
        a[i][2] = points[i][1]
    minor_14: Final = np.linalg.det(a)

    for i in range(0, 4):
        a[i][3] = points[i][2]
    minor_15: Final = np.linalg.det(a)

    x: Final = .5 * minor_12 / minor_11
    y: Final = -.5 * minor_13 / minor_11
    z: Final = .5 * minor_14 / minor_11
    center: Final[TupleOf3Floats] = x, y, z
    radius: Final = math.sqrt(x * x + y * y + z * z - minor_15 / minor_11)
    return Sphere(center, radius)


def get_y_low_and_y_high(points: Sequence[TupleOf3Numbers], x_center: Number, z_center: Number, radius: Number)\
        -> TupleOf2Floats:
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
    r_times_r: Final = radius**2

    for point in points:
        discriminant = r_times_r - (x_center - point[0])**2 - (z_center - point[2])**2
        if zero_in_practice(discriminant):
            continue
        if discriminant < 0:
            raise ValueError('The given radius is too small to reach point')
        sqrt_discriminant = math.sqrt(discriminant)
        y_low = min(y_low, point[1] - sqrt_discriminant)
        y_high = max(y_high, point[1] + sqrt_discriminant)

    return y_low, y_high


def get_best_fit_sphere(points: Sequence[TupleOf3Numbers], center_x_and_z: TupleOf2Floats, y_range: TupleOf2Floats,
                        radius: float, use_mse: bool, num_samples: int) -> Sphere:  # num_samples=9):
    check.arrangement_type(points)
    check.length_is_greater_than_n(points, 4)
    check.arrangement_type(center_x_and_z)
    check.length_is_equal_to_n(center_x_and_z, 2)
    check.arrangement_type(y_range)
    check.length_is_equal_to_n(y_range, 2)
    check.number_is_positive(num_samples)

    x_center: Final = center_x_and_z[0]
    z_center: Final = center_x_and_z[1]

    y_min = y_range[0]
    y_max = y_range[1]

    y = [0.] * num_samples
    error = [0.] * num_samples

    done = False
    i = 0
    idx_min = 0
    epsilon: Final = 1e-10
    sphere = Sphere((0, 0, 0), 1)
    while not done:
        delta = (y_max - y_min)/(num_samples - 1.)
        for j in range(num_samples):
            y[j] = y_min + delta*j
            sphere = Sphere((x_center, y[j], z_center), radius)
            error[j] = sphere.get_mse(points) if use_mse else sphere.get_mean_signed_distance(points)
            # print(f'i = {i}, j = {j}, | y = {y[j]} | error = {error[j]}')
            if zero_in_practice(error[j]):
                return sphere

        error_range_length = get_range_length(error)
        if zero_in_practice(error_range_length, epsilon):
            return sphere

        idx_min, idx_max = get_indices_around_minimum_abs_error(error)
        y_min, y_max = y[idx_min], y[idx_max]
        # print(f'i = {i} | idx_min is {idx_min}, idx_max is {idx_max}, y range: {y_min}, {y_max}')

        i = i + 1
        done = equal_in_practice(y[idx_min], y[idx_max]) or equal_in_practice(error[idx_min], error[idx_max]) or i == 50

    return Sphere((x_center, y[idx_min], z_center), radius)


def get_best_fit_sphere_for_radius_range(points: Sequence[TupleOf3Numbers], center_x_and_z: TupleOf2Floats,
                                         y_range: TupleOf2Floats, radius_range: TupleOf3Floats, use_mse: bool,
                                         num_samples: int) -> Sphere:
    # num_samples=9):
    check.arrangement_type(points)
    check.length_is_greater_than_n(points, 4)
    check.arrangement_type(center_x_and_z)
    check.length_is_equal_to_n(center_x_and_z, 2)
    check.arrangement_type(y_range)
    check.length_is_equal_to_n(y_range, 2)
    check.arrangement_type(radius_range)
    check.length_is_equal_to_n(radius_range, 2)

    radius_min = radius_range[0]
    radius_max = radius_range[1]

    radius = [0.] * num_samples
    error = [0.] * num_samples

    done = False
    i = 0
    idx_min = 0
    epsilon: Final = 1e-9
    spy_error_range_length: Final = False
    sphere = Sphere((0, 0, 0), 1)
    while not done:
        delta = (radius_max - radius_min)/(num_samples - 1.)
        for j in range(num_samples):
            radius[j] = radius_min + delta*j
            sphere = get_best_fit_sphere(points, center_x_and_z, y_range, radius[j], use_mse, num_samples)
            error[j] = sphere.get_mse(points) if use_mse else sphere.get_mean_signed_distance(points)
            # print(f'i = {i}, j = {j} | radius = {radius[j]} | error = {error[j]}')
            if zero_in_practice(error[j]):
                return sphere

        error_range_length = get_range_length(error)
        if spy_error_range_length:
            print(f'>>> Debug: i = {i:d}: error_range_length = {error_range_length:.3E}')
        if zero_in_practice(error_range_length, epsilon):
            return sphere

        idx_min, idx_max = get_indices_around_minimum_abs_error(error)
        radius_min, radius_max = radius[idx_min], radius[idx_max]
        # print(f"idx_min is {idx_min}, idx_max is {idx_max}, radius range: {radius_min}, {radius_max}")

        i = i + 1
        done =\
            equal_in_practice(radius[idx_min], radius[idx_max])\
            or equal_in_practice(error[idx_min], error[idx_max])\
            or i == 50

    return get_best_fit_sphere(points, center_x_and_z, y_range, radius[idx_min], use_mse, num_samples)


def main():
    center: Final[TupleOf3Floats] = 1.11111, 2.22222, 3.33333
    radius: Final = 4.44444
    sphere = Sphere(center, radius)
    print(f'sphere is {sphere}')
    sphere.spy('Spying sphere')

    try:
        negative_radius: Final = -1.23456
        Sphere(center, negative_radius)
    except ValueError as error:
        print(f'ValueError exception caught, as expected: {error}')


if __name__ == '__main__':
    main()