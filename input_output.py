'module docstring should be here'

import math
import numpy as np
import os.path

import check
from formatting import float_formatter, floats_formatter, floats_HQ_formatter
from sphere import Sphere, get_best_fit_sphere, get_best_fit_sphere_for_radius_range, get_sphere
from optical_sphere import OpticalSphere

def get_pringle_points(num_points, a, b, radius_x, radius_z, offset_xyz, max_noise = 0.):
    points = np.random.rand(num_points, 3)
    A_SQR = a**2
    B_SQR = b**2
    for i in range(num_points):
        # print("i is", i)
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
    # print(FUNCTION_NAME, "sphere is", sphere)
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
        # print("distance for point", i, '=', point, "is", distance)
        distances[i] = distance
        scaled_normal = np.zeros(3)
        vector = CENTER - point
        magnitude = np.linalg.norm(vector)
        for k in range(3):
            scaled_normal[k] = distance * vector[k]/magnitude
        scaled_normals[i] = scaled_normal
    print(FUNCTION_NAME, "max_negative_distance is {:.3f} | max_positive_distance is {:.3f}".format(max_negative_distance, max_positive_distance))
    return distances, scaled_normals

np.set_printoptions(formatter={'float_kind':float_formatter})

def save_xyz_file(filename_xyz, points):
    file_out = open(filename_xyz, 'w')

    for point in points:
        print("{}".format(floats_formatter(point)), file=file_out)

    file_out.close()

def print_a_few_points(points):
    FUNCTION_NAME = 'print_a_few_points:'
    print(FUNCTION_NAME, "point #", 0, "is", points[0])
    print(FUNCTION_NAME, "...")
    LAST_INDEX = len(points) - 1
    print(FUNCTION_NAME, "point #", LAST_INDEX, "is", points[LAST_INDEX])

def read_xyz_file(filename_xyz):
    file_in = open(filename_xyz, 'r')
    num_points = 0
    for line in file_in:
        if line.strip():
            num_points += 1

    file_in.seek(0)

    if num_points == 0:
        file_in.close()
        raise ValueError('No input points have been retrieved')

    points = np.random.rand(num_points, 3)
    i = 0
    for line in file_in:
        if line.strip():
            try:
                xyz = list(map(np.float64, line.split()))
            except ValueError as e:
                file_in.close()
                raise ValueError('Exception caught when reading point #' + str(i) + ' | ' + str(e))
            point = np.zeros(3)
            for idx in range(3):
                point[idx] = xyz[idx]
            points[i] = point
            i += 1
    file_in.close()

    PRINT_A_FEW_POINTS = False
    if PRINT_A_FEW_POINTS:
        print_a_few_points(points)

    return points

def save_ply_file(filename_ply, points):
    file_out = open(filename_ply, 'w')

    NUM_POINTS = len(points)
    HEADER = ("ply\n"
              "format ascii 1.0\n"
              "element vertex " + str(NUM_POINTS) + "\n"
              "property float x\n"
              "property float y\n"
              "property float z\n"
              "end_header\n")
    file_out.write(HEADER)
    for point in points:
        # print("{}".format(floats_formatter(point)), file=file_out)
        print("{}".format(floats_HQ_formatter(point)), file=file_out)
    file_out.close()

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
    file_out = open(filename_ply, 'w')

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
    file_out.write(HEADER)
    for i in range(NUM_POINTS):
        point = points[i]
        distance = distances[i]
        scaled_normal = scaled_normals[i]
        print("{} {} 0 {}".format(
            floats_formatter(point),
            float_formatter(distance),
            floats_formatter(scaled_normal)),
            file=file_out)
    file_out.close()

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
    SPHERE_CENTER_X_AND_Z = [PRINGLE_OFFSET[0], PRINGLE_OFFSET[2]]
    SPHERE_Y_RANGE = [0, 500]
    SPHERE_RADIUS = 106 # 6.8
    # SPHERE = Sphere(SPHERE_CENTER, SPHERE_RADIUS)
    USE_MSE = True
    NUM_SAMPLES = 9
    SPHERE = get_best_fit_sphere(PRINGLE_POINTS, SPHERE_CENTER_X_AND_Z, SPHERE_Y_RANGE, SPHERE_RADIUS, USE_MSE, NUM_SAMPLES)
    print("Best fit sphere for the pringle like whatnot-42 is", SPHERE)
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(PRINGLE_FILENAME_XYZ, SPHERE, PRINGLE_FILENAME_PLY)

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

