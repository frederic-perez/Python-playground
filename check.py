'module docstring should be here'

def array_type(arrangement):
    if not is_an_array(arrangement):
        raise TypeError('The arrangement should be an array')

def is_an_array(arrangement):
    return hasattr(arrangement, "__len__") and not isinstance(arrangement, str)

def not_empty(arrangement):
    if arrangement.__len__() == 0:
        raise ValueError('The arrangement should not be empty')

def length_is_less_or_equal_to_N(arrangement, n):
    LENGTH = len(arrangement)
    if not LENGTH <= n:
        raise ValueError('The arrangement should have at most %d element(s)', n)

def length_is_greater_than_N(arrangement, n):
    LENGTH = len(arrangement)
    if not LENGTH > n:
        raise ValueError('The arrangement should have more than %d element(s)', n)
