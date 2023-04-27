"""
Code originally based on a response in
https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
"""

import time


class Timer:
    start: float

    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_duration_string(self):
        duration = time.time() - self.start
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
            return f"{h}h {m}' {s}.{cs:02g}\""
        if m > 0:
            return f"{m}' {s}.{cs:02g}\""
        return f'{s}.{cs:02g}"'


def main():
    timer = Timer()
    time.sleep(.12345678)  # 61.2345678)
    duration_string = timer.get_duration_string()
    print(f'`main` took {duration_string}')


if __name__ == '__main__':
    main()
