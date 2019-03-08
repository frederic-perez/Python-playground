'module docstring should be here'

def get_index_of_minimum_abs_error(error_array):
    if not hasattr(error_array, "__len__"):
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
    N = len(error_array)
    INDEX = get_index_of_minimum_abs_error(error_array)
    if INDEX == 0:
        return 0, 1
    elif INDEX == N - 1:
        return N - 2, N - 1
    return INDEX - 1, INDEX + 1
