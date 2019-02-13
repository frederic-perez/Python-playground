'module docstring should be here'

import numpy as np
import os.path
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

def write_ply_header(file_ply_out, num_points):
    file_ply_out.write("ply\n")
    file_ply_out.write("format ascii 1.0\n")
    file_ply_out.write("element vertex " + str(num_points) + "\n")
    file_ply_out.write("property float x\n")
    file_ply_out.write("property float y\n")
    file_ply_out.write("property float z\n")
    file_ply_out.write("end_header\n")

def write_ply_body(file_ply_out, points):
    for point in points:
        x = str(point[0])
        y = str(point[1])
        z = str(point[2])
        file_ply_out.write(x + ' ' + y + ' ' + z + '\n')

def save_as_ply(filename_xyz_in, filename_ply_out):
    if not filename_xyz_in:
        raise ValueError('Input filename should not be empty')
    if not os.path.exists(filename_xyz_in):
        raise IOError('Input file does not exist')
    if not filename_ply_out:
        raise ValueError('Output filename should not be empty')

    file_in = open(filename_xyz_in, 'r')
    num_points = 0
    for line in file_in:
        if line.strip():
            num_points += 1

    file_in.seek(0)

    points = np.random.rand(num_points, 3)
    i = 0
    for line in file_in:
        if line.strip():
            xyz = list(map(np.float, line.split()))
            point = np.zeros(3)
            point[0] = xyz[0]
            point[1] = xyz[1]
            point[2] = xyz[2]
            print "point #", i, "is", point
            points[i] = point
            i += 1
    file_in.close()

    file_out = open(filename_ply_out, 'w')
    write_ply_header(file_out, num_points)
    write_ply_body(file_out, points)
    file_out.close()

if __name__ == '__main__':

    get_sphere_given4StraightCrosshairPoints_From_42()
    get_sphere_given4RotatedCrosshairPoints_From_42()
    print
    get_sphere_given4StraightCrosshairPoints_From_46()
    get_sphere_given4RotatedCrosshairPoints_From_46()
    print

    FILENAME_IN = 'data/points_in.xyz'
    FILENAME_OUT = 'data/points_out.ply'
    save_as_ply(FILENAME_IN, FILENAME_OUT)