def get_min_and_max_distances_between_points(points):
    min_distance = float("inf")
    max_distance = float("-inf")
    NUM_POINTS = len(points)
    for i in range(NUM_POINTS):
        for j in range(i + 1, NUM_POINTS):
            vector = points[i] - points[j]
            distance = np.linalg.norm(vector)
            if distance < min_distance:
                min_distance = distance
            if distance > max_distance:
                max_distance = distance
    return min_distance, max_distance

def get_index_of_closest_point(point, points, indices_to_skip):
    min_distance = float("inf")
    index = -1
    NUM_POINTS = len(points)
    for i in range(NUM_POINTS):
        if i not in indices_to_skip:
            vector = point - points[i]
            distance = np.linalg.norm(vector)
            if distance < min_distance:
                min_distance = distance
                index = i
    if index == -1:
        # Chosen from https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        raise AssertionError('Could not set the resulting index')
    return index

def get_sorted_points(points):
    check.is_an_array(points)
    check.length_is_greater_or_equal_to_N(points, 4)
    NUM_POINTS = len(points)
    sorted_points= []
    sorted_points.append(points[0])
    indices_to_skip = []
    indices_to_skip.append(0)
    for i in range(1, NUM_POINTS):
        last_sorted_point = sorted_points[i - 1]
        idx = get_index_of_closest_point(last_sorted_point, points, indices_to_skip)
        sorted_points.append(points[idx])
        indices_to_skip.append(idx)
    check.length_is_equal_to_N(sorted_points, NUM_POINTS)
    return sorted_points

def get_spheres_given_series_of_4_points_and_study_variability(points):
    check.is_an_array(points)
    check.length_is_greater_or_equal_to_N(points, 4)
    DELTA = int(len(points)/4)
    four_points = np.random.rand(4, 3)
    sphere_centers = []
    sphere_radii = []
    min_distance_between_points_compared = float("inf")
    max_distance_between_points_compared = float("-inf")
    SORTED_POINTS = get_sorted_points(points)
    save_ply_file('data/_contour-' + contour_ID + '-debug--sorted-points.ply', SORTED_POINTS)
    for i in range(DELTA):
        four_points[0] = SORTED_POINTS[i]
        four_points[1] = SORTED_POINTS[i + DELTA]
        four_points[2] = SORTED_POINTS[i + 2*DELTA]
        four_points[3] = SORTED_POINTS[i + 3*DELTA]
        min_distance_between_4_points, max_distace_between_4_points = get_min_and_max_distances_between_points(four_points)
        if min_distance_between_4_points < min_distance_between_points_compared:
            min_distance_between_points_compared = min_distance_between_4_points
        if max_distace_between_4_points > max_distance_between_points_compared:
            max_distance_between_points_compared = max_distace_between_4_points
        sphere = get_sphere(four_points)
        # print("Sphere #{} given 4 points for indices {} {} {} {} is {}".format(i, i, i + DELTA, i + 2*DELTA, i + 3*DELTA, sphere))
        sphere_centers.append(sphere.get_center())
        sphere_radii.append(sphere.get_radius())
    bounding_box = get_bounding_box(sphere_centers)
    print('From the set of spheres given 4 points',)
    print('  the variability of the centers is [{:.3f}, {:.3f}] [{:.3f}, {:.3f}] [{:.3f}, {:.3f}]'.format(bounding_box[0][0], bounding_box[0][1], bounding_box[1][0], bounding_box[1][1], bounding_box[2][0], bounding_box[2][1]))
    print('  the variability of the radii is [{:.1f}, {:.1f}]'.format(min(sphere_radii), max(sphere_radii)))
    print('and the min and max distances between the sets of 4 points been used are {:.3f} and {:.3f}'.format(min_distance_between_points_compared, max_distance_between_points_compared))

