"""module docstring should be here"""

import math
import numpy as np
import numpy.typing as npt
import os.path

import check
from formatting import format_float, format_floats, format_floats_hq
from sphere import Sphere, get_best_fit_sphere, get_sphere
from typing import Any, Final, Sequence


def get_saddle_points(num_points: int, a: float, b: float, radius_x: float, radius_z: float,
                      offset_xyz: tuple[float, float, float], max_noise: float = 0) -> npt.NDArray:
    points = np.random.rand(num_points, 3)
    a_sqr: Final[float] = a ** 2
    b_sqr: Final[float] = b ** 2
    for i in range(num_points):
        # print(f'i is {i}')
        alpha = i * 2 * math.pi / num_points
        x: float = radius_x * math.sin(alpha)
        z: float = radius_z * math.cos(alpha)
        y: float = z * z / b_sqr - x * x / a_sqr  # https://en.wikipedia.org/wiki/Paraboloid
        point = np.zeros(3)
        point[0] = x + offset_xyz[0]
        point[1] = y + offset_xyz[1]
        point[2] = z + offset_xyz[2]
        if max_noise > 0.:
            for j in range(3):
                point[j] += max_noise * (np.random.random_sample() - .5)
        points[i] = point
    return points


def get_distances_to_sphere_and_scaled_normals(points, sphere):
    function_name = 'get_distances_to_sphere_and_scaled_normals'
    print(f'{function_name}: sphere is {sphere}')
    num_points = len(points)
    distances = [0] * num_points
    scaled_normals = np.random.rand(num_points, 3)
    center = sphere.get_center()
    max_negative_distance = float("inf")
    max_positive_distance = -float("inf")
    for i in range(num_points):
        point = points[i]
        distance = sphere.get_signed_distance_to_surface(point)
        max_negative_distance = min(max_negative_distance, distance)
        max_positive_distance = max(max_positive_distance, distance)
        # print(f'{function_name}: distance for point {i} = {point} is {format_float(distance)}')
        distances[i] = distance
        scaled_normal = np.zeros(3)
        vector = center - point
        magnitude = np.linalg.norm(vector)
        for k in range(3):
            scaled_normal[k] = distance * vector[k] / magnitude
        scaled_normals[i] = scaled_normal
    print(f'{function_name}: max_negative_distance is {format_float(max_negative_distance)} | \
max_positive_distance is {format_float(max_positive_distance)}')
    return distances, scaled_normals


np.set_printoptions(formatter={'float_kind': format_float})


def save_xyz_file(filename_xyz, points):
    file_out = open(filename_xyz, 'w')

    for point in points:
        print(f'{format_floats(point)}', file=file_out)

    file_out.close()


def print_a_few_points(points: npt.NDArray) -> None:
    function_name = 'print_a_few_points'
    print(f'{function_name}: point #0 is {format_floats(points[0])}')
    print(f'{function_name}: ...')
    last_index = len(points) - 1
    print(f'{function_name}: point #{last_index} is {format_floats(points[last_index])}')


def read_xyz_file(filename_xyz) -> npt.NDArray:
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

    do_print_a_few_points = True
    if do_print_a_few_points:
        print_a_few_points(points)

    return points


def save_ply_file(filename_ply, points):
    file_out = open(filename_ply, 'w')

    num_points = len(points)
    header = ("ply\n"
              "format ascii 1.0\n"
              "element vertex " + str(num_points) + "\n"
                                                    "property float x\n"
                                                    "property float y\n"
                                                    "property float z\n"
                                                    "end_header\n")
    file_out.write(header)
    for point in points:
        print(f'{format_floats_hq(point)}', file=file_out)
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

    num_points = len(points)
    header = ("ply\n"
              "format ascii 1.0\n"
              "element vertex " + str(num_points) + "\n"
                                                    "property float x\n"
                                                    "property float y\n"
                                                    "property float z\n"
                                                    "property float u\n"
                                                    "property float v\n"
                                                    "property float nx\n"
                                                    "property float ny\n"
                                                    "property float nz\n"
                                                    "end_header\n")
    file_out.write(header)
    for i in range(num_points):
        point = points[i]
        distance = distances[i]
        scaled_normal = scaled_normals[i]
        print(f'{format_floats(point)} {format_float(distance)} 0 {format_floats(scaled_normal)}', file=file_out)
    file_out.close()


