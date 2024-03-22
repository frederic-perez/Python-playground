"""
Some temporary work in progress stuff
"""

import numpy as np


def main():
    for v in range(1, 3):  # for #labels == 2
        print(f'{v % 2}'  # label 1
              f'{np.floor(v/2).astype(np.ubyte)}')  # label 2

    print()

    for v in range(1, 4):  # for #labels == 3
        print(f'{(v % 3) % 2}'  # label 1
              f'{np.floor((v % 3)/2).astype(np.ubyte)}'  # label 2
              f'{np.floor(v/3).astype(np.ubyte)}')  # label 3

    print()

    for v in range(1, 5):  # for #labels == 4
        print(f'{((v % 4) % 3) % 2}'  # label 1
              f'{np.floor(((v % 4) % 3)/2).astype(np.ubyte)}'  # label 2
              f'{np.floor((v % 4)/3).astype(np.ubyte)}'  # label 3
              f'{np.floor(v/4).astype(np.ubyte)}')  # label 4

    print()

    for v in range(1, 6):  # for #labels == 5
        print(f'{(((v % 5) % 4) % 3) % 2}'  # label 1
              f'{np.floor((((v % 5) % 4) % 3) / 2).astype(np.ubyte)}'  # label 2
              f'{np.floor(((v % 5) % 4) / 3).astype(np.ubyte)}'  # label 3
              f'{np.floor((v % 5) / 4).astype(np.ubyte)}'  # label 4
              f'{np.floor(v / 5).astype(np.ubyte)}')  # label 5


if __name__ == '__main__':
    main()
