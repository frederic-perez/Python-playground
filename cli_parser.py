"""
Code originally based on https://github.com/frederic-perez/Ada-Byron-code-book's cli-parser code, using argparse, the
recommended command-line parsing module in the Python standard library.

Info on argparse:
- https://docs.python.org/3.12/library/argparse.html#argparse.ArgumentParser.parse_args
- https://docs.python.org/3.12/howto/argparse.html#argparse-tutorial
- https://realpython.com/command-line-interfaces-python-argparse/
"""

import argparse
import os
import sys
from enum import Enum
from timer import Timer
from typing import Final


class PlatonicSolid(Enum):
    tetrahedron = 'tetrahedron'
    octahedron = 'octahedron'
    icosahedron = 'icosahedron'
    hexahedron = 'hexahedron'
    dodecahedron = 'dodecahedron'


class Color(Enum):
    red = 'red'
    green = 'green'
    blue = 'blue'


class Fruit(Enum):
    apple = 'apple'
    orange = 'orange'
    pear = 'pear'


class OnOff(Enum):
    on = 'on'
    off = 'off'


prog_name: Final[str] = os.path.basename(__file__)

epilog_text: Final[str] = \
    (f'Parse a set of example mandatory and optional CLI arguments, capitalizing `word`,\n'
     'and squaring all the input numbers.\n\n'
     'Usage examples:\n'
     f'1) python {prog_name} spam 2 -3 4.5 -i in.txt -o out.txt -u Jane\n'
     f'2) python {prog_name} -i in.txt spam -o out.txt 2 -u Jane -3 4.5 # notice the interspersed mandatory arguments\n'
     f'3) python {prog_name} spam 2 -3 4.5 -i in -o out -u user --platonic-solid {PlatonicSolid.icosahedron.value}'
     f' --color {Color.green.value} --fruit {Fruit.pear.value} --suggested-window-position 6 7\n'
     f'4) python {prog_name} spam 2 -3 4.5 @response-file-1.txt --dry-run\n'
     f'5) python {prog_name} @response-file-1.txt @response-file-2.txt -u Eve\n')


# Custom type function for negative integer
def negative_integer(value: str) -> int:
    int_value = int(value)
    if int_value >= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a negative integer")
    return int_value


# Custom type function for unsigned integer
def unsigned_integer(value: str) -> int:
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not an integer")
    if int_value < 0:
        raise argparse.ArgumentTypeError(f"{value} is not an unsigned integer")
    return int_value


