"""
Code originally based on a response in
https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
"""

import time
from timeit import default_timer


class Timer:
    start: float
    elapsed: str

    def __init__(self):
        self._start = default_timer()
        self._elapsed = ''

    def __enter__(self):
        self._start = default_timer()
        self._elapsed = ''
        return self

    def __exit__(self, the_type, the_value, the_traceback):
        self.set_elapsed()

    def restart(self):
        self._start = default_timer()

    def set_elapsed(self):
        duration = default_timer() - self._start
        _, cs = divmod(duration, 1)
        cs = 100*round(cs, 2)  # ms = 1000*round(ms, 3) if we want ms instead of cs
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)

        # print(f'» types of h, m, s, and cs are {type(h)}, {type(m)}, {type(s)}, and {type(s)}')  # all <class 'float'>
        # print(f'» cs is {cs}')

        h = int(h)
        m = int(m)
        s = int(s)
        # print(f'» types of h, m, s, and cs are {type(h)}, {type(m)}, {type(s)}, and {type(s)}')  # all <class 'int'>

        # We use primes for compact representation of duration See
        # https://english.stackexchange.com/questions/114205/english-notation-for-hour-minutes-and-seconds
        #
        if h > 0:
            self._elapsed = f"{h}h {m}' {s}.{cs:02g}\""
        elif m > 0:
            self._elapsed = f"{m}' {s}.{cs:02g}\""
        else:
            self._elapsed = f'{s}.{cs:02g}"'

    def elapsed(self):
        self.set_elapsed()
        return self._elapsed


def main():
    timer = Timer()
    time.sleep(.12345678)  # 61.2345678)
    print(f'First `sleep` took {timer.elapsed()}')

    timer.restart()
    print(f'After `restart` {timer.elapsed()} have passed')

    with Timer() as timer_for_context:
        time.sleep(.2468)
    print(f'After context {timer_for_context.elapsed()} have passed')


if __name__ == '__main__':
    main()
