"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_check
"""

import unittest
from check import check_array_type, is_an_array

class Test_check_array_type(unittest.TestCase):

    def test_GivenANotAnArray_When_check_array_type_ThenExceptionIsRaised(self):
        ERRORS = 'error'
        self.assertRaises(TypeError, check_array_type, ERRORS)

class Test_is_an_array(unittest.TestCase):

    def test_GivenANotAnArray_When_is_an_array_ThenReturnFalse(self):
        ERRORS = 'error'
        self.assertFalse(is_an_array(ERRORS))

if __name__ == '__main__':
    unittest.main()
