"""module docstring should be here"""

epsilon_distance = 1e-12


def zero_in_practice(a_float, epsilon=epsilon_distance):
    return abs(a_float) <= epsilon


def equal_in_practice(float_1, float_2, epsilon=epsilon_distance):
    return abs(float_1 - float_2) <= epsilon


if __name__ == '__main__':
    F = 12.3456789e-5
    print('zero_in_practice({}) returns {}'.format(F, zero_in_practice(F)))
