"""
Code originally based on https://github.com/frederic-perez/Ada-Byron-code-book's cli-parser code, using argparse, the
recommended command-line parsing module in the Python standard library.

Info on argparse:
- https://docs.python.org/3.12/library/argparse.html#argparse.ArgumentParser.parse_args
- https://docs.python.org/3.12/howto/argparse.html#argparse-tutorial
"""

from enum import Enum
import argparse


class PlatonicSolid(Enum):
    tetrahedron = "tetrahedron"
    octahedron = "octahedron"
    icosahedron = "icosahedron"
    hexahedron = "hexahedron"
    dodecahedron = "dodecahedron"


PossiblePlatonicSolids = (member.value for member in PlatonicSolid)


def help_of_possible_enum_values(enum_class):
    return '{ ' + ', '.join(member.value for member in enum_class) + ' }'


class Color(Enum):
    red = "red"
    green = "green"
    blue = "blue"


class Fruit(Enum):
    apple = 'apple'
    orange = 'orange'
    pear = 'pear'


def create_parser():
    # Create ArgumentParser instance
    parser = argparse.ArgumentParser(
        description='A simple Python script to learn about parsing using the argparse module.',
        epilog='Parse a set of example mandatory and optional CLI arguments, capitalizing `word`, and squaring '
               '`number`.')

    # Define known command-line options

    # 1) Positional argument(s)
    #
    parser.add_argument('word')
    parser.add_argument('number')

    # 2) File selection
    #
    parser.add_argument(
        '-i', '--input-file', dest='input_file', required=True, help='read input from FILE', metavar='FILE')
    parser.add_argument(
        '-o', '--output-file', dest='output_file', required=True, help='write output to FILE', metavar='FILE')

    # 3) Operation flags/parameters
    #
    parser.add_argument('-u', '--username', dest='username', required=True, help='your username')
    parser.add_argument('--platonic-solid', dest='platonic_solid', help=help_of_possible_enum_values(PlatonicSolid))
    parser.add_argument('--color', dest='color', help=help_of_possible_enum_values(Color))
    parser.add_argument('--fruit', dest='fruit', help=help_of_possible_enum_values(Fruit))

    # 4) Informative output
    #
    parser.add_argument('-v', '--verbose', help='{ on, off }')  # TODO: Create, set and use args.verbose_bool

    return parser


def check_arguments(args):
    if not args.input_file:
        return False
    if not args.output_file:
        return False
    # TODO: parse the rest of arguments, like the enum-related arguments
    return True


def output_arguments(args):
    print('Positional argument(s):')
    print(f'   word is {args.word}')
    print(f'   number is {args.number}')
    print('\nFile selection:')
    print(f'  --input-file {args.input_file}')
    print(f'  --output-file {args.output_file}')
    print('\nOperation flags/parameters:')
    print(f'  --username {args.username}')
    print(f'  --platonic-solid {args.platonic_solid}')
    print(f'  --color {args.color}')
    print(f'  --fruit {args.fruit}')
    print('\nInformative output:')
    print(f'   --verbose {args.verbose}')
    print('')


def main():
    parser = create_parser()
    args = parser.parse_args()  # Parse known command-line options
    succeeded = check_arguments(args)
    if not succeeded:
        parser.print_help()
    output_arguments(args)

    # Do "the job"
    print(f'Capitalization of {args.word} is {args.word.upper()}.')
    print(f'The square of {args.number} is {int(args.number) * int(args.number)}.')


if __name__ == '__main__':
    main()
