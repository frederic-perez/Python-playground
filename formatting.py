"""module docstring should be here"""


# Code based on
# https://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
# and on
# https://stackoverflow.com/questions/2440692/formatting-floats-in-python-without-superfluous-zeros
#
def format_float(x):
    return '{0:.3f}'.format(x).rstrip('0').rstrip('.')


def format_float_hq(x):
    return '{0:.21f}'.format(x).rstrip('0').rstrip('.')


def format_floats(array):
    result = ''
    length = len(array)
    for i in range(0, length):
        result += format_float(array[i])
        if i != length - 1:
            result += ' '
    return result


def format_floats_hq(array):
    result = ''
    length = len(array)
    for i in range(0, length):
        result += format_float_hq(array[i])
        if i != length - 1:
            result += ' '
    return result


def main():
    for f in 12.3456789000000, 12.0003456789000, 12345.6789, -0.000001:  # trailing zeros are not printed
        print('f being ' + str(f) + ':')
        print('  » {} (using `.format(format_float(f)`)'.format(format_float(f)))
        print(f'  » {f:.3f} (using just 3 decimals with .3f)')
        print(f'  » {f:.3g} (using just 3 decimals with .3g)')
        print(f'  » {format_float(f)} (using float_formatter in an f-string)')


if __name__ == '__main__':
    main()
