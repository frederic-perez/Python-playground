"""module docstring should be here"""

import logging
import numpy as np
import subprocess

from sphere import get_sphere, Sphere
from timer import Timer
from typing import Final, Generator, Sequence, TypeAlias

logging.basicConfig(
    format='%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s: %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def play_with_numpy_random_numbers() -> None:
    np.random.seed(42)
    num_points: Final[int] = 2
    points = np.random.rand(num_points, 3)
    logger.info(f'points = {points}')


def average(*numbers: int | float) -> float:
    """Self-explanatory"""
    if not numbers:
        raise ValueError('numbers should not be empty')

    numbers_list = [float(number) for number in numbers]
    return sum(numbers_list) / float(len(numbers_list))


Number: TypeAlias = int | float
TupleOf3Numbers: TypeAlias = tuple[Number, Number, Number]


def get_sphere_given_4_points(description: str, points: Sequence[TupleOf3Numbers]) -> None:
    sphere: Final[Sphere] = get_sphere(points)
    logger.info(f'Sphere given {description}: {sphere}')


def get_git_version() -> None:
    command: Final[str] = 'git --version'
    timer = Timer()
    result: Final[int] = subprocess.call(command, shell=True)  # returns the exit code in unix
    logger.info(f'Command `{command}` took {timer.elapsed()} and returned {result}')


def download_file_using_curl(url: str, output_filename: str) -> None:
    command: Final[str] = 'curl ' + url + ' -o ' + output_filename
    timer = Timer()
    result: Final[int] = subprocess.call(command, shell=True)  # returns the exit code in unix
    if result == 0:
        logger.info(f'File `{output_filename}` has been downloaded in {timer.elapsed()}')
    else:
        logger.error(f'Failed to download file `{output_filename}`')


def decompress_7z_file(filename: str, output_directory: str) -> None:
    command: Final[str] = '7z x ' + filename + ' -o' + output_directory
    timer = Timer()
    result: Final[int] = subprocess.call(command, shell=True)  # returns the exit code in unix
    logger.info(f'Command `{command}` took {timer.elapsed()} and returned {result}')


def fibonacci_generator(n: int) -> Generator[int, None, None]:  # the function returns a generator that yields integers
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def main():
    play_with_numpy_random_numbers()

    array_of_description_and_points: Final = \
        ('4 straight crosshair points from whatnot 42', [
            (-35.3025, 0.6357,   3.8584),
            (-35.0932, 1.3599, -43.2535),
            (-09.054, -0.958,  -19.6768),
            (-62.0412, 5.9778, -19.7658)
        ]), \
        ('4 rotated crosshair points from whatnot 42', [
            (-58.7767,  4.9348,    -3.7779),
            (-13.3565, -0.644701, -29.8066),
            (-16.4319, -0.999301,   1.6949),
            (-55.543,   4.7384,   -37.1852)
        ]), \
        ('4 straight crosshair points from whatnot 46', [
            (-36.9284,  2.1009,  -1.0189),
            (-37.0922,  2.2078, -51.4502),
            (-10.4147, -0.1741, -26.0583),
            (-65.5153,  8.0756, -26.2123)
        ]), \
        ('4 rotated crosshair points from whatnot 46', [
            (-56.2434, 5.6835, -8.3162),
            (-15.5323, 0.0641003, -37.5089),
            (-54.5831, 5.3886, -44.8675),
            (-18.2069, 0.2075, -3.8871)
        ])
    for description, points in array_of_description_and_points:
        get_sphere_given_4_points(description, points)

    get_git_version()

    filename_and_url_array: Final[list[tuple[str, str]]] = [
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

    # Using the Fibonacci generator to print the first n Fibonacci numbers
    n: Final = 10
    print(f"First {n} Fibonacci numbers: ", end='')
    for num in fibonacci_generator(10):
        print(f"{num} ", end='')
    print()


if __name__ == '__main__':
    main()
