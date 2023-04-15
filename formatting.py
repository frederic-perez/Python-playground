"""module docstring should be here"""


# Code based on
# https://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
# and on
# https://stackoverflow.com/questions/2440692/formatting-floats-in-python-without-superfluous-zeros
#
def float_formatter(x):
    return "{0:.3f}".format(x).rstrip('0').rstrip('.')


def float_hq_formatter(x):
    return "{0:.21f}".format(x).rstrip('0').rstrip('.')


def floats_formatter(array):
    result = ''
    length = len(array)
    for i in range(0, length):
        result += float_formatter(array[i])
        if i != length - 1:
            result += ' '
    return result


def floats_hq_formatter(array):
    result = ''
    length = len(array)
    for i in range(0, length):
        result += float_hq_formatter(array[i])
        if i != length - 1:
            result += ' '
    return result
