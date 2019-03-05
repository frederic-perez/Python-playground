"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_timer
"""

import unittest
from time import sleep
from timer import Timer

class Test_timer(unittest.TestCase):

    def test_GivenATimerAnd0msPass_When_get_duration_string_ThenReturnDurationCloseTo0ms(self):
        TIMER = Timer()
        RESULT = TIMER.get_duration_string()
        self.assertTrue(RESULT == "0.000\"" or RESULT == "0.001\"")

    def test_GivenATimerAndXmsPass_When_get_duration_string_ThenReturnDurationCloseToXms(self):
        TIMER = Timer()
        X_MILLISECONDS = 0.123
        sleep(X_MILLISECONDS)
        RESULT = TIMER.get_duration_string()
        self.assertTrue(RESULT == "0.123\"" or RESULT == "0.124\"")

if __name__ == '__main__':
    unittest.main()