def study_contour(contour_ID, sphere):
    print('\nstudy_contour({}, {}) starts...'.format(contour_ID, sphere))
    FILENAME_CONTOUR_XYZ = 'data/_contour-' + contour_ID + '.xyz'
    POINTS = read_xyz_file(FILENAME_CONTOUR_XYZ)

    _, _ = get_distances_to_sphere_and_scaled_normals(POINTS, sphere)

    get_spheres_given_series_of_4_points_and_study_variability(POINTS)

if __name__ == '__main__':

    np.random.seed(42)

    FILENAME_IN = 'data/points-in.xyz'
    FILENAME_OUT = 'data/points-out.ply'
    save_as_ply(FILENAME_IN, FILENAME_OUT)

    print
    play_with_a_pringle()

    print
    play_with_a_pringle_with_noise()

    print
    play_with_a_pringle_like_whatnot_42_with_noise()

    CONTOUR_ID_AND_SPHERE_ARRAY = [
        # ['01', 6], # hsalps
        # ['02', 0], # ainte
        # ['03', 6], # nabyar
        # ['04', Sphere([-20.684027, 53.338932, -14.109715], 132)], # ano, using vertices barycenter
        # ['05', Sphere([-22.295578, 60.587006, -609.661499], 131.3)], # maerts, using vertices barycenter
        # # ['06', Sphere(...)], # yzzif -- dismissed because we lack the sphere
        # ['07', Sphere([-19.99, 60.98, -116.1], 132)], # uen, using provided data 
        # ['08', Sphere([-22.372335, 61.412712, -601.807983], 132)], # tsorf, using vertices barycenter
        # ['09', Sphere([-22.22, 64.71, -609.73], 131.25)], # 7xr, using provided data, and trial-and-error for radius
        # ['10', Sphere([-21.56, 62.67, -118], 131.94)], # ram, using provided data, and trial-and-error for radius
        ['90', Sphere([-21.71, 61.51, -11.40], 131.9)], # B7 CIMIM, using center from MeshLab, and trial-and-error for radius
        ['91', Sphere([-21.64, 93.65, -12.88], 131.95)], # B4 CIMIM, using center from MeshLab, and trial-and-error for radius
        ['92', Sphere([-20.67, 61.48, -13.44], 131.95)], # 2 CIMIM, using center from MeshLab, and trial-and-error for radius
        ['93', Sphere([-21.17, 61.87, -11.40], 131.95)], # B9 CIMIM, using provided data, and trial-and-error for radius
        ['94', Sphere([-21.64, 62.29, -11.56], 131.955)], # B2 CIMIM, using provided data, and trial-and-error for radius
        ['95', Sphere([-24.09, 93.39, -11.27], 131.95)], # 1 CIMIM, using provided data, and trial-and-error for radius
        ['96', Sphere([-21.64, 61.44, -14.06], 132.77)], # B3 CIMIM, using provided data, and trial-and-error for radius
        ['97', Sphere([-21.64, 62.10, -10.70], 131.96)], # 7 CIMIM, using provided data, and trial-and-error for radius
        ['98', Sphere([-21.64, 62.29, -10.70], 131.95)], # B1 CIMIM, using provided data, and trial-and-error for radius
        ['99', Sphere([-20.68, 62.34, -10.70], 131.95)] # 3 CIMIM, using provided data, and trial-and-error for radius
    ]
    for contour_ID_and_sphere in CONTOUR_ID_AND_SPHERE_ARRAY:
        contour_ID, sphere = contour_ID_and_sphere
        study_contour(contour_ID, sphere)
        print
