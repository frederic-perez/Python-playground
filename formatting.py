'module docstring should be here'

# Code based on
# https://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
# and on
# https://stackoverflow.com/questions/2440692/formatting-floats-in-python-without-superfluous-zeros
#
float_formatter = lambda x: "{0:.3f}".format(x).rstrip('0').rstrip('.')
float_HQ_formatter = lambda x: "{0:.21f}".format(x).rstrip('0').rstrip('.')

def floats_formatter(array):
    result = ''
    LENGTH = len(array)
    for i in range(0, LENGTH):
        result += float_formatter(array[i])
        if i != LENGTH - 1:
            result += ' '
    return result

def floats_HQ_formatter(array):
    result = ''
    LENGTH = len(array)
    for i in range(0, LENGTH):
        result += float_HQ_formatter(array[i])
        if i != LENGTH - 1:
            result += ' '
    return result