def save_as_ply(filename_xyz_in: str, filename_ply_out: str) -> None:
    if not filename_xyz_in:
        raise ValueError('Input filename should not be empty')
    if not os.path.exists(filename_xyz_in):
        raise IOError('Input file does not exist')
    if not filename_ply_out:
        raise ValueError('Output filename should not be empty')

    points = read_xyz_file(filename_xyz_in)
    save_ply_file(filename_ply_out, points)


def save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(
        filename_xyz_in: str, sphere: Sphere, filename_ply_out: str):
    if not filename_xyz_in:
        raise ValueError('Input filename should not be empty')
    if not os.path.exists(filename_xyz_in):
        raise IOError('Input file does not exist')
    if not filename_ply_out:
        raise ValueError('Output filename should not be empty')

    points = read_xyz_file(filename_xyz_in)
    distances, scaled_normals = get_distances_to_sphere_and_scaled_normals(points, sphere)
    save_ply_file_with_distances_and_scaled_normals(filename_ply_out, points, distances, scaled_normals)


def play_with_a_saddle() -> None:
    saddle_filename_xyz: Final = 'data/saddle.xyz'
    num_saddle_points: Final = 10  # 100
    saddle_a: Final = 8
    saddle_b: Final = 4
    saddle_radius_x: Final = 5
    saddle_radius_z: Final = 5
    saddle_offset: Final = 0, 4, 0
    saddle_points: Final = get_saddle_points(
        num_saddle_points,
        saddle_a,
        saddle_b,
        saddle_radius_x,
        saddle_radius_z,
        saddle_offset)
    save_xyz_file(saddle_filename_xyz, saddle_points)
    saddle_filename_ply: Final = 'data/saddle.ply'
    sphere_center: Final = 0, 0, 0
    sphere_radius: Final = 6.8
    sphere: Final = Sphere(sphere_center, sphere_radius)
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(
        saddle_filename_xyz, sphere, saddle_filename_ply)


def play_with_a_saddle_with_noise():
    saddle_filename_xyz = 'data/saddle-with-noise.xyz'
    num_saddle_points = 10  # 100
    saddle_a = 8
    saddle_b = 4
    saddle_radius_x = 5
    saddle_radius_z = 5
    saddle_offset = 0, 0, 4
    saddle_max_noise = .15
    saddle_points = get_saddle_points(
        num_saddle_points,
        saddle_a,
        saddle_b,
        saddle_radius_x,
        saddle_radius_z,
        saddle_offset,
        saddle_max_noise)
    save_xyz_file(saddle_filename_xyz, saddle_points)
    saddle_filename_ply = 'data/saddle-with-noise.ply'
    sphere_center = 0, 0, 0
    sphere_radius = 6.8
    sphere = Sphere(sphere_center, sphere_radius)
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(
        saddle_filename_xyz, sphere, saddle_filename_ply)


def play_with_a_saddle_like_whatnot_42_with_noise():
    saddle_filename_xyz = 'data/saddle-like-whatnot-42-with-noise.xyz'
    num_saddle_points = 10  # 100
    saddle_a = 15  # 20
    saddle_b = 20  # 15
    saddle_radius_x = 22  # 26
    saddle_radius_z = 26  # 22
    saddle_offset = -35, 0, -20
    saddle_max_noise = .5
    saddle_points = get_saddle_points(
        num_saddle_points,
        saddle_a,
        saddle_b,
        saddle_radius_x,
        saddle_radius_z,
        saddle_offset,
        saddle_max_noise)
    save_xyz_file(saddle_filename_xyz, saddle_points)
    saddle_filename_ply = 'data/saddle-like-whatnot-42-with-noise.ply'
    # sphere_center = [saddle_offset[0], 0, saddle_offset[2]]
    sphere_center_x_and_z = [saddle_offset[0], saddle_offset[2]]
    sphere_y_range = [0, 500]
    sphere_radius = 106  # 6.8
    # sphere = Sphere(sphere_center, sphere_radius)
    use_mse = True
    num_samples = 9
    sphere = \
        get_best_fit_sphere(saddle_points, sphere_center_x_and_z, sphere_y_range, sphere_radius, use_mse, num_samples)
    print(f'Best fit sphere for the saddle like whatnot-42 is {sphere}')
    save_as_ply_with_with_distances_and_scaled_normals_to_fitted_sphere(
        saddle_filename_xyz, sphere, saddle_filename_ply)


