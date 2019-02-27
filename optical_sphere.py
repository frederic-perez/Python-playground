'module docstring should be here'

#import math
import numpy as np
from sphere import Sphere

class OpticalSphere(Sphere):
    def __init__(self, radius):
        CENTER = np.zeros(3)
        Sphere.__init__(self, CENTER, radius)
        self.N = 1.53
        return

    def __str__(self):
        return 'OpticalSphere(radius: {0} mm, n: {1})'.format(self.radius, self.N)

    def get_n(self):
        return self.N
        
    def get_surface_power(self):
        return 530/self.radius

    def get_base_curve(self):
        N_VACUUM = 1
        return 1000*(self.N - N_VACUUM)/self.radius

    def spy(self, message):
        print '{0}: {1}'.format(message, self)
        return

def print_optical_info(base_curve):
    OPTICAL_SPHERE = OpticalSphere(base_curve)
    print "OPTICAL_SPHERE:", OPTICAL_SPHERE
    print "  |- surface power is", OPTICAL_SPHERE.get_surface_power(), "diopter(s)"
    print "  '- base curve is", OPTICAL_SPHERE.get_base_curve(), "diopter(s)"
    print

if __name__ == '__main__':
    
    radius = 530 # 530 mm is the radius of a 1 diopter curve
    print_optical_info(radius)

    radius = 106
    print_optical_info(radius)
