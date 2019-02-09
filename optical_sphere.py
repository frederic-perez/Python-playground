'module docstring should be here'

#import math
import numpy as np
from sphere import Sphere

class OpticalSphere(Sphere):
    def __init__(self, radius, n):
        CENTER = np.zeros(3)
        Sphere.__init__(self, CENTER, radius)
        self.n = n
        return

    def __str__(self):
        return 'OpticalSphere(radius={0}, n={1})'.format(self.radius, self.n)

    def get_n(self):
        return self.n

    def get_base_curve(self):
        N_VACUUM = 1
        return (self.n - N_VACUUM)/self.radius

    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

if __name__ == '__main__':
    RADIUS = 0.1
    N = 1.5
    OPTICAL_SPHERE = OpticalSphere(RADIUS, N)
    print "OPTICAL_SPHERE:", OPTICAL_SPHERE
    print "  '- base curve is", OPTICAL_SPHERE.get_base_curve(), "diopters"
