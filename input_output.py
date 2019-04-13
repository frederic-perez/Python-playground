'module docstring should be here'

import math
import numpy as np
import os.path
from sphere import Sphere, get_best_fit_sphere, get_best_fit_sphere_for_radius_range
from optical_sphere import OpticalSphere

"""
TODO: Implement function `verify-contour-on-sphere` that reads a set of points,
and does a loop for alpha ranging from 0 to 85 degrees (delta = 5; i x delta),
retrieving the four points closest to the cross-mark lines, compute the sphere
that passes through those points, and save them to study the variability of
centers and radii.
"""

def get_pringle_points(num_points, a, b, radius_x, radius_z, offset_xyz, max_noise = 0.):
    points = np.random.rand(num_points, 3)
    A_SQR = a**2
    B_SQR = b**2
    for i in range(num_points):
        print "i is", i
        alpha = i * 2*math.pi/num_points
        x = radius_x * math.sin(alpha)
        z = radius_z * math.cos(alpha)
        y = z*z/B_SQR - x*x/A_SQR # https://en.wikipedia.org/wiki/Paraboloid
        point = np.zeros(3)
        point[0] = x + offset_xyz[0]
        point[1] = y + offset_xyz[1]
        point[2] = z + offset_xyz[2]
        if (max_noise > 0.):
            for j in range(3):
                point[j] += max_noise * (np.random.random_sample() - .5)
        points[i] = point
    return points

def get_distances_to_sphere_and_scaled_normals(points, sphere):
    FUNCTION_NAME = 'get_distances_to_sphere_and_scaled_normals:'
    print FUNCTION_NAME, "sphere is", sphere
    NUM_POINTS = len(points)
    distances = [0] * NUM_POINTS
    scaled_normals = np.random.rand(NUM_POINTS, 3)
    CENTER = sphere.get_center()
    max_negative_distance = float("inf")
    max_positive_distance = -float("inf")
    for i in range(NUM_POINTS):
        point = points[i]
        distance = sphere.get_signed_distance_to_surface(point)
        max_negative_distance = min(max_negative_distance, distance)
        max_positive_distance = max(max_positive_distance, distance)
        # print "distance for point", i, '=', point, "is", distance
        distances[i] = distance
        scaled_normal = np.zeros(3)
        vector = CENTER - point
        magnitude = np.linalg.norm(vector)
        for k in range(3):
            scaled_normal[k] = distance * vector[k]/magnitude
        scaled_normals[i] = scaled_normal
    print FUNCTION_NAME, "max_negative_distance is", max_negative_distance, "| max_positive_distance is", max_positive_distance
    return distances, scaled_normals

def save_xyz_file(filename_xyz, points):
    file = open(filename_xyz, 'w')

    NUM_POINTS = len(points)
    for point in points:
        LINE = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n'
        file.write(LINE)

    file.close()

