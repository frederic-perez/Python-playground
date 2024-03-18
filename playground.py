"""module docstring should be here"""

import logging
import numpy as np
import subprocess
from sphere import get_sphere
from timer import Timer

logging.basicConfig(
    format='%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s: %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def play_with_numpy_random_numbers():
    np.random.seed(42)
    num_points = 2
    points = np.random.rand(num_points, 3)
    logger.info(f'points = {points}')


def average(*numbers):
    """Self-explanatory"""
    if not numbers:
        raise ValueError('numbers should not be empty')

    numbers_list = [float(number) for number in numbers]
    return sum(numbers_list) / float(len(numbers_list))


def get_sphere_given_4_points(description, points):
    sphere = get_sphere(points)
    logger.info(f'Sphere given {description}: {sphere}')


def get_git_version():
    command = 'git --version'
    timer = Timer()
    result = subprocess.call(command, shell=True)  # returns the exit code in unix
    logger.info(f'Command `{command}` took {timer.elapsed()} and returned {result}')


def download_file_using_curl(url, output_filename):
    command = 'curl ' + url + ' -o ' + output_filename
    timer = Timer()
    result = subprocess.call(command, shell=True)  # returns the exit code in unix
    if result == 0:
        logger.info(f'File `{output_filename}` has been downloaded in {timer.elapsed()}')
    else:
        logger.error(f'Failed to download file `{output_filename}`')


def decompress_7z_file(filename, output_directory):
    command = '7z x ' + filename + ' -o' + output_directory
    timer = Timer()
    result = subprocess.call(command, shell=True)  # returns the exit code in unix
    logger.info(f'Command `{command}` took {timer.elapsed()} and returned {result}')


def main():
    play_with_numpy_random_numbers()

    array_of_description_and_points = \
        ('4 straight crosshair points from whatnot 42', [
            [-35.3025, 0.6357,   3.8584],
            [-35.0932, 1.3599, -43.2535],
            [-09.054, -0.958,  -19.6768],
            [-62.0412, 5.9778, -19.7658]
        ]), \
        ('4 rotated crosshair points from whatnot 42', [
            [-58.7767,  4.9348,    -3.7779],
            [-13.3565, -0.644701, -29.8066],
            [-16.4319, -0.999301,   1.6949],
            [-55.543,   4.7384,   -37.1852]
        ]), \
        ('4 straight crosshair points from whatnot 46', [
            [-36.9284,  2.1009,  -1.0189],
            [-37.0922,  2.2078, -51.4502],
            [-10.4147, -0.1741, -26.0583],
            [-65.5153,  8.0756, -26.2123]
        ]), \
        ('4 rotated crosshair points from whatnot 46', [
            [-56.2434, 5.6835, -8.3162],
            [-15.5323, 0.0641003, -37.5089],
            [-54.5831, 5.3886, -44.8675],
            [-18.2069, 0.2075, -3.8871]
        ])
    for description, points in array_of_description_and_points:
        get_sphere_given_4_points(description, points)

    get_git_version()

    filename_and_url_array: list[tuple[str, str]] = [
      # ('data/_L.7z', 'https://uccbc8e1809ffe6c06563a47e1bb66.dl.dropboxusercontent.com/cd/0/get/A.../file#'),
      # ('data/_M.7z', 'https://uc26a4adfaf1d3cdc9423283971b37.dl.dropboxusercontent.com/cd/0/get/A.../file#')
      # ('data/_C54.xml', 'https://uc7b36b201202ac7cc04d68a05a966.dl.dropboxusercontent.com/cd/0/get/A.../file#'),
      # ('data/_F.stl', 'https://uc9961f6bd3472cdc89cd193cf4f37.dl.dropboxusercontent.com/cd/0/get/A.../file#'),
      # ('data/_L.stl', 'https://uc0a059daf35cb3466bfa34ee51666.dl.dropboxusercontent.com/cd/0/get/A.../file#'),
      # ('data/_R.stl', 'https://uc0dfa07f6b21b5c7d4102e78bb537.dl.dropboxusercontent.com/cd/0/get/A.../file#')
    ]
    for filename_and_url in filename_and_url_array:
        filename, url = filename_and_url
        download_file_using_curl(url, filename)

        filename_extension = filename[-2:]
        if filename_extension == '7z':
            output_directory = filename[0:7]
            decompress_7z_file(filename, output_directory)


if __name__ == '__main__':
    main()
