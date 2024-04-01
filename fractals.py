"""module docstring should be here
Originally based on the frim1’s (for "Fractal Images") good-old-`C` code circa 1995.
"""

import colorsys
import math
import random
import tkinter as tk

from formatting import format_float
from timer import Timer
from typing import Final, TypeAlias


def sOrVcommand(event):
    pass


def grayCommand(event):
    return


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


def go_julia(canvas, size: tuple[int, int]) -> None:
    timer: Final = Timer()
    photo_image: Final = tk.PhotoImage(width=size[0], height=size[1])

    # Draw the PhotoImage on the Canvas
    # canvas.create_image((size[0] / 2, size[1] / 2), image=photo_image, state="normal")

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
    print('')

    # canvas.create_image(0, 0, anchor=tk.NW, image=new_photo, tags="image")
    canvas.create_image((size[0] / 2, size[1] / 2), image=photo_image, state="normal")
    canvas.image = photo_image  # Keep a reference to the image
    canvas.update()

    function_name: Final = go_julia.__name__
    print(f'Call to `{function_name}` took {timer.elapsed()}')


def go_mandelbrot(canvas, size: tuple[int, int]) -> None:
    timer: Final = Timer()

    photo_image: Final = tk.PhotoImage(width=size[0], height=size[1])

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
    print('')

    # canvas.create_image(0, 0, anchor=tk.NW, image=new_photo, tags="image")
    canvas.create_image((size[0] / 2, size[1] / 2), image=photo_image, state="normal")
    canvas.image = photo_image  # Keep a reference to the image
    canvas.update()

    function_name: Final = go_mandelbrot.__name__
    print(f'Call to `{function_name}` took {timer.elapsed()}')


