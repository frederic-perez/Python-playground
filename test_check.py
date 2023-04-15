"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_check.py
  or
  $ python test_check.py
"""

import unittest

import check


class TestArrayType(unittest.TestCase):

    def test_GivenANotAnArray_When_array_type_ThenExceptionIsRaised(self):
        errors = 'error'
        self.assertRaises(TypeError, check.array_type, errors)


class TestIsAnArray(unittest.TestCase):

    def test_GivenANotAnArray_When_is_an_array_ThenReturnFalse(self):
        errors = 'error'
        self.assertFalse(check.is_an_array(errors))


class TestNotEmpty(unittest.TestCase):

    def test_GivenAnEmptyArray_When_not_empty_ThenExceptionIsRaised(self):
        array = []
        self.assertRaises(ValueError, check.not_empty, array)

    def test_GivenANotEmptyArray_When_not_empty_ThenReturnNone(self):
        array = [1]
        self.assertEqual(check.not_empty(array), None)


class TestLengthIsEqualToN(unittest.TestCase):

    def test_GivenANotEmptyArrayAndNDifferentThanItsSize_When_length_is_equal_to_N_ThenExceptionIsRaised(self):
        array = [1, 2, 3]
        size = len(array)
        n_array = []
        for i in range(0, size):
            n_array.append(i)
        for i in range(size + 1, size + 5):
            n_array.append(i)

        for n in n_array:
            self.assertRaises(ValueError, check.length_is_equal_to_n, array, n)

    def test_GivenANotEmptyArrayAndNEqualToItsSize_When_length_is_equal_to_N_ThenReturnNone(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            n = size
            self.assertEqual(check.length_is_equal_to_n(array, n), None)


class TestLengthIsLessThanN(unittest.TestCase):

    def test_GivenANotEmptyArrayAndNLowerOrEqualThanItsSize_When_length_is_less_than_N_ThenExceptionIsRaised(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(0, size + 1):
                self.assertRaises(ValueError, check.length_is_less_than_n, array, n)

    def test_GivenANotEmptyArrayAndNGreaterThanItsSize_When_length_is_less_than_N_ThenReturnNone(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(size + 1, size + 5):
                self.assertEqual(check.length_is_less_than_n(array, n), None)


class TestLengthIsLessOrEqualToN(unittest.TestCase):

    def test_GivenANotEmptyArrayAndNGreaterThanItsSize_When_length_is_less_or_equal_to_N_ThenReturnNone(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(size + 1, size + 5):
                self.assertEqual(check.length_is_less_or_equal_to_n(array, n), None)

    def test_GivenANotEmptyArrayAndNLowerOrEqualToItsSize_When_length_is_less_or_equal_to_N_ThenExceptionIsRaised(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(0, size):
                self.assertRaises(ValueError, check.length_is_less_or_equal_to_n, array, n)


class TestLengthIsGreaterThanN(unittest.TestCase):

    def test_GivenANotEmptyArrayAndNLowerThanItsSize_When_length_is_greater_than_N_ThenReturnNone(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(0, size):
                self.assertEqual(check.length_is_greater_than_n(array, n), None)

    def test_GivenANotEmptyArrayAndNGreaterOrEqualToItsSize_When_length_is_greater_than_N_ThenExceptionIsRaised(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(size, size + 5):
                self.assertRaises(ValueError, check.length_is_greater_than_n, array, n)


class TestLengthIsGreaterOrEqualToN(unittest.TestCase):

    def test_GivenANotEmptyArrayAndNLowerOrEqualToItsSize_When_length_is_greater_or_equal_to_N_ThenReturnNone(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(0, size + 1):
                self.assertEqual(check.length_is_greater_or_equal_to_n(array, n), None)

    def test_GivenANotEmptyArrayAndNLargerThanItsSize_When_length_is_greater_or_equal_to_N_ThenExceptionIsRaised(self):
        array = []
        for i in range(0, 5):
            array.append(i)
            size = len(array)
            for n in range(size + 1, size + 5):
                self.assertRaises(ValueError, check.length_is_greater_or_equal_to_n, array, n)


if __name__ == '__main__':
    unittest.main()
