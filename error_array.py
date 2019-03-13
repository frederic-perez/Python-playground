'module docstring should be here'

def get_index_of_minimum_abs_error(error_array):
    if not hasattr(error_array, "__len__") or isinstance(error_array, str):
        raise TypeError('error_array should be an array')
    if error_array.__len__() == 0:
        raise TypeError('error_array should not be empty')

    N = len(error_array)
    index = 0
    minimum_abs_error = float("inf")
    for i in range(N):
        current_abs_error = abs(error_array[i])
        if current_abs_error < minimum_abs_error:
            minimum_abs_error = current_abs_error
            index = i
    return index

def get_indices_around_minimum_abs_error(error_array):
    if not hasattr(error_array, "__len__") or isinstance(error_array, str):
        raise TypeError('error_array should be an array')
    if error_array.__len__() < 3:
        raise TypeError('error_array should have at least 3 components ')

    check_single_minimum(error_array)

    N = len(error_array)
    INDEX = get_index_of_minimum_abs_error(error_array)
    if INDEX == 0:
        return 0, 1
    elif INDEX == N - 1:
        return N - 2, N - 1
    return INDEX - 1, INDEX + 1

def check_single_minimum(y_array):
    if not hasattr(y_array, "__len__") or isinstance(y_array, str):
        raise TypeError('y_array should be an array')
    N = y_array.__len__()
    if N < 3:
        raise ValueError('y_array has too few elements')

    num_slope_changes = 0
    previous_slope = get_slope(y_array[0], y_array[1])
    for i in range (2, N):
        current_slope = get_slope(y_array[i - 1], y_array[i])
        # print 'i = %d, current_slope = %d, num_slope_changes = %d' % (i, current_slope, num_slope_changes)
        if previous_slope != SLOPE_LEVEL \
           and current_slope != SLOPE_LEVEL \
           and previous_slope != current_slope:
            num_slope_changes += 1
            if num_slope_changes > 1:
                raise ValueError('y_array = `%s` has more than one slope change', y_array)
                # print 'Warning: y_array = `%s` has more than one slope change' % y_array
        if current_slope != SLOPE_LEVEL:
            previous_slope = current_slope

def get_slope(y0, y1):
    if y0 > y1:
        return SLOPE_NEGATIVE
    elif y0 < y1:
        return SLOPE_POSITIVE
    return SLOPE_LEVEL

SLOPE_NEGATIVE = -1
SLOPE_LEVEL = 0
SLOPE_POSITIVE = +1
