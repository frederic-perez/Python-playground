'module docstring should be here'

import math
import numpy as np
import os.path
from sphere import Sphere

def get_pringle_points(num_points, a, b, radius, offset_xyz, max_noise = 0.):
    points = np.random.rand(num_points, 3)
    A_SQR = a*a
    B_SQR = b*b
    for i in range(num_points):
        print "i is", i
        alpha = i * 2*math.pi/num_points
        x = offset_xyz[0] + radius * math.cos(alpha)
        y = offset_xyz[1] + radius * math.sin(alpha)
        z = offset_xyz[2] + y*y/B_SQR - x*x/A_SQR # https://en.wikipedia.org/wiki/Paraboloid
        if (max_noise > 0.):
            x += max_noise * (np.random.random_sample() - .5)
            y += max_noise * (np.random.random_sample() - .5)
            z += max_noise * (np.random.random_sample() - .5)
        point = np.zeros(3)
        point[0] = x
        point[1] = y
        point[2] = z
        points[i] = point
    return points

def get_distances_to_sphere_and_scaled_normals(points, sphere):
    print "sphere is", sphere
    NUM_POINTS = len(points)
    distances = [0] * NUM_POINTS
    scaled_normals = np.random.rand(NUM_POINTS, 3)
    CENTER = sphere.get_center()
    for i in range(NUM_POINTS):
        point = points[i]
        distance = sphere.get_signed_distance_to_surface(point)
        print "distance for point", i, '=', point, "is", distance
        distances[i] = distance
        scaled_normal = np.zeros(3)
        vector = CENTER - point
        magnitude = np.linalg.norm(vector)
        for k in range(3):
            scaled_normal[k] = distance * vector[k]/magnitude
        scaled_normals[i] = scaled_normal
    return distances, scaled_normals

def save_xyz_file(filename_xyz, points):
    file = open(filename_xyz, 'w')

    NUM_POINTS = len(points)
    for point in points:
        LINE = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
        file.write(LINE)

    file.close()

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
            try:
                xyz = list(map(np.float, line.split()))
            except ValueError as e:
                raise ValueError('Exception caught when reading point #' + str(i) + ' | ' + str(e))
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
    HEADER = ("ply\n"
              "format ascii 1.0\n"
              "element vertex " + str(NUM_POINTS) + "\n"
              "property float x\n"
              "property float y\n"
              "property float z\n"
              "end_header\n")
    file.write(HEADER)
    for point in points:
        LINE = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
        file.write(LINE)
    file.close()

def save_ply_file_with_distances_and_scaled_normals(filename_ply, points, distances, scaled_normals):
    """
    Here we use the information given by Cory Quammen (from Kitware)
    in https://public.kitware.com/pipermail/paraview/2018-March/042164.html:

    > I believe you are running into a limitation of the PLY reader in VTK, which
    > is what ParaView uses to read PLY files. I'm afraid it does not read
    > arbitrary properties from PLY files. It will read only vertex properties
    > named "x", "y", "z", "u","v", "nx", "ny", "nz", "red", "green", "blue", and
    > "alpha" and face properties named "vertex_indices", "intensity", "red",
    > "green", "blue", and "alpha".

    Credits for Cory Quammen to provide the hint to write this function.
    """
    file = open(filename_ply, 'w')

    NUM_POINTS = len(points)
    HEADER = ("ply\n"
              "format ascii 1.0\n"
              "element vertex " + str(NUM_POINTS) + "\n"
              "property float x\n"
              "property float y\n"
              "property float z\n"
              "property float u\n"
              "property float v\n"
              "property float nx\n"
              "property float ny\n"
              "property float nz\n"
              "end_header\n")
    file.write(HEADER)
    for i in range(NUM_POINTS):
        point = points[i]
        distance = distances[i]
        scaled_normal = scaled_normals[i]
        LINE = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) \
            + ' ' + str(distance) + ' 0' \
            + ' ' + str(scaled_normal[0]) + ' ' + str(scaled_normal[1]) + ' ' + str(scaled_normal[2]) + '\n'
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

def save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(filename_xyz_in, sphere, filename_ply_out):
    if not filename_xyz_in:
        raise ValueError('Input filename should not be empty')
    if not os.path.exists(filename_xyz_in):
        raise IOError('Input file does not exist')
    if not filename_ply_out:
        raise ValueError('Output filename should not be empty')

    POINTS = read_xyz_file(filename_xyz_in)
    DISTANCES, SCALED_NORMALS = get_distances_to_sphere_and_scaled_normals(POINTS, sphere)
    save_ply_file_with_distances_and_scaled_normals(filename_ply_out, POINTS, DISTANCES, SCALED_NORMALS)

def play_with_a_pringle():
    PRINGLE_FILENAME_XYZ = 'data/pringle.xyz'
    NUM_PRINGLE_POINTS = 10 # 100
    PRINGLE_A = 8
    PRINGLE_B = 4
    PRINGLE_RADIUS = 5
    PRINGLE_OFFSET = [0, 0, 4]
    PRINGLE_POINTS = get_pringle_points(
        NUM_PRINGLE_POINTS,
        PRINGLE_A,
        PRINGLE_B,
        PRINGLE_RADIUS,
        PRINGLE_OFFSET)
    save_xyz_file(PRINGLE_FILENAME_XYZ, PRINGLE_POINTS)
    PRINGLE_FILENAME_PLY = 'data/pringle.ply'
    SPHERE_CENTER = np.array([0, 0, 0], np.float_)
    SPHERE_RADIUS = 6.8
    SPHERE = Sphere(SPHERE_CENTER, SPHERE_RADIUS)
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(PRINGLE_FILENAME_XYZ, SPHERE, PRINGLE_FILENAME_PLY)

def play_with_a_pringle_with_noise():
    PRINGLE_FILENAME_XYZ = 'data/pringle-with-noise.xyz'
    NUM_PRINGLE_POINTS = 10 # 100
    PRINGLE_A = 8
    PRINGLE_B = 4
    PRINGLE_RADIUS = 5
    PRINGLE_OFFSET = [0, 0, 4]
    PRINGLE_MAX_NOISE = .15
    PRINGLE_POINTS = get_pringle_points(
        NUM_PRINGLE_POINTS,
        PRINGLE_A,
        PRINGLE_B,
        PRINGLE_RADIUS,
        PRINGLE_OFFSET,
        PRINGLE_MAX_NOISE)
    save_xyz_file(PRINGLE_FILENAME_XYZ, PRINGLE_POINTS)
    PRINGLE_FILENAME_PLY = 'data/pringle-with-noise.ply'
    SPHERE_CENTER = np.array([0, 0, 0], np.float_)
    SPHERE_RADIUS = 6.8
    SPHERE = Sphere(SPHERE_CENTER, SPHERE_RADIUS)
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(PRINGLE_FILENAME_XYZ, SPHERE, PRINGLE_FILENAME_PLY)

if __name__ == '__main__':
    FILENAME_IN = 'data/points-in.xyz'
    FILENAME_OUT = 'data/points-out.ply'
    save_as_ply(FILENAME_IN, FILENAME_OUT)

    print

    play_with_a_pringle()

    print

    play_with_a_pringle_with_noise()
