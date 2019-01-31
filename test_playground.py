"""
Run the tests by executing:
$ python -m unittest -v test_playground
"""

import math
import unittest
from playground import average

class Test_average(unittest.TestCase):

    def test_GivenSingleParameterP_When_average_ThenReturnP(self):
        self.assertEqual(average(1), 1)
        self.assertEqual(average(math.pi), math.pi)

    def test_Given2Parameters_When_average_ThenReturnHalfTheirSum(self):
        self.assertEqual(average(1, 2), (1+2)/2.)

if __name__ == '__main__':
    unittest.main()
