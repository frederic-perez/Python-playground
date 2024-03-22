"""module docstring should be here"""

import numpy.typing as npt

from typing import Final, Sequence, TypeAlias


Arrangement: TypeAlias = Sequence | npt.NDArray


def arrangement_type(arrangement: Arrangement) -> None:
    if not is_an_arrangement(arrangement):
        raise TypeError('The arrangement should be an Arrangement')


def is_an_arrangement(arrangement: Arrangement) -> bool:
    return hasattr(arrangement, "__len__") and not isinstance(arrangement, str)


def tuple_type(arrangement: tuple) -> None:
    if not is_a_tuple(arrangement):
        raise TypeError('The arrangement should be a tuple')


def is_a_tuple(arrangement: tuple) -> bool:
    return isinstance(arrangement, tuple)


def not_empty(arrangement: Arrangement) -> None:
    if arrangement.__len__() == 0:
        raise ValueError('The arrangement should not be empty')


"""
The names of the functions below loosely follow the nomenclature from C++ of
operator comparisons.
See https://en.cppreference.com/w/cpp/language/operator_comparison.
"""


def length_is_equal_to_n(arrangement: Arrangement, n: int) -> None:
    length: Final = len(arrangement)
    if not length == n:
        raise ValueError(f'The arrangement should have exactly {n} element(s)')


def length_is_less_than_n(arrangement: Arrangement, n: int) -> None:
    length: Final = len(arrangement)
    if not length < n:
        raise ValueError(f'The arrangement should have less than {n} element(s)')


def length_is_less_or_equal_to_n(arrangement: Arrangement, n: int) -> None:
    length: Final = len(arrangement)
    if not length <= n:
        raise ValueError(f'The arrangement should have at most {n} element(s)')


def length_is_greater_than_n(arrangement: Arrangement, n: int) -> None:
    length: Final = len(arrangement)
    if not length > n:
        raise ValueError(f'The arrangement should have more than {n} element(s)')


def length_is_greater_or_equal_to_n(arrangement: Arrangement, n: int) -> None:
    length: Final = len(arrangement)
    if not length >= n:
        raise ValueError(f'The arrangement should have at least {n} element(s)')


def number_is_positive(number: int | float) -> None:
    if not number > 0:
        raise ValueError(f'The number {number} should be positive')
