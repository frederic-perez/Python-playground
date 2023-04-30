"""
Some temporary work in progress stuff
"""


def main():
    for v in range(1, 3):
        print(f'{v%2} {int(v/2)}')

    print()

    for v in range(1, 4):
        print(f'{(v%3)%2} {int((v%3)/2)} {int(v/3)}')

    print()

    for v in range(1, 5):
        print(f'{((v%4)%3)%2} {int(((v%4)%3)/2)} {int((v%4)/3)} {int(v/4)}')

    print()

    for v in range(1, 6):
        print(f'{(((v % 5) % 4) % 3) % 2} {int((((v % 5) % 4) % 3) / 2)} {int(((v % 5) % 4) / 3)} {int((v % 5) / 4)} '
              f'{int(v / 5)}')


if __name__ == '__main__':
    main()
