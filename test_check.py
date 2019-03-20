"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_check
"""

import unittest

import check

class Test_array_type(unittest.TestCase):

    def test_GivenANotAnArray_When_array_type_ThenExceptionIsRaised(self):
        ERRORS = 'error'
        self.assertRaises(TypeError, check.array_type, ERRORS)

class Test_is_an_array(unittest.TestCase):

    def test_GivenANotAnArray_When_is_an_array_ThenReturnFalse(self):
        ERRORS = 'error'
        self.assertFalse(check.is_an_array(ERRORS))

class Test_not_empty(unittest.TestCase):

    def test_GivenAnEmptyArray_When_not_empty_ThenExceptionIsRaised(self):
        array = []
        self.assertRaises(ValueError, check.not_empty, array)

    def test_GivenANotEmptyArray_When_not_empty_ThenReturnNone(self):
        array = [1]
        self.assertEqual(check.not_empty(array), None)

if __name__ == '__main__':
    unittest.main()
