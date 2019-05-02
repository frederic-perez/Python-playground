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

class Test_zero_in_practice(unittest.TestCase):

    def test_GivenAFloatVeryCloseToZero_When_zero_in_practice_ThenReturnTrue(self):
        F = epsilon_distance/2.
        self.assertTrue(zero_in_practice(F))
 
    def test_GivenAFarEnoughFromZero_When_zero_in_practice_ThenReturnFalse(self):
        F = 2.*epsilon_distance
        self.assertFalse(zero_in_practice(F))

class Test_equal_in_practice(unittest.TestCase):

    def test_GivenAFloat_When_test_equal_in_practice_ThenReturnTrue(self):
        F = 3.
        self.assertTrue(equal_in_practice(F, F))

    def test_GivenAFloatAndA2ndVeryClose_When_test_equal_in_practice_ThenReturnTrue(self):
        F_1 = 3.
        F_2 = F_1 + epsilon_distance/2.
        self.assertTrue(equal_in_practice(F_1, F_2))
 
    def test_GivenAFloatAndA2ndFarEnough_When_test_equal_in_practice_ThenReturnFalse(self):
        F_1 = 3.
        F_2 = F_1 + 2.*epsilon_distance
        self.assertFalse(equal_in_practice(F_1, F_2))

if __name__ == '__main__':
    unittest.main()
