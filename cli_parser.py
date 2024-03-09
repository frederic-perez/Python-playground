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


PlatonicSolidValues = tuple(member.value for member in PlatonicSolid)  # tuple is a MUST to reuse object


class Color(Enum):
    red = 'red'
    green = 'green'
    blue = 'blue'


ColorValues = tuple(member.value for member in Color)  # tuple is a MUST to reuse object


class Fruit(Enum):
    apple = 'apple'
    orange = 'orange'
    pear = 'pear'


FruitValues = tuple(member.value for member in Fruit)  # tuple is a MUST to reuse object


class OnOff(Enum):
    on = 'on'
    off = 'off'


OnOffValues = tuple(member.value for member in OnOff)  # tuple is a MUST to reuse object


prog_name: Final = os.path.basename(__file__)

epilog_text = \
    (f'Parse a set of example mandatory and optional CLI arguments, capitalizing `word`,\n'
     'and squaring both `integer` and `double`.\n'
     'Usage examples:\n'
     f'1) python {prog_name} word 2 3.14 -i in.txt -o out.txt -u Jane\n'
     f'2) python {prog_name} -i in.txt -o out.txt -u Jane word 2 3.14\n'
     f'3) python {prog_name} word 2 3.14 -i in -o out -u user --platonic-solid {PlatonicSolid.icosahedron.value}'
     f' --color {Color.green.value} --fruit {Fruit.pear.value}')


def create_parser():
    # Create ArgumentParser instance
    parser = argparse.ArgumentParser(
        description='A simple Python script to learn about parsing using the argparse module.',
        epilog=epilog_text,
        formatter_class=argparse.RawTextHelpFormatter)  # to preserve newlines and other formatting

    # Define known command-line options

    # 1) Positional argument(s)
    #
    parser.add_argument('word', type=str)
    parser.add_argument('integer', type=int)
    parser.add_argument('float', type=float)

    # 2) File selection
    #
    parser.add_argument(
        '-i', '--input-file', dest='input_file',
        type=str, required=True,
        help='read input from FILE', metavar='FILE')
    parser.add_argument(
        '-o', '--output-file', dest='output_file',
        type=str, required=True,
        help='write output to FILE', metavar='FILE')

    # 3) Operation flags/parameters
    #
    parser.add_argument(
        '-u', '--username', dest='username',
        type=str, required=True,
        help='your username')
    parser.add_argument(
        '--platonic-solid', dest='platonic_solid',
        type=str, choices=PlatonicSolidValues, required=False, default=PlatonicSolid.hexahedron.value)
    parser.add_argument(
        '--color', dest='color',
        type=str, choices=ColorValues, required=False, default=Color.red.value)
    parser.add_argument(
        '--fruit', dest='fruit',
        type=str, choices=FruitValues, required=False, default=Fruit.apple.value)

    # 4) Informative output
    #
    parser.add_argument(
        '-v', '--verbose',
        type=str, choices=OnOffValues, required=False, default=OnOff.off.value)

    return parser


def output_arguments(args):
    print('Positional argument(s):')
    print(f'   word is {args.word}')
    print(f'   integer is {args.integer}')
    print(f'   float is {args.float}')
    print('')
    print('File selection:')
    print(f'  --input-file {args.input_file}')
    print(f'  --output-file {args.output_file}')
    print('')
    print('Operation flags/parameters:')
    print(f'  --username {args.username}')
    print(f'  --platonic-solid {args.platonic_solid}')
    print(f'  --color {args.color}')
    print(f'  --fruit {args.fruit}')
    print('')
    print('Informative output:')
    print(f'   --verbose {args.verbose}')
    print('')


def deal_with_the_cli_parsing():
    parser = create_parser()
    try:
        args = parser.parse_args()  # Parse known command-line options
    except argparse.ArgumentError:
        print('❌  ERROR: Caught `argparse.ArgumentError`')
        parser.print_help()
        sys.exit(1)
    except SystemExit:
        print('❌  ERROR: Caught `SystemExit`')
        parser.print_help()
        sys.exit(1)
    output_arguments(args)
    return args


def do_the_actual_work(args):
    print(f'Capitalization of the word {args.word} is {args.word.upper()}.')
    print(f'The square of the integer {args.integer} is {args.integer * args.integer}.')
    print(f'The square of the float {args.float} is {args.integer * args.float}.')


def main():
    timer = Timer()

    args = deal_with_the_cli_parsing()
    do_the_actual_work(args)

    if args.verbose == OnOff.on.value:
        print(f'Script finished in {timer.elapsed()}')


if __name__ == '__main__':
    main()
