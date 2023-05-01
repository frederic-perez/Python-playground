"""
Some temporary work in progress stuff
"""

import numpy as np


def main():
    for v in range(1, 3):
        print(f'{v%2} {np.floor(v/2).astype(int)}')

    print()

    for v in range(1, 4):
        print(f'{(v%3)%2} {np.floor((v%3)/2).astype(int)} {np.floor(v/3).astype(int)}')

    print()

    for v in range(1, 5):
        print(f'{((v%4)%3)%2} {np.floor(((v%4)%3)/2).astype(int)} {np.floor((v%4)/3).astype(int)} '
              f'{np.floor(v/4).astype(int)}')

    print()

    for v in range(1, 6):
        print(f'{(((v % 5) % 4) % 3) % 2} {np.floor((((v % 5) % 4) % 3) / 2).astype(int)} '
              f'{np.floor(((v % 5) % 4) / 3).astype(int)} {np.floor((v % 5) / 4).astype(int)} '
              f'{np.floor(v / 5).astype(int)}')


if __name__ == '__main__':
    main()
