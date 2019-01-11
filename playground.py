'module docstring should be here'

import math

from numpy import matrix
from numpy import linalg

def average(*numbers):
    """Self-explanatory"""
    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))

assert average(1) == 1
assert average(math.pi) == math.pi
assert average(1, 2) == 1.5

assert linalg.det(matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])) == 1
