"""
Run the tests by executing:
$ python -m unittest -v test_playground
"""

import math
import unittest
from epsilon import equal_in_practice
from playground import average

class Test_average(unittest.TestCase):
    
    def test_GivenAnEmptyInput_When_average_ThenExceptionIsRaised(self):
        self.assertRaises(ValueError, average)

    def test_GivenSingleParameterP_When_average_ThenReturnP(self):
        self.assertTrue(equal_in_practice(average(1), 1))
        self.assertTrue(equal_in_practice(average(math.pi), math.pi))

    def test_Given2Parameters_When_average_ThenReturnHalfTheirSum(self):
        self.assertTrue(equal_in_practice(average(1, 2), (1+2)/2.))

if __name__ == '__main__':
    unittest.main()
