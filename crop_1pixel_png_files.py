# -*- coding: utf-8 -*-
"""module docstring should be here"""

# Create an installer (a .exe file that will be placed in the dist/ subfolder) with the following command:
# $ pyinstaller.exe --onefile crop_1pixel_png_files.py
# Then you can create a shortcut on the Desktop to the newly created file .../dist/crop_1pixel_png_files.exe
# that allows dragging and dropping to the corresponding icon the user's selected files to be cropped.

import colorama
import emoji
import os
import re
import sys

from colorama import Fore, Back, Style
from PIL import Image
from typing import Final, TypeAlias

PillowImage: TypeAlias = Image.Image


def crop_image(image: PillowImage) -> PillowImage:
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the dimensions of the cropped image
    left: Final[int] = 1
    top: Final[int] = 1
    right: Final[int] = width - 1
    bottom: Final[int] = height - 1

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def get_human_readable_size(size_in_bytes: int) -> str:
    units: Final = "B", "KB", "MB", "GB", "TB", "PB"
    index: int = 0
    size_as_float: float = size_in_bytes
    while size_as_float >= 1024 and index < len(units) - 1:
        size_as_float /= 1024.
        index += 1
    return f"{size_as_float:.1f}{units[index]}"


def calculate_percentage_reduction(size_a: int, size_b: int) -> float:
    # Calculate the reduction amount
    reduction_amount: Final[int] = size_a - size_b

    # Calculate the percentage reduction
    percentage_reduction: Final[float] = (reduction_amount / size_a) * 100

    return percentage_reduction


def process_file(the_file_path_original: str, acc: int) -> None:
    # Open the original image
    image_original: Final = Image.open(the_file_path_original)
    width_original, height_original = image_original.size

    # Crop the image
    image_cropped: Final = crop_image(image_original)
    width_cropped, height_cropped = image_cropped.size

    # Construct the file path for the new image by adding a suffix before the extension
    base, ext = os.path.splitext(the_file_path_original)
    file_path_treated: Final[str] = f"{base}-TRTD{ext}"  # https://acronyms.thefreedictionary.com/trtd » Treated

    # Save the cropped image
    image_cropped.save(file_path_treated)

    basename_original: Final[str] = os.path.basename(the_file_path_original)
    basename_base, _ = os.path.splitext(basename_original)
    size_original: Final[int] = os.path.getsize(the_file_path_original)
    size_cropped: Final[int] = os.path.getsize(file_path_treated)
    size_str_original: Final[str] = get_human_readable_size(size_original)
    size_str_cropped: Final[str] = get_human_readable_size(size_cropped)
    percent_reduction: Final[float] = calculate_percentage_reduction(size_original, size_cropped)
    print(Back.LIGHTYELLOW_EX + Fore.BLACK + f' #{acc:03d} ' + Style.RESET_ALL + ' ' +
          Fore.LIGHTCYAN_EX + f'{basename_base}' +
          Back.LIGHTYELLOW_EX + Fore.BLACK + f' -TRTD ' + Style.RESET_ALL + Fore.LIGHTCYAN_EX + f'{ext}' +
          Style.RESET_ALL + ': ' +
          'From ' + Fore.LIGHTCYAN_EX + f'{width_original}x{height_original} ({size_str_original}) ' + Style.RESET_ALL +
          'to ' + Back.LIGHTYELLOW_EX + Fore.BLACK + f' {width_cropped}x{height_cropped} ({size_str_cropped}'
          ' ' + emoji.emojize(':down_arrow:') + f'{percent_reduction:.1f}%) ')


def process_hardcoded(folder_path: str, pattern: str) -> None:
    # Traverse the folder and print the names of PNG files that satisfy the pattern
    acc: int = 0
    for file_name in os.listdir(folder_path):
        if re.match(pattern, file_name):
            acc += 1
            file_path_original: str = folder_path + '/' + file_name
            process_file(file_path_original, acc)
        # if acc > 5:
        #    break


def process_files(file_paths: list[str]) -> None:
    if len(file_paths) == 0:
        return

    folder_path: Final[str] = os.path.dirname(file_paths[0])
    print(f"Folder path (of the first file) is `{folder_path}`")

    acc: int = 0
    for file_path_original in file_paths:
        acc += 1
        process_file(file_path_original, acc)
    # if acc > 5:
    #    break


if __name__ == '__main__':
    colorama.init(autoreset=True)  # initialize the console

    if len(sys.argv) < 2:
        print("No files provided » processing 'hardcoded' files:")
        hardcoded_folder_path: Final[str] = "D:\\3phemeral/foo-TRTD"
        hardcoded_pattern: Final[str] = r"^\d\d (DE|EN|ES) snap-\d{6}-\d{4}.png"
        process_hardcoded(hardcoded_folder_path, hardcoded_pattern)
    else:
        process_files(sys.argv[1:])
        input("Press any key to finish...")
