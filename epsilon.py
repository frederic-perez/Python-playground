"""module docstring should be here"""

from typing import Final

epsilon_distance: Final[float] = 1e-12


def zero_in_practice(a_float: float, epsilon: float = epsilon_distance) -> bool:
    return abs(a_float) <= epsilon


def equal_in_practice(float_1: float, float_2: float, epsilon: float = epsilon_distance) -> bool:
    return abs(float_1 - float_2) <= epsilon


def main():
    f: Final[float] = 12.3456789e-5
    print(f'zero_in_practice({f}) returns {zero_in_practice(f)}')

    
if __name__ == '__main__':
    main()
