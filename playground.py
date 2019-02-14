'module docstring should be here'

import numpy as np
from sphere import \
    Sphere, get_sphere, epsilon_distance, equal_in_practice, zero_in_practice

def average(*numbers):
    """Self-explanatory"""
    if not numbers:
        raise ValueError('numbers should not be empty')

    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))

def get_sphere_given4StraightCrosshairPoints_From_42():
    POINT_1 = np.array([-35.3025, 0.6357,   3.8584], np.float_)
    POINT_2 = np.array([-35.0932, 1.3599, -43.2535], np.float_)
    POINT_3 = np.array([ -9.054, -0.958,  -19.6768], np.float_)
    POINT_4 = np.array([-62.0412, 5.9778, -19.7658], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_42 = get_sphere(POINTS)
    print "SPHERE_42 given 4 straight crosshair points", SPHERE_42

def get_sphere_given4RotatedCrosshairPoints_From_42():
    POINT_1 = np.array([-58.7767,  4.9348,    -3.7779], np.float_)
    POINT_2 = np.array([-13.3565, -0.644701, -29.8066], np.float_)
    POINT_3 = np.array([-16.4319, -0.999301,   1.6949], np.float_)
    POINT_4 = np.array([-55.543,   4.7384,   -37.1852], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_42 = get_sphere(POINTS)
    print "SPHERE_42 given 4 rotated crosshair points", SPHERE_42

def get_sphere_given4StraightCrosshairPoints_From_46():
    POINT_1 = np.array([-36.9284,  2.1009,  -1.0189], np.float_)
    POINT_2 = np.array([-37.0922,  2.2078, -51.4502], np.float_)
    POINT_3 = np.array([-10.4147, -0.1741, -26.0583], np.float_)
    POINT_4 = np.array([-65.5153,  8.0756, -26.2123], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_46 = get_sphere(POINTS)
    print "SPHERE_46 given 4 straight crosshair points", SPHERE_46

def get_sphere_given4RotatedCrosshairPoints_From_46():
    POINT_1 = np.array([-56.2434, 5.6835, -8.3162], np.float_)
    POINT_2 = np.array([-15.5323, 0.0641003, -37.5089], np.float_)
    POINT_3 = np.array([-54.5831, 5.3886, -44.8675], np.float_)
    POINT_4 = np.array([-18.2069, 0.2075, -3.8871], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_46 = get_sphere(POINTS)
    print "SPHERE_46 given 4 rotated crosshair points", SPHERE_46

if __name__ == '__main__':

    get_sphere_given4StraightCrosshairPoints_From_42()
    get_sphere_given4RotatedCrosshairPoints_From_42()
    print
    get_sphere_given4StraightCrosshairPoints_From_46()
    get_sphere_given4RotatedCrosshairPoints_From_46()
    print
