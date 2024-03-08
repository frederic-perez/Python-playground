"""
Code originally based on https://github.com/frederic-perez/Ada-Byron-code-book's cli-parser code, using argparse, the
recommended command-line parsing module in the Python standard library.

Info on argparse:
- https://docs.python.org/3.12/library/argparse.html#argparse.ArgumentParser.parse_args
- https://docs.python.org/3.12/howto/argparse.html#argparse-tutorial
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


def help_for_parser(enum_class):
    return '{ ' + ', '.join(member.value for member in enum_class) + ' }'


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
    (f'Parse a set of example mandatory and optional CLI arguments, capitalizing `word`, and squaring `number`.\n'
     'Usage examples:\n'
     f'1) python {prog_name} word 2 3.14 -i in.txt -o out.txt -u Jane\n'
     f'2) python {prog_name} -i in.txt -o out.txt -u Jane word 2 3.14\n'
     f'3) python {prog_name} word 2 3.14 -i in -o out -u user --platonic-solid icosahedron --color green --fruit pear')


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
        '-i', '--input-file', dest='input_file', required=True, type=str, help='read input from FILE', metavar='FILE')
    parser.add_argument(
        '-o', '--output-file', dest='output_file', required=True, type=str, help='write output to FILE', metavar='FILE')

    # 3) Operation flags/parameters
    #
    parser.add_argument('-u', '--username', dest='username', required=True, type=str, help='your username')
    parser.add_argument('--platonic-solid', dest='platonic_solid', type=str, default=PlatonicSolid.hexahedron.value,
                        help=help_for_parser(PlatonicSolid))
    parser.add_argument('--color', dest='color', type=str, default=Color.red.value, help=help_for_parser(Color))
    parser.add_argument('--fruit', dest='fruit', type=str, default=Fruit.apple.value, help=help_for_parser(Fruit))

    # 4) Informative output
    #
    parser.add_argument('-v', '--verbose', type=str, default=OnOff.off.value, help=help_for_parser(OnOff))

    return parser


def check_arguments(args):
    if not args.input_file:
        return False
    if not args.output_file:
        return False
    if args.platonic_solid not in PlatonicSolidValues:
        print(f'❌ ERROR: Wrong platonic_solid ({args.platonic_solid}).\n')
        return False
    if args.color not in ColorValues:
        print(f'❌ ERROR: Wrong color ({args.color}).\n')
        return False
    if args.fruit not in FruitValues:
        print(f'❌ ERROR: Wrong fruit ({args.fruit}).\n')
        return False
    if args.verbose not in OnOffValues:
        print(f'❌ ERROR: Wrong verbose ({args.verbose}).\n')
        return False
    return True


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
    args = parser.parse_args()  # Parse known command-line options
    succeeded = check_arguments(args)
    if not succeeded:
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
