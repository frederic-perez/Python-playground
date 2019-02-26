'module docstring should be here'

#import math
import numpy as np
from sphere import Sphere

class OpticalSphere(Sphere):
    def __init__(self, base_curve):
        CENTER = np.zeros(3)
        N = 1.53
        N_VACUUM = 1
        RADIUS = 1000*(N - N_VACUUM)/base_curve
        Sphere.__init__(self, CENTER, RADIUS)
        self.base_curve = base_curve
        self.N = N
        return

    def __str__(self):
        return 'OpticalSphere(base_curve: {0} mm, n: {1})'.format(self.base_curve, self.N)

    def get_base_curve(self):
        return self.base_curve

    def get_n(self):
        return self.N
        
    def get_surface_power(self):
        return 530/self.radius

    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

def print_optical_info(base_curve):
    OPTICAL_SPHERE = OpticalSphere(base_curve)
    print "OPTICAL_SPHERE:", OPTICAL_SPHERE
    print "  |- base curve is", OPTICAL_SPHERE.get_base_curve(), "diopter(s)"
    print "  |- surface power is", OPTICAL_SPHERE.get_surface_power(), "diopter(s)"
    print "  '- radius is", OPTICAL_SPHERE.get_radius(), "mm"
    print

if __name__ == '__main__':
    
    base_curve = 1 # 1 diopter curve
    print_optical_info(base_curve)

    base_curve = 5
    print_optical_info(base_curve)
