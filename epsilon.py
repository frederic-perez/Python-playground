"""module docstring should be here"""

epsilon_distance = 1e-12


def zero_in_practice(a_float, epsilon=epsilon_distance):
    return abs(a_float) <= epsilon


def equal_in_practice(float_1, float_2, epsilon=epsilon_distance):
    return abs(float_1 - float_2) <= epsilon


def main():
    f = 12.3456789e-5
    print(f'zero_in_practice({f}) returns {zero_in_practice(f)}')

    
if __name__ == '__main__':
    main()
