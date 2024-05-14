# -*- coding: utf-8 -*-
"""module docstring should be here"""

# Create an installer (a .exe file that will be placed in the dist/ subfolder) with the following command:
# $ pyinstaller.exe --onefile crop_1pixel_png_files.py
# Then you can create a shortcut on the Desktop to the newly created file .../dist/crop_1pixel_png_files.exe
# that allows dragging and dropping to the corresponding icon the user's selected files to be treated.

import argparse
import colorama
import emoji
import os
import re
import sys

from colorama import Fore, Back, Style
from enum import Enum
from PIL import Image
from timer import Timer
from typing import Final, TypeAlias

PillowImage: TypeAlias = Image.Image


class OnOff(Enum):
    on = 'on'
    off = 'off'


class CompressMode(Enum):
    do_not_compress = 'do-not-compress'
    reduce_palette = 'reduce-palette'
    webp_convert = 'webp-convert'


prog_name: Final[str] = os.path.basename(__file__)

epilog_text: Final[str] = \
    (f'Treat png files depending on the CLI parameters.\n\n'
     'Usage examples:\n'
     f'1) python {prog_name} --crop {OnOff.on.value} --compress-mode {CompressMode.reduce_palette.value}\n'
     f'2) python {prog_name} @response-file-1.txt @response-file-2.txt --crop {OnOff.off.value}\n')


def create_parser() -> argparse.ArgumentParser:
    # Create ArgumentParser instance
    parser = argparse.ArgumentParser(
        add_help=False,  # disable the default help argument provided by argparse
        allow_abbrev=False,
        description='A simple Python script to treat png images according to the CLI parameters.',
        formatter_class=argparse.RawTextHelpFormatter,  # to preserve newlines and other formatting
        fromfile_prefix_chars='@',
        epilog=epilog_text)

    # Define known command-line options

    # 1) Operation flags/parameters
    #
    operation_flags_and_parameters = parser.add_argument_group('1) Operation flags/parameters')
    operation_flags_and_parameters.add_argument(
        '--crop', choices=tuple(member.value for member in OnOff), dest='crop',
        type=str,
        required=False, default=OnOff.off.value,
        help='crop (optional)')
    operation_flags_and_parameters.add_argument(
        '--compress-mode', choices=tuple(member.value for member in CompressMode), dest='compress_mode',
        type=str,
        required=False, default=CompressMode.do_not_compress.value,
        help='compress mode (optional)')

    # 2) Informative output
    #
    informative_output = parser.add_argument_group('2) Informative output (optional)')
    informative_output.add_argument('-h', '--help', action='help', help='show this help message and exit')
    informative_output.add_argument(
        '-v', '--verbose', choices=tuple(member.value for member in OnOff),
        type=str,
        required=False, default=OnOff.on.value)

    return parser


def output_arguments(args: argparse.Namespace, unknown_args: list[str]) -> None:
    print(Style.BRIGHT + f'{prog_name}' + Style.RESET_ALL + ' was called with the following options:')
    print('')
    print('1) Operation flags/parameters:')
    print(f'  --crop {args.crop}')
    print(f'  --compress-mode {args.compress_mode}')
    print('')
    print('2) Informative output:')
    print(f'   --verbose {args.verbose}')
    print('')
    print('3) Unknown arguments:')
    print(f'   {unknown_args}')
    print('')


def deal_with_the_cli_parsing() -> tuple[argparse.Namespace, list[str]]:
    parser = create_parser()
    try:
        args, unknown_args = parser.parse_known_args()  # Parse known command-line options
    except SystemExit:
        sys.exit(1)
    except argparse.ArgumentError as e:
        print(f'❌  ERROR: Caught `argparse.ArgumentError` {e}')
        parser.print_help()
        sys.exit(1)

    output_arguments(args, unknown_args)
    return args, unknown_args


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