def get_bounding_box(points):
    x_coordinates, y_coordinates, z_coordinates = zip(*points)
    return [
        [min(x_coordinates), max(x_coordinates)],
        [min(y_coordinates), max(y_coordinates)],
        [min(z_coordinates), max(z_coordinates)]]


def get_center(bounding_box):
    center = [0] * 3
    for i in range(3):
        center[i] = (bounding_box[i][1] - bounding_box[i][0]) / 2. + bounding_box[i][0]
    return center


def get_min_and_max_distances_between_points(points):
    min_distance: float | np.floating[Any] = float("inf")
    max_distance: float | np.floating[Any] = float("-inf")
    num_points = len(points)
    for i in range(num_points):
        for j in range(i + 1, num_points):
            vector = points[i] - points[j]
            distance = np.linalg.norm(vector)
            if distance < min_distance:
                min_distance = distance
            if distance > max_distance:
                max_distance = distance
    return min_distance, max_distance


def get_index_of_closest_point(point, points, indices_to_skip):
    min_distance: float | np.floating[Any] = float("inf")
    index = -1
    num_points = len(points)
    for i in range(num_points):
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
    check.length_is_greater_or_equal_to_n(points, 4)
    num_points = len(points)
    sorted_points = [points[0]]
    indices_to_skip = [0]
    for i in range(1, num_points):
        last_sorted_point = sorted_points[i - 1]
        idx = get_index_of_closest_point(last_sorted_point, points, indices_to_skip)
        sorted_points.append(points[idx])
        indices_to_skip.append(idx)
    check.length_is_equal_to_n(sorted_points, num_points)
    return sorted_points


def get_spheres_given_series_of_4_points_and_study_variability(contour_id, points):
    check.is_an_array(points)
    check.length_is_greater_or_equal_to_n(points, 4)
    delta = int(len(points) / 4)
    four_points = np.random.rand(4, 3)
    sphere_centers = []
    sphere_radii = []
    min_distance_between_points_compared = float("inf")
    max_distance_between_points_compared = float("-inf")
    sorted_points = get_sorted_points(points)
    save_ply_file('data/_contour-' + contour_id + '-debug--sorted-points.ply', sorted_points)
    for i in range(delta):
        four_points[0] = sorted_points[i]
        four_points[1] = sorted_points[i + delta]
        four_points[2] = sorted_points[i + 2 * delta]
        four_points[3] = sorted_points[i + 3 * delta]
        min_distance_between_4_points, max_distance_between_4_points = \
            get_min_and_max_distances_between_points(four_points)
        if min_distance_between_4_points < min_distance_between_points_compared:
            min_distance_between_points_compared = min_distance_between_4_points
        if max_distance_between_4_points > max_distance_between_points_compared:
            max_distance_between_points_compared = max_distance_between_4_points
        sphere = get_sphere(four_points)
        # print(f'Sphere #{i} given 4 points for indices {i} {i + delta} {i + 2*delta} {i + 3*delta} is {sphere}')
        sphere_centers.append(sphere.get_center())
        sphere_radii.append(sphere.get_radius())
    bounding_box = get_bounding_box(sphere_centers)
    print('From the set of spheres given 4 points', )
    print(f'  the variability of the centers is \
[{format_float(bounding_box[0][0])}, {format_float(bounding_box[0][1])}] \
[{format_float(bounding_box[1][0])}, {format_float(bounding_box[1][1])}] \
[{format_float(bounding_box[2][0])}, {format_float(bounding_box[2][1])}]')
    print(f'  the variability of the radii is [{min(sphere_radii):.1f}, {max(sphere_radii):.1f}]')
    print(f'  and the min and max distances between the sets of 4 points been used are \
{format_float(min_distance_between_points_compared)} and {format_float(max_distance_between_points_compared)}')


def main():
    np.random.seed(42)

    filename_in: Final[str] = 'data/points-in.xyz'
    filename_out: Final[str] = 'data/points-out.ply'
    save_as_ply(filename_in, filename_out)

    print('Gonna call `play_with_a_saddle()`:')
    play_with_a_saddle()

    print('Gonna call `play_with_a_saddle_with_noise()`:')
    play_with_a_saddle_with_noise()

    print('Gonna call `play_with_a_saddle_like_whatnot_42_with_noise()`:')
    play_with_a_saddle_like_whatnot_42_with_noise()


if __name__ == '__main__':
    main()