def create_gui(size: int) -> None:
    root = tk.Tk() # Create the main window

    # Create the frames
    args = tk.Frame(root, relief="raised", borderwidth=1)
    args_julia_and_mandelbrot = tk.Frame(args, relief="raised", borderwidth=1)
    args_julia = tk.Frame(args_julia_and_mandelbrot, relief="raised", borderwidth=1)
    args_mandelbrot = tk.Frame(args_julia_and_mandelbrot, relief="raised", borderwidth=1)
    args_controls = tk.Frame(args, relief="raised", borderwidth=1)
    canvas: Final[tk.Canvas] = tk.Canvas(root, width=size, height=size, background='black')

    # Pack the frames
    args.pack(side="left", expand=True, fill="both")
    args_julia_and_mandelbrot.pack(side="top", expand=True, fill="both")
    args_julia.pack(side="left", expand=True, fill="both")
    args_mandelbrot.pack(side="right", expand=True, fill="both")
    args_controls.pack(side="bottom", expand=False, fill="both")
    canvas.pack(side="right")

    # Julia set
    julia_label = tk.Label(args_julia, text="Julia set")
    julia_rec_frame = tk.Frame(args_julia)
    julia_rec_label = tk.Label(julia_rec_frame, text="Re(c)")
    julia_rec_entry = tk.Entry(julia_rec_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    julia_rec_entry.bind("<Return>", lambda event: None)
    julia_imc_frame = tk.Frame(args_julia)
    julia_imc_label = tk.Label(julia_imc_frame, text="Im(c)")
    julia_imc_entry = tk.Entry(julia_imc_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    julia_imc_entry.bind("<Return>", lambda event: None)
    julia_xmin_frame = tk.Frame(args_julia)
    julia_xmin_label = tk.Label(julia_xmin_frame, text="xMin")
    julia_xmin_entry = tk.Entry(julia_xmin_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    julia_xmin_entry.bind("<Return>", lambda event: None)
    julia_xmax_frame = tk.Frame(args_julia)
    julia_xmax_label = tk.Label(julia_xmax_frame, text="xMax")
    julia_xmax_entry = tk.Entry(julia_xmax_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    julia_xmax_entry.bind("<Return>", lambda event: None)
    julia_ymin_frame = tk.Frame(args_julia)
    julia_ymin_label = tk.Label(julia_ymin_frame, text="yMin")
    julia_ymin_entry = tk.Entry(julia_ymin_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    julia_ymin_entry.bind("<Return>", lambda event: None)
    julia_ymax_frame = tk.Frame(args_julia)
    julia_ymax_label = tk.Label(julia_ymax_frame, text="yMax")
    julia_ymax_entry = tk.Entry(julia_ymax_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    julia_ymax_entry.bind("<Return>", lambda event: None)
    julia_go_button = tk.Button(args_julia, text="Go!", command=lambda: go_julia(canvas, (150, 150)))

    # Mandelbrot set
    mandelbrot_label = tk.Label(args_mandelbrot, text="Mandelbrot set")
    mandelbrot_pmin_frame = tk.Frame(args_mandelbrot)
    mandelbrot_pmin_label = tk.Label(mandelbrot_pmin_frame, text="pMin")
    mandelbrot_pmin_entry = tk.Entry(mandelbrot_pmin_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    mandelbrot_pmin_entry.bind("<Return>", lambda event: None)
    mandelbrot_pmax_frame = tk.Frame(args_mandelbrot)
    mandelbrot_pmax_label = tk.Label(mandelbrot_pmax_frame, text="pMax")
    mandelbrot_pmax_entry = tk.Entry(mandelbrot_pmax_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    mandelbrot_pmax_entry.bind("<Return>", lambda event: None)
    mandelbrot_qmin_frame = tk.Frame(args_mandelbrot)
    mandelbrot_qmin_label = tk.Label(mandelbrot_qmin_frame, text="qMin")
    mandelbrot_qmin_entry = tk.Entry(mandelbrot_qmin_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    mandelbrot_qmin_entry.bind("<Return>", lambda event: None)
    mandelbrot_qmax_frame = tk.Frame(args_mandelbrot)
    mandelbrot_qmax_label = tk.Label(mandelbrot_qmax_frame, text="qMax")
    mandelbrot_qmax_entry = tk.Entry(mandelbrot_qmax_frame, width=12, relief="sunken", textvariable=tk.StringVar())
    mandelbrot_qmax_entry.bind("<Return>", lambda event: None)
    mandelbrot_go_button = tk.Button(args_mandelbrot, text="Go!", command=lambda: go_mandelbrot(canvas, (150, 150)))

    # Controls
    controls_label = tk.Label(args_controls, text="Controls")
    controls_myM_frame = tk.Frame(args_controls)
    controls_myM_label = tk.Label(controls_myM_frame, text="M (magnitude)")
    controls_myM_entry = tk.Entry(controls_myM_frame, width=5, relief="sunken", textvariable=tk.StringVar())
    controls_myM_entry.bind("<Return>", lambda event: None)
    controls_myK_frame = tk.Frame(args_controls)
    controls_myK_label = tk.Label(controls_myK_frame, text="K (max. #iterations)")
    controls_myK_entry = tk.Entry(controls_myK_frame, width=5, relief="sunken", textvariable=tk.StringVar())
    controls_myK_entry.bind("<Return>", lambda event: None)
    controls_myC_frame = tk.Frame(args_controls)
    controls_myC_label = tk.Label(controls_myC_frame, text="C (max. #colors)")
    controls_myC_entry = tk.Entry(controls_myC_frame, width=5, relief="sunken", textvariable=tk.StringVar())
    controls_myC_entry.bind("<Return>", lambda event: None)
    controls_mySC_frame = tk.Frame(args_controls)
    controls_mySC_label = tk.Label(controls_mySC_frame, text="SC (step colors)")
    controls_mySC_entry = tk.Entry(controls_mySC_frame, width=5, relief="sunken", textvariable=tk.StringVar())
    controls_mySC_entry.bind("<Return>", lambda event: None)
    controls_mySandV_frame = tk.Frame(args_controls)
    controls_mySandV_s = tk.Scale(controls_mySandV_frame, label="s (saturation)", from_=0, to=10, length="3c", relief="sunken", orient="horizontal", command=sOrVcommand)
    controls_mySandV_v = tk.Scale(controls_mySandV_frame, label="v (value)", from_=0, to=10, length="3c", relief="sunken", orient="horizontal", command=sOrVcommand)
    controls_g_checkbutton = tk.Checkbutton(args_controls, text="g (gray)", variable=tk.BooleanVar(), relief="flat", anchor="w", command=grayCommand)
    controls_resXandY_frame = tk.Frame(args_controls)
    controls_resXandY_x_frame = tk.Frame(controls_resXandY_frame)
    controls_resXandY_y_frame = tk.Frame(controls_resXandY_frame)
    controls_resXandY_x_label = tk.Label(controls_resXandY_x_frame, text="resX")
    controls_resXandY_x_entry = tk.Entry(controls_resXandY_x_frame, width=4, relief="sunken", textvariable=tk.StringVar())
    controls_resXandY_y_label = tk.Label(controls_resXandY_y_frame, text="resY")
    controls_resXandY_y_entry = tk.Entry(controls_resXandY_y_frame, width=4, relief="sunken", textvariable=tk.StringVar())

    # Pack the widgets
    julia_label.pack()
    julia_rec_frame.pack(anchor="e")
    julia_rec_label.pack(side="left", padx="1m")
    julia_rec_entry.pack(side="left", padx="1m")
    julia_imc_frame.pack(anchor="e")
    julia_imc_label.pack(side="left", padx="1m")
    julia_imc_entry.pack(side="left", padx="1m")
    julia_xmin_frame.pack(anchor="e")
    julia_xmin_label.pack(side="left", padx="1m")
    julia_xmin_entry.pack(side="left", padx="1m")
    julia_xmax_frame.pack(anchor="e")
    julia_xmax_label.pack(side="left", padx="1m")
    julia_xmax_entry.pack(side="left", padx="1m")
    julia_ymin_frame.pack(anchor="e")
    julia_ymin_label.pack(side="left", padx="1m")
    julia_ymin_entry.pack(side="left", padx="1m")
    julia_ymax_frame.pack(anchor="e")
    julia_ymax_label.pack(side="left", padx="1m")
    julia_ymax_entry.pack(side="left", padx="1m")
    julia_go_button.pack(pady="1m")

    mandelbrot_label.pack()
    mandelbrot_pmin_frame.pack(anchor="se")
    mandelbrot_pmin_label.pack(side="left", padx="1m")
    mandelbrot_pmin_entry.pack(side="left", padx="1m")
    mandelbrot_pmax_frame.pack(anchor="se")
    mandelbrot_pmax_label.pack(side="left", padx="1m")
    mandelbrot_pmax_entry.pack(side="left", padx="1m")
    mandelbrot_qmin_frame.pack(anchor="se")
    mandelbrot_qmin_label.pack(side="left", padx="1m")
    mandelbrot_qmin_entry.pack(side="left", padx="1m")
    mandelbrot_qmax_frame.pack(anchor="se")
    mandelbrot_qmax_label.pack(side="left", padx="1m")
    mandelbrot_qmax_entry.pack(side="left", padx="1m")
    mandelbrot_go_button.pack(pady="1m")

    controls_label.pack()
    controls_myM_frame.pack()
    controls_myM_label.pack(side="left")
    controls_myM_entry.pack(side="left")
    controls_myK_frame.pack()
    controls_myK_label.pack(side="left")
    controls_myK_entry.pack(side="left")
    controls_myC_frame.pack()
    controls_myC_label.pack(side="left")
    controls_myC_entry.pack(side="left")
    controls_mySC_frame.pack()
    controls_mySC_label.pack(side="left")
    controls_mySC_entry.pack(side="left")
    controls_mySandV_frame.pack()
    controls_mySandV_s.pack(side="left")
    controls_mySandV_v.pack(side="right")
    controls_g_checkbutton.pack()
    controls_resXandY_frame.pack()
    controls_resXandY_x_frame.pack(side="left")
    controls_resXandY_x_label.pack(side="left")
    controls_resXandY_x_entry.pack(side="left")
    controls_resXandY_y_frame.pack(side="right")
    controls_resXandY_y_entry.pack(side="right")
    controls_resXandY_y_label.pack(side="right")

    root.config()
    tk.mainloop()


def main():
    hsv: Final[TupleOf3Floats] = 41., .3, .7
    rgb: Final = hsv2rgb(hsv)
    print(f'hsv {to_str(hsv)} converted to RGB resulted in {to_str(rgb)}')

    canvas_size: Final[int] = 300
    create_gui(canvas_size)


if __name__ == '__main__':
    main()