def process_file(args: argparse.Namespace, the_file_path_original: str, acc: int) -> None:
    image_original: Final = Image.open(the_file_path_original)  # Open the original image
    width_original, height_original = image_original.size

    image_treated = crop_image(image_original) if args.crop == OnOff.on.value else image_original

    width_treated, height_treated = image_treated.size

    # Construct the file path for the new image by adding a suffix before the extension
    base, ext = os.path.splitext(the_file_path_original)
    file_path_treated: Final[str] = f"{base}-TRTD{ext}"  # https://acronyms.thefreedictionary.com/trtd » Treated

    # Save the treated image
    image_treated.save(file_path_treated)

    basename_original: Final[str] = os.path.basename(the_file_path_original)
    basename_base, _ = os.path.splitext(basename_original)
    size_original: Final[int] = os.path.getsize(the_file_path_original)
    size_treated: Final[int] = os.path.getsize(file_path_treated)
    size_str_original: Final[str] = get_human_readable_size(size_original)
    size_str_treated: Final[str] = get_human_readable_size(size_treated)
    percent_reduction: Final[float] = calculate_percentage_reduction(size_original, size_treated)
    print(Back.LIGHTYELLOW_EX + Fore.BLACK + f' #{acc:03d} ' + Style.RESET_ALL + ' ' +
          Fore.LIGHTCYAN_EX + f'{basename_base}' +
          Back.LIGHTYELLOW_EX + Fore.BLACK + f' -TRTD ' + Style.RESET_ALL + Fore.LIGHTCYAN_EX + f'{ext}' +
          Style.RESET_ALL + ': ' +
          'From ' + Fore.LIGHTCYAN_EX + f'{width_original}x{height_original} ({size_str_original}) ' + Style.RESET_ALL +
          'to ' + Back.LIGHTYELLOW_EX + Fore.BLACK + f' {width_treated}x{height_treated} ({size_str_treated}' +
          ' ' + emoji.emojize(':down_arrow:') + f'{percent_reduction:.1f}%) ')


def process_hardcoded(args: argparse.Namespace, folder_path: str, pattern: str) -> None:
    # Traverse the folder and print the names of PNG files that satisfy the pattern
    acc: int = 0
    for file_name in os.listdir(folder_path):
        if re.match(pattern, file_name):
            acc += 1
            file_path_original: str = folder_path + '/' + file_name
            process_file(args, file_path_original, acc)
        # if acc > 5:
        #    break


def process_files(args: argparse.Namespace, file_paths: list[str]) -> None:
    if len(file_paths) == 0:
        return

    folder_path: Final[str] = os.path.dirname(file_paths[0])
    print(f"Folder path (of the first file) is `{folder_path}`.\n")

    acc: int = 0
    for file_path_original in file_paths:
        acc += 1
        process_file(args, file_path_original, acc)
    # if acc > 5:
    #    break


if __name__ == '__main__':
    colorama.init(autoreset=True)  # initialize the console

    timer = Timer()

    args_and_unknown_args: Final = deal_with_the_cli_parsing()
    args: Final[argparse.Namespace] = args_and_unknown_args[0]
    unknown_args: Final[list[str]] = args_and_unknown_args[1]

    if args.verbose == OnOff.on.value:
        print(f'The actual work is about to start...\n')

    if len(unknown_args) == 0:
        print("No files provided » processing 'hardcoded' files:")
        hardcoded_folder_path: Final[str] = "D:\\3phemeral/foo-TRTD"
        hardcoded_pattern: Final[str] = r"^\d\d (DE|EN|ES) snap-\d{6}-\d{4}.png"
        process_hardcoded(args, hardcoded_folder_path, hardcoded_pattern)
    else:
        process_files(args, unknown_args)

    if args.verbose == OnOff.on.value:
        print('\n' + Style.BRIGHT + f'{prog_name}' + Style.RESET_ALL + f' finished in {timer.elapsed()}.')

    input('\n' + Style.BRIGHT + Fore.LIGHTYELLOW_EX + 'Press any key to finish... ' + Style.RESET_ALL)
