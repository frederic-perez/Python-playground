'module docstring should be here'

def check_array_type(parameter):
    if not is_an_array(parameter):
        raise TypeError('The parameter should be an array')

def is_an_array(parameter):
    return hasattr(parameter, "__len__") and not isinstance(parameter, str)
