"""module docstring should be here"""

from formatting import format_float

from sphere import Sphere


class OpticalSphere(Sphere):
    N: float

    def __new__(cls, radius):
        return object.__new__(cls)

    def __init__(self, radius):
        Sphere.__init__(self, center=(0, 0, 0), radius=radius)
        self.N = 1.53

    def __str__(self):
        return f'OpticalSphere(radius: {format_float(self.radius)} mm, n: {format_float(self.N)})'

    def get_n(self):
        return self.N
        
    def get_surface_power(self):
        return 530/self.radius

    def get_base_curve(self):
        n_vacuum = 1
        return 1000*(self.N - n_vacuum)/self.radius

    def spy(self, message):
        print(f'{self}: {message}')


def print_optical_info(radius):
    optical_sphere = OpticalSphere(radius=radius)
    print(f'optical_sphere: {optical_sphere}')
    print(f'  |- surface power is {format_float(optical_sphere.get_surface_power())} diopter(s)')
    print(f"  '- base curve is {format_float(optical_sphere.get_base_curve())} diopter(s)")


def main():
    radius_int = 530  # 530 mm is the radius of a 1 diopter curve
    print_optical_info(radius_int)

    radius_int = 106
    print_optical_info(radius_int)

    radius_int = 53
    print_optical_info(radius_int)

    radius_float = 123.456789
    print_optical_info(radius_float)


if __name__ == '__main__':
    main()
