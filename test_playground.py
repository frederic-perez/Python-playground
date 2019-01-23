"""
Run the tests by executing:
$ python -m unittest -v test_playground
"""

import math
import unittest
from playground import average

class Test_average(unittest.TestCase):

    def test_WHEN_single_parameter_THEN_result_must_be_equal_to_parameter(self):
        self.assertEqual(average(1), 1)
        self.assertEqual(average(math.pi), math.pi)

    def test_WHEN_two_parameters_THEN_result_must_be_equal_to_half_their_sum(self):
        self.assertEqual(average(1, 2), (1+2)/2.)

if __name__ == '__main__':
    unittest.main()
