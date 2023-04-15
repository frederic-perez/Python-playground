"""module docstring should be here"""

import numpy as np
from formatting import float_formatter

from sphere import Sphere


class OpticalSphere(Sphere):
    def __init__(self, radius):
        center = np.zeros(3)
        Sphere.__init__(self, center, radius)
        self.N = 1.53
        return

    def __str__(self):
        return 'OpticalSphere(radius: {} mm, n: {})'.format(float_formatter(self.radius), float_formatter(self.N))

    def get_n(self):
        return self.N
        
    def get_surface_power(self):
        return 530/self.radius

    def get_base_curve(self):
        n_vacuum = 1
        return 1000*(self.N - n_vacuum)/self.radius

    def spy(self, message):
        print('{}: {}'.format(message, self))
        return


def print_optical_info(radius):
    optical_sphere = OpticalSphere(radius)
    print("OPTICAL_SPHERE:", optical_sphere)
    print("  |- surface power is {} diopter(s)".format(float_formatter(optical_sphere.get_surface_power())))
    print("  '- base curve is {} diopter(s)".format(float_formatter(optical_sphere.get_base_curve())))
    print()


if __name__ == '__main__':
    
    radius = 530  # 530 mm is the radius of a 1 diopter curve
    print_optical_info(radius)

    radius = 106
    print_optical_info(radius)

    radius = 53
    print_optical_info(radius)

    radius = 123.456789
    print_optical_info(radius)
