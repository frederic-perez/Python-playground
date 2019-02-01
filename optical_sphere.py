'module docstring should be here'

#import math
import numpy as np
from sphere import Sphere

class OpticalSphere(Sphere):
    def __init__(self, center, radius, n):
        Sphere.__init__(self, center, radius)
        self.n = n
        return

    def __str__(self):
        return 'OpticalSphere(center={0}, radius={1}, n={2})'.format(self.center, self.radius, self.n)

    def get_n(self):
        return self.n

    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

CENTER = np.array([1, 2, 3], np.float_)
RADIUS = 7
N = 1.5
OPTICAL_SPHERE = OpticalSphere(CENTER, RADIUS, N)
OPTICAL_SPHERE.spy("OPTICAL_SPHERE")
print "OPTICAL_SPHERE:", OPTICAL_SPHERE
