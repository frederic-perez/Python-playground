"""module docstring should be here
Originally based on the frim1’s (for "Fractal Images") good-old-`C` code circa 1995.
"""

import colorsys
import math
import random
import tkinter as tk

from formatting import format_float
from typing import Final, TypeAlias

TupleOf3Ints: TypeAlias = tuple[int, int, int]
TupleOf3Floats: TypeAlias = tuple[float, float, float]


def get_random_rgb() -> TupleOf3Floats:
    return random.random(), random.random(), random.random()


def hsv2rgb(hsv: TupleOf3Floats) -> TupleOf3Floats:
    """Converts a color specification from the hsv model to the rgb model. As input, h ranges from 0. to 360. (not
    included), and s and v range from 0 to 1. [Baker]328.-"""
    (h, s, v) = hsv
    return colorsys.hsv_to_rgb(h/360., s, v)  # h is normalized for the call to colorsys’s function


def to_str(rgb: TupleOf3Floats) -> str:
    return '(' + format_float(rgb[0]) + ', ' + format_float(rgb[1]) + ', ' + format_float(rgb[2]) + ')'


def rgb_to_hex(rgb: TupleOf3Floats) -> str:
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))


def generate_array_colors(num_colors: int, step_colors: int, card_s: int, card_v: int) -> tuple[str, ...]:
    """We reserve num_colors + 1 entries to save in position 0 the color associated with 'no finished iterations'
    state."""
    array_colors: list[str] = [rgb_to_hex((0., 0., 0.))]
    for i in range(0, num_colors):
        h = ((i * step_colors) % num_colors) * (360. / num_colors)
        s = (i % card_s + 1.)/card_s if card_s > 0 else 0.
        v = (i % card_v + 1.)/card_v if card_v > 0 else (i+1.)/num_colors  # else -> gray scale
        rgb = hsv2rgb((h, s, v))
        array_colors.append(rgb_to_hex(rgb))
    return tuple(array_colors)


M: Final = 100.  # Magnitude
K: Final = 16  # Maximum number of iterations
num_colors: Final = 16
step_colors: Final = 1
card_s: Final = 1
card_v: Final = 1


def julia_set(photo_image: tk.PhotoImage) -> None:
    resolution_i: Final = photo_image.width()
    resolution_j: Final = photo_image.height()

    c: Final = -.39054, -.58679
    jx_min, jx_max = -1.5, 1.5
    jy_min, jy_max = -1.5, 1.5
    inc_x: Final = (jx_max - jx_min)/(resolution_i - 1.)
    inc_y: Final = (jy_min - jy_max)/(resolution_j - 1.)
    int_color: int = 0

    informer_out: int = 1
    informer: int = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
    row_column: int = 0

    array_colors: Final = generate_array_colors(num_colors, step_colors, card_s, card_v)
    # print(f"array_colors is {array_colors}")

    for j in range(0, resolution_j):
        for i in range(0, resolution_i):
            k: int = 0
            x_k = jx_min + i * inc_x
            y_k = jy_max + j * inc_y
            finished = False
            while not finished:
                x_k_plus_1 = x_k * x_k-y_k * y_k + c[0]
                y_k_plus_1 = 2. * x_k * y_k + c[1]
                k += 1
                x_k = x_k_plus_1
                y_k = y_k_plus_1
                r = x_k * x_k + y_k * y_k
                if r > M:
                    int_color = k % num_colors + 1
                    finished = True
                elif k == K:
                    int_color = 0
                    finished = True

            photo_image.put(array_colors[int_color], (i, j))
            if row_column > informer:
                print(f"{informer_out}", end='', flush=True)
                informer_out += 1
                informer = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
            row_column += 1


def mandelbrot_set(photo_image: tk.PhotoImage) -> None:
    resolution_i: Final = photo_image.width()
    resolution_j: Final = photo_image.height()

    mp_min, mp_max = -2.25, .75
    mq_min, mq_max = -1.5, 1.5
    inc_p = (mp_max - mp_min)/(resolution_i - 1.)
    inc_q = (mq_min - mq_max)/(resolution_j - 1.)  # beware!
    int_color: int = 0

    informer_out: int = 1
    informer: int = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
    row_column: int = 0

    array_colors: Final = generate_array_colors(num_colors, step_colors, card_s, card_v)
    # print(f"array_colors is {array_colors}")

    for q in range(0, resolution_j):
        for p in range(0, resolution_i):
            k: int = 0
            p_0 = mp_min + p * inc_p
            q_0 = mq_max + q * inc_q  # beware!
            x_k = 0.
            y_k = 0.
            finished = False
            while not finished:
                x_k_plus_1 = x_k * x_k - y_k * y_k + p_0
                y_k_plus_1 = 2. * x_k * y_k + q_0
                k += 1
                x_k = x_k_plus_1
                y_k = y_k_plus_1
                r = x_k * x_k + y_k * y_k
                if r > M:
                    int_color = k % num_colors + 1
                    finished = True
                elif k == K:
                    int_color = 0
                    finished = True

            photo_image.put(array_colors[int_color], (p, q))
            if row_column > informer:
                print(f"{informer_out}", end='', flush=True)
                informer_out += 1
                informer = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
            row_column += 1


def paint_fractal(photo_image: tk.PhotoImage) -> None:
    julia_set(photo_image)
    # mandelbrot_set(photo_image)


def create_a_window_and_paint_a_fractal(size: tuple[int, int]) -> None:
    # Create tkinter window
    window: Final = tk.Tk()
    window.title('fractals')

    canvas: Final[tk.Canvas] = tk.Canvas(window, width=size[0], height=size[1], background='black')
    canvas.pack()

    photo_image: Final = tk.PhotoImage(width=size[0], height=size[1])

    # Draw the PhotoImage on the Canvas
    canvas.create_image((size[0] / 2, size[1] / 2), image=photo_image, state="normal")

    paint_fractal(photo_image)

    window.config()
    tk.mainloop()


def main():
    hsv: Final[TupleOf3Floats] = 41., .3, .7
    rgb: Final = hsv2rgb(hsv)
    print(f'hsv {to_str(hsv)} converted to RGB resulted in {to_str(rgb)}')

    size: Final = 150, 150
    create_a_window_and_paint_a_fractal(size)


if __name__ == '__main__':
    main()
