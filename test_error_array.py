"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_error_array
"""

import unittest
from error_array import get_index_of_minimum_abs_error, get_indices_around_minimum_abs_error

class Test_get_index_of_minimum_abs_error(unittest.TestCase):

    def test_GivenANotAnArray_When_get_index_of_minimum_abs_error_ThenExceptionIsRaised(self):
        ERRORS = 'error'
        self.assertRaises(TypeError, get_index_of_minimum_abs_error, ERRORS)

    def test_GivenAnEmptyArray_When_get_index_of_minimum_abs_error_ThenExceptionIsRaised(self):
        ERRORS = []
        self.assertRaises(TypeError, get_index_of_minimum_abs_error, ERRORS)

    def test_GivenAnArrayOf1Element_When_get_index_of_minimum_abs_error_ThenReturn0(self):
        ERRORS = [7]
        self.assertEqual(get_index_of_minimum_abs_error(ERRORS), 0)
 
    def test_GivenAnArrayOfEqualElements_When_get_index_of_minimum_abs_error_ThenReturn0(self):
        ERRORS = [7, 7, 7]
        self.assertEqual(get_index_of_minimum_abs_error(ERRORS), 0)

    def test_GivenAnArrayOfAscendingAbsoluteValues_When_get_index_of_minimum_abs_error_ThenReturn0(self):
        errors = [1, 3, 5]
        self.assertEqual(get_index_of_minimum_abs_error(errors), 0)

        errors = [-1, -3, -5]
        self.assertEqual(get_index_of_minimum_abs_error(errors), 0)

    def test_GivenAnArrayOfNDescendingAbsoluteValues_When_get_index_of_minimum_abs_error_ThenReturnNMinus1(self):
        errors = [5, 3, 1]
        self.assertEqual(get_index_of_minimum_abs_error(errors), len(errors) - 1)

        errors = [-5, -3, -1]
        self.assertEqual(get_index_of_minimum_abs_error(errors), len(errors) - 1)

    def test_GivenAnArrayWithTheMinimumAbsoluteValueInTheMiddle_When_get_index_of_minimum_abs_error_ThenReturnNMinus1Div2(self):
        errors = [5, 1, 3]
        self.assertEqual(get_index_of_minimum_abs_error(errors), (len(errors) - 1)/2)

        errors = [-5, -1, -3]
        self.assertEqual(get_index_of_minimum_abs_error(errors), (len(errors) - 1)/2)

if __name__ == '__main__':
    unittest.main()
