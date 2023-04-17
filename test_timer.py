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
        timer = Timer()
        result = timer.get_duration_string()
        self.assertTrue(result == "0.000\"" or result == "0.001\"")

    def test_GivenATimerAndXmsPass_When_get_duration_string_ThenReturnDurationCloseToXms(self):
        x_milliseconds = 0.123
        timer = Timer()
        sleep(x_milliseconds)
        result = timer.get_duration_string()
        result_trimmed = result.replace("\"", "")
        it_is_close_enough = float(result_trimmed) - x_milliseconds <= 0.003
        if not it_is_close_enough:
            print("Too bad: result is {}, too far from {}".format(result, x_milliseconds))
        self.assertTrue(it_is_close_enough)


if __name__ == '__main__':
    unittest.main()
