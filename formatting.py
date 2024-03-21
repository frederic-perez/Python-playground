"""module docstring should be here"""

import numpy as np

from typing import Final, Sequence


# Code based on
# https://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
# and on
# https://stackoverflow.com/questions/2440692/formatting-floats-in-python-without-superfluous-zeros
#
def format_float(x: float) -> str:
    return '{0:.3f}'.format(x).rstrip('0').rstrip('.')


def format_float_hq(x: float) -> str:
    return '{0:.21f}'.format(x).rstrip('0').rstrip('.')


def format_floats(array: Sequence) -> str:
    result = ''
    length: Final[int] = len(array)
    for i in range(0, length):
        result += format_float(array[i])
        if i != length - 1:
            result += ' '
    return result


def format_floats_hq(array: Sequence) -> str:
    result = ''
    length: Final[int] = len(array)
    for i in range(0, length):
        result += format_float_hq(array[i])
        if i != length - 1:
            result += ' '
    return result


def format_np_floating(x: np.floating) -> str:
    return format_float(float(x))


def main():
    for x in 12.3456789000000, 12.0003456789000, 12345.6789, -0.000001:
        print('x being ' + str(x) + f' (type(x) = {type(x)}):')
        print('  » {} (using `.format(format_float(x)`)'.format(format_float(x)))
        print(f'  » {x:.3f} (using just 3 decimals with .3f)')
        print(f'  » {x:.3g} (using just 3 decimals with .3g)')

    y: Final[np.floating] = np.float64(12.3456789000000)
    print('y being ' + str(y) + f' (type(y) = {type(y)}):')
    print('  » {} (using `.format(format_np_floating(y)`)'.format(format_np_floating(y)))
    print(f'  » {y:.3f} (using just 3 decimals with .3f)')
    print(f'  » {y:.3g} (using just 3 decimals with .3g)')


if __name__ == '__main__':
    main()
