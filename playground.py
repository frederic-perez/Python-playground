"""module docstring should be here"""

import logging
import numpy as np
import subprocess

from pathlib import Path
from sphere import get_sphere, Sphere
from timer import Timer
from typing import Callable, Final, Generator, Sequence, TypeAlias

logging.basicConfig(
    format='%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s: %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def print_the_current_directory() -> None:
    current_directory : Final = Path.cwd()
    logger.info(f"Current directory is '{current_directory}'")


def check_if_file_exists_and_check_its_magic_numbers(filename_relative_path : str) -> None:
    def get_magic_bytes(a_file_path: Path, num_bytes=4) -> str:
        with open(a_file_path, 'rb') as file:
            magic_bytes : Final = file.read(num_bytes)
            return magic_bytes.hex().upper()

    file_path : Final = Path.cwd() / Path(filename_relative_path)
    if not file_path.is_file():
        logger.error(f"The file '{file_path}' does not exist")
        return

    file_magic_bytes : Final = get_magic_bytes(file_path, 8)
    png_magic_bytes : Final = "89504E470D0A1A0A"
    if file_magic_bytes == png_magic_bytes:
        logger.info(f"Magic bytes of '{filename_relative_path}' match the ones expected from a PNG file")
    else:
        logger.error(f"The magic bytes of '{filename_relative_path}' do not match the ones expected from a PNG file")


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


def apply_operation(operation: Callable[[int, int], int], a: int, b: int) -> int:
    return operation(a, b)


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


def create_multiplier(factor: int) -> Callable[[int], int]:
    def multiplier(number: int) -> int:
        return number * factor

    return multiplier


double: Callable[[int], int] = create_multiplier(2)
triple: Callable[[int], int] = create_multiplier(3)


def fibonacci_generator(n: int) -> Generator[int, None, None]:  # the function returns a generator that yields integers
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def main():
    print_the_current_directory()
    check_if_file_exists_and_check_its_magic_numbers('images/snap-240425-0035-fractals--Julia.png')

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

    print(f"double(7) = {double(7)}")
    print(f"triple(8) = {triple(8)}")

    print(f"apply_operation(add, 2, 3) = {apply_operation(add, 2, 3)}")
    print(f"apply_operation(multiply, 4, 5) = {apply_operation(multiply, 4, 5)}")

    # Using the Fibonacci generator to print the first n Fibonacci numbers
    n: Final = 10
    print(f"First {n} Fibonacci numbers: ", end='')
    for num in fibonacci_generator(10):
        print(f"{num} ", end='')
    print()


if __name__ == '__main__':
    main()
