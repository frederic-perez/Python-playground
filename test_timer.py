"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_timer.py
  or
  $ python test_timer.py
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
        X_MILLISECONDS = 0.123
        TIMER = Timer()
        sleep(X_MILLISECONDS)
        RESULT = TIMER.get_duration_string()
        RESULT_TRIMMED = RESULT.replace("\"", "")
        IT_IS_CLOSE_ENOUGH = float(RESULT_TRIMMED) - X_MILLISECONDS <= 0.003
        if not IT_IS_CLOSE_ENOUGH:
            print("Too bad: RESULT is {}, too far from {}".format(RESULT, X_MILLISECONDS))
        self.assertTrue(IT_IS_CLOSE_ENOUGH)

if __name__ == '__main__':
    unittest.main()
