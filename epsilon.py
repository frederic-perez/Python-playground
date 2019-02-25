'module docstring should be here'

epsilon_distance = 1e-12

def zero_in_practice(float, epsilon = epsilon_distance):
    return abs(float) <= epsilon

def equal_in_practice(float_1, float_2, epsilon = epsilon_distance):
    return abs(float_1 - float_2) <= epsilon