def create_parser() -> argparse.ArgumentParser:
    # Create ArgumentParser instance
    parser = argparse.ArgumentParser(
        add_help=False,  # disable the default help argument provided by argparse
        allow_abbrev=False,
        description='A simple Python script to learn about parsing using the argparse module.',
        formatter_class=argparse.RawTextHelpFormatter,  # to preserve newlines and other formatting
        fromfile_prefix_chars='@',
        epilog=epilog_text)

    # Define known command-line options

    # 1) Positional arguments (mandatory)
    #
    positional = parser.add_argument_group('1) Positional arguments (mandatory)')
    positional.add_argument('word', metavar='<word>', type=str)
    positional.add_argument('integer', metavar='<integer>', type=int)
    positional.add_argument('negative_integer', metavar='<negative integer>', type=negative_integer)
    positional.add_argument('float', metavar='<float>', type=float)

    # 2) File selection (mandatory)
    #
    file_selection = parser.add_argument_group('2) File selection (mandatory)')
    file_selection.add_argument(
        '-i', '--input-file', metavar='<file>', dest='input_file',
        type=str,
        required=True,
        help='read input from <file>')
    file_selection.add_argument(
        '-o', '--output-file', metavar='<file>', dest='output_file',
        type=str,
        required=True,
        help='write output to <file>')

    # 3) Operation flags/parameters
    #
    operation_flags_and_parameters = parser.add_argument_group('3) Operation flags/parameters')
    operation_flags_and_parameters.add_argument(
        '-u', '--username', metavar='<string>', dest='username',
        type=str,
        required=True,
        help='your username (mandatory)')
    operation_flags_and_parameters.add_argument(
        '--platonic-solid', choices=tuple(member.value for member in PlatonicSolid), dest='platonic_solid',
        type=str,
        required=False, default=PlatonicSolid.hexahedron.value,
        help='platonic solid (optional)')
    operation_flags_and_parameters.add_argument(
        '--color', choices=tuple(member.value for member in Color), dest='color',
        type=str,
        required=False, default=Color.red.value,
        help='color (optional)')
    operation_flags_and_parameters.add_argument(
        '--fruit', choices=tuple(member.value for member in Fruit), dest='fruit',
        type=str,
        required=False, default=Fruit.apple.value,
        help='fruit (optional)')
    operation_flags_and_parameters.add_argument(
        '--suggested-window-position', metavar=('<i>', '<j>'),
        type=unsigned_integer, nargs=2,
        required=False, default=(1, 1),
        help='in (unsigned integer) pixels, with `1 1` being the top-left corner (optional)')
    operation_flags_and_parameters.add_argument(
        '--dry-run', dest='dry_run', action='store_true',
        help='simulate the execution without applying any changes')  # flag

    # 4) Informative output
    #
    informative_output = parser.add_argument_group('4) Informative output (optional)')
    informative_output.add_argument('-h', '--help', action='help', help='show this help message and exit')
    informative_output.add_argument(
        '-v', '--verbose', choices=tuple(member.value for member in OnOff),
        type=str,
        required=False, default=OnOff.off.value)

    return parser


def output_arguments(args: argparse.Namespace) -> None:
    print(f'{prog_name} was called with the following options:')
    print('')
    print('1) Mandatory positional argument(s):')
    print(f'   word is {args.word}')
    print(f'   integer is {args.integer}')
    print(f'   negative_integer is {args.negative_integer}')
    print(f'   float is {args.float}')
    print('')
    print('2) File selection:')
    print(f'  --input-file {args.input_file}')
    print(f'  --output-file {args.output_file}')
    print('')
    print('3) Operation flags/parameters:')
    print(f'  --username {args.username}')
    print(f'  --platonic-solid {args.platonic_solid}')
    print(f'  --color {args.color}')
    print(f'  --fruit {args.fruit}')
    print(f'  --suggested-window-position {args.suggested_window_position[0]} {args.suggested_window_position[1]}')
    print('  --dry-run') if args.dry_run else print('  # --dry-run was not requested')
    print('')
    print('4) Informative output:')
    print(f'   --verbose {args.verbose}')
    print('')


def deal_with_the_cli_parsing() -> argparse.Namespace:
    parser = create_parser()
    try:
        args = parser.parse_args()  # Parse known command-line options
    except SystemExit:
        sys.exit(1)
    except argparse.ArgumentError as e:
        print(f'❌  ERROR: Caught `argparse.ArgumentError` {e}')
        parser.print_help()
        sys.exit(1)

    output_arguments(args)
    return args


def do_the_actual_work(args: argparse.Namespace) -> None:
    print(f'Capitalization of the word {args.word} is {args.word.upper()}.')
    print(f'The square of the integer {args.integer} is {args.integer * args.integer}.')
    print(f'The square of the negative integer {args.negative_integer} is'
          f' {args.negative_integer * args.negative_integer}.')
    print(f'The square of the float {args.float} is {args.integer * args.float}.')


def main():
    timer = Timer()

    args: argparse.Namespace = deal_with_the_cli_parsing()

    if args.verbose == OnOff.on.value:
        print(f'The actual work is about to start...')

    do_the_actual_work(args)

    if args.verbose == OnOff.on.value:
        print(f'{prog_name} finished in {timer.elapsed()}.')


if __name__ == '__main__':
    main()
