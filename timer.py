"""
Code originarily based on a response in
https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
"""

import time

class Timer:
  def __init__(self):
    self.start = time.time()

  def restart(self):
    self.start = time.time()

  def get_duration_string(self):
    duration = time.time() - self.start()
    _, ms = divmod(duration, 1)
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    if h > 0:
        time_string = "%02d:%02d:%02d.%02d" % (h, m, s, ms)
    else:
        time_string = "%02d:%02d.%02d" % (m, s, ms)
    return time_string