def print_a_few_points(points):
    FUNCTION_NAME = 'print_a_few_points:'
    print FUNCTION_NAME, "point #", 0, "is", points[0]
    print FUNCTION_NAME, "..."
    LAST_INDEX = len(points) - 1
    print FUNCTION_NAME, "point #", LAST_INDEX, "is", points[LAST_INDEX]

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
    PRINGLE_RADIUS_X = 5
    PRINGLE_RADIUS_Z = 5
    PRINGLE_OFFSET = [0, 4, 0]
    PRINGLE_POINTS = get_pringle_points(
        NUM_PRINGLE_POINTS,
        PRINGLE_A,
        PRINGLE_B,
        PRINGLE_RADIUS_X,
        PRINGLE_RADIUS_Z,
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
    PRINGLE_RADIUS_X = 5
    PRINGLE_RADIUS_Z = 5
    PRINGLE_OFFSET = [0, 0, 4]
    PRINGLE_MAX_NOISE = .15
    PRINGLE_POINTS = get_pringle_points(
        NUM_PRINGLE_POINTS,
        PRINGLE_A,
        PRINGLE_B,
        PRINGLE_RADIUS_X,
        PRINGLE_RADIUS_Z,
        PRINGLE_OFFSET,
        PRINGLE_MAX_NOISE)
    save_xyz_file(PRINGLE_FILENAME_XYZ, PRINGLE_POINTS)
    PRINGLE_FILENAME_PLY = 'data/pringle-with-noise.ply'
    SPHERE_CENTER = [0, 0, 0]
    SPHERE_RADIUS = 6.8
    SPHERE = Sphere(SPHERE_CENTER, SPHERE_RADIUS)
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(PRINGLE_FILENAME_XYZ, SPHERE, PRINGLE_FILENAME_PLY)

def play_with_a_pringle_like_whatnot_42_with_noise():
    PRINGLE_FILENAME_XYZ = 'data/pringle-like-whatnot-42-with-noise.xyz'
    NUM_PRINGLE_POINTS = 10 # 100
    PRINGLE_A = 15 # 20
    PRINGLE_B = 20 # 15
    PRINGLE_RADIUS_X = 22 # 26
    PRINGLE_RADIUS_Z = 26 # 22
    PRINGLE_OFFSET = [-35, 0, -20]
    PRINGLE_MAX_NOISE = .5
    PRINGLE_POINTS = get_pringle_points(
        NUM_PRINGLE_POINTS,
        PRINGLE_A,
        PRINGLE_B,
        PRINGLE_RADIUS_X,
        PRINGLE_RADIUS_Z,
        PRINGLE_OFFSET,
        PRINGLE_MAX_NOISE)
    save_xyz_file(PRINGLE_FILENAME_XYZ, PRINGLE_POINTS)
    PRINGLE_FILENAME_PLY = 'data/pringle-like-whatnot-42-with-noise.ply'
    # SPHERE_CENTER = [PRINGLE_OFFSET[0], 0, PRINGLE_OFFSET[2]]
    SPHERE_Y_RANGE = [0, 500]
    SPHERE_RADIUS = 106 # 6.8
    # SPHERE = Sphere(SPHERE_CENTER, SPHERE_RADIUS)
    SPHERE = get_best_fit_sphere(PRINGLE_POINTS, PRINGLE_OFFSET[0], PRINGLE_OFFSET[2], SPHERE_Y_RANGE, SPHERE_RADIUS)
    print "Best fit sphere for the pringle like whatnot-42 is", SPHERE
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(PRINGLE_FILENAME_XYZ, SPHERE, PRINGLE_FILENAME_PLY)

def get_points_rotated_around_z(points, theta):
    rotated_points = []
    COS_THETA = math.cos(theta)
    SIN_THETA = math.sin(theta)
    for point in points:
        rotated_point = [
            point[0]*COS_THETA + point[1]*SIN_THETA,
            point[0]*(-SIN_THETA) + point[1]*COS_THETA,
            point[2]]
        rotated_points.append(rotated_point)
    return rotated_points

def get_bounding_box(points):
    x_coords, y_coords, z_coords = zip(*points)
    return [
        [min(x_coords), max(x_coords)],
        [min(y_coords), max(y_coords)],
        [min(z_coords), max(z_coords)]]

def get_center(bounding_box):
    center = [0] * 3
    for i in range(3):
        center[i] = (bounding_box[i][1] - bounding_box[i][0])/2. + bounding_box[i][0]
    return center

def study_contour(contour_ID, tilt):
    print 'study_contour(' + contour_ID + ', ' + str(tilt) + ") starts..."
    FILENAME_CONTOUR_XYZ = 'data/_contour-' + contour_ID + '.xyz'
    POINTS = read_xyz_file(FILENAME_CONTOUR_XYZ)
    THETA = math.radians(-tilt)
    ROTATED_POINTS = get_points_rotated_around_z(POINTS, THETA)
    FILENAME_CONTOUR_ROTATED_BASE = 'data/_contour-' + contour_ID + '-rotated'
    FILENAME_CONTOUR_ROTATED_XYZ = FILENAME_CONTOUR_ROTATED_BASE + '.xyz'
    FILENAME_CONTOUR_ROTATED_PLY = FILENAME_CONTOUR_ROTATED_BASE + '.ply'
    save_xyz_file(FILENAME_CONTOUR_ROTATED_XYZ, ROTATED_POINTS)
    save_ply_file(FILENAME_CONTOUR_ROTATED_PLY, ROTATED_POINTS)

    BOUNDING_BOX = get_bounding_box(ROTATED_POINTS)
    CENTER = get_center(BOUNDING_BOX)
    CENTER_X_AND_Z = [CENTER[0], CENTER[2]]
    SPHERE_Y_RANGE = [0, 500]
    SPHERE_RADIUS_RANGE = [40., 1000.]
    USE_MSE = True
    NUM_SAMPLES = 9
    SPHERE = get_best_fit_sphere_for_radius_range(ROTATED_POINTS, CENTER_X_AND_Z, SPHERE_Y_RANGE, SPHERE_RADIUS_RANGE, USE_MSE, NUM_SAMPLES)
    print "Best fit sphere for", FILENAME_CONTOUR_XYZ, "is", SPHERE, "| Base is", OpticalSphere(SPHERE.get_radius()).get_base_curve()

    FILENAME_CONTOUR_STUDY_RESULTS_PLY = 'data/_contour-' + contour_ID + '-study-results.ply'
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(
        FILENAME_CONTOUR_ROTATED_XYZ, SPHERE, FILENAME_CONTOUR_STUDY_RESULTS_PLY)

if __name__ == '__main__':
    """
    FILENAME_IN = 'data/points-in.xyz'
    FILENAME_OUT = 'data/points-out.ply'
    save_as_ply(FILENAME_IN, FILENAME_OUT)

    print
    play_with_a_pringle()

    print
    play_with_a_pringle_with_noise()

    print
    play_with_a_pringle_like_whatnot_42_with_noise()

    print
    play_with_a_pringle_like_whatnot_42_with_noise()
    """

    CONTOUR_ID_AND_TILT_ARRAY = [
        ['41', 5],
        ['42', 7],
        ['43', 6],
        ['44', 5],
        ['45', 9],
        ['46', 8],
        ['47', 7],
        ['48', 4]
    ]
    """
        ['41', 5],
        ['42', 7],
        ['43', 6],
        ['44', 5],
        ['45', 9],
        ['46', 8],
        ['47', 7],
        ['48', 4]
    ]
    """
    for contour_ID_and_tilt in CONTOUR_ID_AND_TILT_ARRAY:
        contour_ID, tilt = contour_ID_and_tilt
        study_contour(contour_ID, tilt)
        print
