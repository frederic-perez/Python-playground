"""module docstring should be here"""


def array_type(arrangement):
    if not is_an_array(arrangement):
        raise TypeError('The arrangement should be an array')


def is_an_array(arrangement):
    return hasattr(arrangement, "__len__") and not isinstance(arrangement, str)


def tuple_type(arrangement):
    if not is_a_tuple(arrangement):
        raise TypeError('The arrangement should be a tuple')


def is_a_tuple(arrangement):
    return isinstance(arrangement, tuple)


def not_empty(arrangement):
    if arrangement.__len__() == 0:
        raise ValueError('The arrangement should not be empty')


"""
The names of the functions below loosely follow the nomenclature from C++ of
operator comparisons.
See https://en.cppreference.com/w/cpp/language/operator_comparison.
"""


def length_is_equal_to_n(arrangement, n):
    length: int = len(arrangement)
    if not length == n:
        raise ValueError(f'The arrangement should have exactly {n} element(s)')


def length_is_less_than_n(arrangement, n):
    length: int = len(arrangement)
    if not length < n:
        raise ValueError(f'The arrangement should have less than {n} element(s)')


def length_is_less_or_equal_to_n(arrangement, n):
    length: int = len(arrangement)
    if not length <= n:
        raise ValueError(f'The arrangement should have at most {n} element(s)')


def length_is_greater_than_n(arrangement, n):
    length: int = len(arrangement)
    if not length > n:
        raise ValueError(f'The arrangement should have more than {n} element(s)')


def length_is_greater_or_equal_to_n(arrangement, n):
    length: int = len(arrangement)
    if not length >= n:
        raise ValueError(f'The arrangement should have at least {n} element(s)')


def number_is_positive(number):
    if not number > 0:
        raise ValueError(f'The number {number} should be positive')
