"""module docstring should be here"""

from typing import Sequence


def array_type(sequence: Sequence) -> None:
    if not is_an_array(sequence):
        raise TypeError('The arrangement should be an array')


def is_an_array(sequence: Sequence) -> bool:
    return hasattr(sequence, "__len__") and not isinstance(sequence, str)


def tuple_type(arrangement: tuple) -> None:
    if not is_a_tuple(arrangement):
        raise TypeError('The arrangement should be a tuple')


def is_a_tuple(arrangement: tuple) -> bool:
    return isinstance(arrangement, tuple)


def not_empty(sequence: Sequence) -> None:
    if sequence.__len__() == 0:
        raise ValueError('The sequence should not be empty')


"""
The names of the functions below loosely follow the nomenclature from C++ of
operator comparisons.
See https://en.cppreference.com/w/cpp/language/operator_comparison.
"""


def length_is_equal_to_n(sequence: Sequence, n: int) -> None:
    length = len(sequence)
    if not length == n:
        raise ValueError(f'The sequence should have exactly {n} element(s)')


def length_is_less_than_n(sequence: Sequence, n: int) -> None:
    length = len(sequence)
    if not length < n:
        raise ValueError(f'The sequence should have less than {n} element(s)')


def length_is_less_or_equal_to_n(sequence: Sequence, n: int) -> None:
    length = len(sequence)
    if not length <= n:
        raise ValueError(f'The sequence should have at most {n} element(s)')


def length_is_greater_than_n(sequence: Sequence, n: int) -> None:
    length = len(sequence)
    if not length > n:
        raise ValueError(f'The sequence should have more than {n} element(s)')


def length_is_greater_or_equal_to_n(sequence: Sequence, n: int) -> None:
    length = len(sequence)
    if not length >= n:
        raise ValueError(f'The sequence should have at least {n} element(s)')


def number_is_positive(number: int | float) -> None:
    if not number > 0:
        raise ValueError(f'The number {number} should be positive')
