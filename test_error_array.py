"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_error_array.py
  or
  $ python test_error_array.py
"""

import unittest

from error_array import check_single_minimum, get_index_of_minimum_abs_error, get_indices_around_minimum_abs_error, \
    get_range_length
from typing import Any, Final


class Test_get_index_of_minimum_abs_error(unittest.TestCase):

    def test_GivenANotAnArray_When_get_index_of_minimum_abs_error_ThenExceptionIsRaised(self):
        errors: Final = 'error'
        self.assertRaises(TypeError, get_index_of_minimum_abs_error, errors)

    def test_GivenAnEmptyArray_When_get_index_of_minimum_abs_error_ThenExceptionIsRaised(self):
        errors: Final[tuple] = ()
        self.assertRaises(ValueError, get_index_of_minimum_abs_error, errors)

    def test_GivenAnArrayOf1Element_When_get_index_of_minimum_abs_error_ThenReturn0(self):
        errors: Final[tuple[int]] = 7,
        self.assertEqual(get_index_of_minimum_abs_error(errors), 0)
 
    def test_GivenAnArrayOfEqualElements_When_get_index_of_minimum_abs_error_ThenReturn0(self):
        errors: Final = 7, 7, 7
        self.assertEqual(get_index_of_minimum_abs_error(errors), 0)

    def test_GivenAnArrayOfAscendingAbsoluteValues_When_get_index_of_minimum_abs_error_ThenReturn0(self):
        for errors in (1, 3, 5), (-1, -3, -5):
            self.assertEqual(get_index_of_minimum_abs_error(errors), 0)

    def test_GivenAnArrayOfNDescendingAbsoluteValues_When_get_index_of_minimum_abs_error_ThenReturnNMinus1(self):
        for errors in (5, 3, 1), (-5, -3, -1):
            self.assertEqual(get_index_of_minimum_abs_error(errors), len(errors) - 1)

    def test_GivenAnArrayWithTheMinimumAbsoluteValueInTheMiddle_When_get_index_of_minimum_abs_error_ThenReturnNMinus1Div2(self):
        for errors in (5, 1, 3), (-5, -1, -3):
            self.assertEqual(get_index_of_minimum_abs_error(errors), (len(errors) - 1)/2)


class Test_get_indices_around_minimum_abs_error(unittest.TestCase):

    def test_GivenANotAnArray_When_get_indices_around_minimum_abs_error_ThenExceptionIsRaised(self):
        errors: Final = 'error'
        self.assertRaises(TypeError, get_indices_around_minimum_abs_error, errors)

    def test_GivenAnEmptyArray_When_get_indices_around_minimum_abs_error_ThenExceptionIsRaised(self):
        errors: list[Any] = []
        self.assertRaises(ValueError, get_indices_around_minimum_abs_error, errors)

    def test_GivenAnArrayWithLessThan3Elements_When_get_indices_around_minimum_abs_error_ThenExceptionIsRaised(self):
        self.assertRaises(ValueError, get_indices_around_minimum_abs_error, [1])
        self.assertRaises(ValueError, get_indices_around_minimum_abs_error, [1, 2])

    def test_GivenAnArrayOfEqualElements_When_get_indices_around_minimum_abs_error_ThenReturn0And1(self):
        errors: Final = [7, 7, 7]
        self.assertEqual(get_indices_around_minimum_abs_error(errors), (0, 1))

    def test_GivenAnArrayOfAscendingAbsoluteValues_When_get_indices_around_minimum_abs_error_ThenReturn0And1(self):
        for errors in (1, 3, 5), (-1, -3, -5):
            self.assertEqual(get_indices_around_minimum_abs_error(errors), (0, 1))

    def test_GivenAnArrayOfNDescendingAbsoluteValues_When_get_indices_around_minimum_abs_error_ThenReturnNMinus2AndNMinus1(self):
        for errors in (5, 3, 1), (-5, -3, -1):
            n = len(errors)
            self.assertEqual(get_indices_around_minimum_abs_error(errors), (n - 2, n - 1))

    def test_GivenAnArrayWithTheMinimumAbsoluteValueInTheMiddle_When_get_indices_around_minimum_abs_error_ThenReturnIndicesAroundCenter(self):
        for errors in (5, 1, 3), (-5, -1, -3):
            n = len(errors)
            idx_center = (n - 1)/2
            self.assertEqual(get_indices_around_minimum_abs_error(errors), (idx_center - 1, idx_center + 1))


class Test_check_single_minimum(unittest.TestCase):

    def test_GivenANotAnArray_When_check_single_minimum_ThenExceptionIsRaised(self):
        for parameter in 'error', 0, None:
            self.assertRaises(TypeError, check_single_minimum, parameter)

    def test_GivenAnArrayWithFewerThan3Elements_When_check_single_minimum_ExceptionIsNotRaised(self):
        y_arrays: Final = (), (1,), (1, 2)
        for y_array in y_arrays:
            try:
                check_single_minimum(y_array)
            except ValueError:
                self.assertTrue(self, False)

    def test_GivenAnArrayWithTheMinimumElementBeingThe1st_When_check_single_minimum_ThenExceptionIsNotRaised(self):
        y_arrays: Final = (1, 1, 1), (1, 1, 2), (1, 2, 2)
        for y_array in y_arrays:
            try:
                check_single_minimum(y_array)
            except ValueError:
                self.assertTrue(self, False)

    def test_GivenAnArrayWithTheMinimumElementBeingThe3rd_When_check_single_minimum_ThenExceptionIsNotRaised(self):
        y_array: Final = 8, 2, 1, 6, 24
        try:
            check_single_minimum(y_array)
        except ValueError:
            self.assertTrue(self, False)


class Test_get_range_length(unittest.TestCase):

    def test_GivenANotAnArray_When_get_range_ThenExceptionIsRaised(self):
        for parameter in 'error', 0, None:
            self.assertRaises(TypeError, get_range_length, parameter)

    def test_GivenAnArrayWithLessThan2Elements_When_get_range_ThenExceptionIsRaised(self):
        y_arrays: Final[tuple[list[Any], list[int]]] = [], [1]
        for y_array in y_arrays:
            self.assertRaises(ValueError, get_range_length, y_array)

    def test_GivenAnArrayWithARepeatedK_When_get_range_ThenReturn0(self):
        y_arrays: Final = [0, 0], [7, 7], [9, 9, 9, 9]
        for y_array in y_arrays:
            self.assertEqual(get_range_length(y_array), 0)

    def test_GivenAnArrayWithRangeR_When_get_range_ThenReturnR(self):
        y_arrays: Final = [0, 3], [-3, 0], [0, 3, 1, 2]
        expected_range: Final = 3
        for y_array in y_arrays:
            self.assertEqual(get_range_length(y_array), expected_range)


if __name__ == '__main__':
    unittest.main()
