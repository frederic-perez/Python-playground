'module docstring should be here'

import numpy as np
import os.path

def print_a_few_points(points):
    print "point #", 0, "is", points[0]
    print "..."
    LAST_INDEX = len(points) - 1
    print "point #", LAST_INDEX, "is", points[LAST_INDEX]

def read_xyz_file(filename_xyz):
    file_in = open(filename_xyz, 'r')
    num_points = 0
    for line in file_in:
        if line.strip():
            num_points += 1

    file_in.seek(0)

    if num_points == 0:
        raise ValueError('No input points have been retrieved')

    points = np.random.rand(num_points, 3)
    i = 0
    for line in file_in:
        if line.strip():
            xyz = list(map(np.float, line.split()))
            point = np.zeros(3)
            for idx in range(3):
               point[idx] = xyz[idx]
            points[i] = point
            i += 1
    file_in.close()

    print_a_few_points(points)

    return points

def save_ply_file(filename_ply, points):
    file = open(filename_ply, 'w')

    NUM_POINTS = len(points)
    file.write("ply\n")
    file.write("format ascii 1.0\n")
    file.write("element vertex " + str(NUM_POINTS) + "\n")
    file.write("property float x\n")
    file.write("property float y\n")
    file.write("property float z\n")
    file.write("end_header\n")
    for point in points:
        LINE = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
        file.write(LINE)
    file.close()

def save_as_ply(filename_xyz_in, filename_ply_out):
    if not filename_xyz_in:
        raise ValueError('Input filename should not be empty')
    if not os.path.exists(filename_xyz_in):
        raise IOError('Input file does not exist')
    if not filename_ply_out:
        raise ValueError('Output filename should not be empty')

    POINTS = read_xyz_file(filename_xyz_in)
    save_ply_file(filename_ply_out, POINTS)

if __name__ == '__main__':
    FILENAME_IN = 'data/points_in.xyz'
    FILENAME_OUT = 'data/points_out.ply'
    save_as_ply(FILENAME_IN, FILENAME_OUT)
