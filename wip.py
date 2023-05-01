"""
Some temporary work in progress stuff
"""

import numpy as np


def main():
    for v in range(1, 3):
        print(f'{v%2} {np.floor(v/2):.0f}')

    print()

    for v in range(1, 4):
        print(f'{(v%3)%2} {np.floor((v%3)/2):.0f} {np.floor(v/3):.0f}')

    print()

    for v in range(1, 5):
        print(f'{((v%4)%3)%2} {np.floor(((v%4)%3)/2):.0f} {np.floor((v%4)/3):.0f} {np.floor(v/4):.0f}')

    print()

    for v in range(1, 6):
        print(f'{(((v % 5) % 4) % 3) % 2} {np.floor((((v % 5) % 4) % 3) / 2):.0f} {np.floor(((v % 5) % 4) / 3):.0f} '
              f'{np.floor((v % 5) / 4):.0f} {np.floor(v / 5):.0f}')


if __name__ == '__main__':
    main()
