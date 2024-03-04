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

    def test_GivenATimerAnd0msPass_When_elapsed_ThenReturnElapsedCloseTo0ms(self):
        timer = Timer()
        result = timer.elapsed()
        self.assertTrue(result == '0.0 seconds' or result == '0.1 seconds')

    def test_GivenATimerAndXmsPass_When_elapsed_ThenReturnElapsedCloseToXms(self):
        x_milliseconds = 0.123
        timer = Timer()
        sleep(x_milliseconds)
        result = timer.elapsed()
        result_trimmed = result.replace(" seconds", "")
        it_is_close_enough = float(result_trimmed) - x_milliseconds <= 0.003
        if not it_is_close_enough:
            print(f'Too bad: result is {result}, too far from {x_milliseconds}')
        self.assertTrue(it_is_close_enough)


if __name__ == '__main__':
    unittest.main()
