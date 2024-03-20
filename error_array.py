"""module docstring should be here"""

import check

from enum import Enum
from typing import Final, Sequence


def get_index_of_minimum_abs_error(error_array: Sequence) -> int:
    check.array_type(error_array)
    check.not_empty(error_array)

    n: Final[int] = len(error_array)
    index = 0
    minimum_abs_error = float("inf")
    for i in range(n):
        current_abs_error = abs(error_array[i])
        if current_abs_error < minimum_abs_error:
            minimum_abs_error = current_abs_error
            index = i
    return index


def get_indices_around_minimum_abs_error(error_array: Sequence) -> tuple[int, int]:
    check.array_type(error_array)
    check.length_is_greater_or_equal_to_n(error_array, 3)

    check_single_minimum(error_array)

    n: Final[int] = len(error_array)
    index: Final[int] = get_index_of_minimum_abs_error(error_array)
    if index == 0:
        return 0, 1
    elif index == n - 1:
        return n - 2, n - 1
    return index - 1, index + 1


class Slope(Enum):
    negative = -1
    level = 0
    positive = +1


def get_slope(y0: float, y1: float) -> Slope:
    if y0 > y1:
        return Slope.negative
    elif y0 < y1:
        return Slope.positive
    return Slope.level


def check_single_minimum(y_array: Sequence) -> None:
    check.array_type(y_array)
    check.length_is_greater_or_equal_to_n(y_array, 3)

    n: Final[int] = len(y_array)
    num_slope_changes = 0
    previous_slope = get_slope(y_array[0], y_array[1])
    for i in range(2, n):
        current_slope = get_slope(y_array[i - 1], y_array[i])
        # print(f'i = {i}, current_slope = {current_slope}, num_slope_changes = {num_slope_changes}')
        if previous_slope != Slope.level \
           and current_slope != Slope.level \
           and previous_slope != current_slope:
            num_slope_changes += 1
            if num_slope_changes > 1:
                raise ValueError(f'y_array = `{y_array}` has more than one slope change')
        if current_slope != Slope.level:
            previous_slope = current_slope


def get_range_length(error_array: Sequence) -> float:
    check.array_type(error_array)
    check.length_is_greater_or_equal_to_n(error_array, 2)

    n: Final[int] = len(error_array)
    minimum_error = float("inf")
    maximum_error = float("-inf")
    for i in range(n):
        current_error = error_array[i]
        if current_error < minimum_error:
            minimum_error = current_error
        if current_error > maximum_error:
            maximum_error = current_error
    return maximum_error - minimum_error
