"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_epsilon.py
  or
  $ python test_epsilon.py

or, for individual test classes (sorted as appearing in this file):

  $ python -m unittest -v test_sphere.Test_zero_in_practice
  $ python -m unittest -v test_sphere.Test_equal_in_practice
"""

import unittest

from epsilon import epsilon_distance, zero_in_practice, equal_in_practice
from typing import Final

class Test_zero_in_practice(unittest.TestCase):

    def test_GivenAFloatVeryCloseToZero_When_zero_in_practice_ThenReturnTrue(self):
        f: Final = epsilon_distance/2.
        self.assertTrue(zero_in_practice(f))
 
    def test_GivenAFarEnoughFromZero_When_zero_in_practice_ThenReturnFalse(self):
        f: Final = 2.*epsilon_distance
        self.assertFalse(zero_in_practice(f))


class Test_equal_in_practice(unittest.TestCase):

    def test_GivenAFloat_When_test_equal_in_practice_ThenReturnTrue(self):
        f: Final = 3.
        self.assertTrue(equal_in_practice(f, f))

    def test_GivenAFloatAndA2ndVeryClose_When_test_equal_in_practice_ThenReturnTrue(self):
        f_1: Final = 3.
        f_2: Final = f_1 + epsilon_distance/2.
        self.assertTrue(equal_in_practice(f_1, f_2))
 
    def test_GivenAFloatAndA2ndFarEnough_When_test_equal_in_practice_ThenReturnFalse(self):
        f_1: Final = 3.
        f_2: Final = f_1 + 2.*epsilon_distance
        self.assertFalse(equal_in_practice(f_1, f_2))


if __name__ == '__main__':
    unittest.main()
