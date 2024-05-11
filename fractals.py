"""Originally based on the frim1’s (for "Fractal Images") good-old-`C` code circa 1995."""

import colorsys
import math
import random
import tkinter as tk
from tkinter.font import Font

from formatting import format_float
from timer import Timer
from typing import Final, TypeAlias


TupleOf3Ints: TypeAlias = tuple[int, int, int]
TupleOf3Floats: TypeAlias = tuple[float, float, float]


def get_random_rgb() -> TupleOf3Floats:
    return random.random(), random.random(), random.random()


def hsv2rgb(hsv: TupleOf3Floats) -> TupleOf3Floats:
    """Converts a color specification from the hsv model to the rgb model. As input, h ranges from 0. to 360. (not
    included), and s and v range from 0 to 1. [Baker]328.-"""
    (h, s, v) = hsv
    return colorsys.hsv_to_rgb(h/360., s, v)  # h must be normalized for the call to this particular function


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


def singleton(cls):
    """A decorator can be used to make a class a singleton. This method is concise and allows the class to be used as
    a singleton without modifying its code. However, it has limitations, such as not being thread-safe and not allowing
    the class to be inherited from."""
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class CommonVars:
    def __new__(cls,
                a_magnitude: tk.DoubleVar,
                a_k_max: tk.IntVar, a_c_max: tk.IntVar, a_step_colors: tk.IntVar,
                a_card_s: tk.Scale, a_card_v: tk.Scale,
                a_res_xy: tuple[tk.IntVar, tk.IntVar],
                a_use_photo_image: tk.BooleanVar) -> 'CommonVars':
        return object.__new__(cls)

    def __init__(self,
                 a_magnitude: tk.DoubleVar,
                 a_k_max: tk.IntVar, a_c_max: tk.IntVar, a_step_colors: tk.IntVar,
                 a_card_s: tk.Scale, a_card_v: tk.Scale,
                 a_res_xy: tuple[tk.IntVar, tk.IntVar],
                 a_use_photo_image: tk.BooleanVar) -> None:
        self.magnitude = a_magnitude
        self.k_max = a_k_max
        self.c_max = a_c_max
        self.step_colors = a_step_colors
        self.card_s = a_card_s
        self.card_v = a_card_v
        self.res_xy = a_res_xy[0], a_res_xy[1]
        self.use_photo_image = a_use_photo_image


@singleton
class JuliaSetVars:
    def __new__(cls,
                a_c: tuple[tk.DoubleVar, tk.DoubleVar],  # complex c number (real and imaginary parts)
                a_x_min_max: tuple[tk.DoubleVar, tk.DoubleVar],
                a_y_min_max: tuple[tk.DoubleVar, tk.DoubleVar]) -> 'JuliaSetVars':
        return object.__new__(cls)

    def __init__(self,
                 a_c: tuple[tk.DoubleVar, tk.DoubleVar],
                 a_x_min_max: tuple[tk.DoubleVar, tk.DoubleVar],
                 a_y_min_max: tuple[tk.DoubleVar, tk.DoubleVar]) -> None:
        self.c = a_c[0], a_c[1]
        self.x_min_max = a_x_min_max[0], a_x_min_max[1]
        self.y_min_max = a_y_min_max[0], a_y_min_max[1]


@singleton
class MandelbrotSetVars:
    def __new__(cls,
                a_p_min_max: tuple[tk.DoubleVar, tk.DoubleVar],
                a_q_min_max: tuple[tk.DoubleVar, tk.DoubleVar]) -> 'MandelbrotSetVars':
        return object.__new__(cls)

    def __init__(self,
                 a_p_min_max: tuple[tk.DoubleVar, tk.DoubleVar],
                 a_q_min_max: tuple[tk.DoubleVar, tk.DoubleVar]) -> None:
        self.p_min_max = a_p_min_max[0], a_p_min_max[1]
        self.q_min_max = a_q_min_max[0], a_q_min_max[1]


def go_julia(common_vars: CommonVars, julia_set_vars: JuliaSetVars, canvas: tk.Canvas) -> None:
    timer: Final = Timer()

    magnitude: Final[float] = common_vars.magnitude.get()
    k_max: Final[int] = common_vars.k_max.get()
    num_colors: Final[int] = common_vars.c_max.get()
    step_colors: Final[int] = common_vars.step_colors.get()
    card_s: Final[int] = int(common_vars.card_s.get())
    card_v: Final[int] = int(common_vars.card_v.get())
    res_xy: Final[tuple[int, int]] = common_vars.res_xy[0].get(), common_vars.res_xy[1].get()

    c: Final[tuple[float, float]] = julia_set_vars.c[0].get(), julia_set_vars.c[1].get()
    x_min: Final[float] = julia_set_vars.x_min_max[0].get()
    x_max: Final[float] = julia_set_vars.x_min_max[1].get()
    y_min: Final[float] = julia_set_vars.y_min_max[0].get()
    y_max: Final[float] = julia_set_vars.y_min_max[1].get()

    use_photo_image: Final[bool] = common_vars.use_photo_image.get()

    photo_image: Final = tk.PhotoImage(width=res_xy[0], height=res_xy[1]) if use_photo_image else None

    resolution_i: Final = res_xy[0]
    resolution_j: Final = res_xy[1]

    inc_x: Final = (x_max - x_min)/(resolution_i - 1.)
    inc_y: Final = (y_min - y_max)/(resolution_j - 1.)
    int_color: int = 0

    informer_out: int = 1
    informer: int = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
    row_column: int = 0

    array_colors: Final = generate_array_colors(num_colors, step_colors, card_s, card_v)
    # print(f"array_colors is {array_colors}")

    canvas.delete('all')  # delete old objects, reducing memory footprint and running time

    for j in range(0, resolution_j):
        for i in range(0, resolution_i):
            k: int = 0
            x_k = x_min + i * inc_x
            y_k = y_max + j * inc_y
            finished = False
            while not finished:
                x_k_plus_1 = x_k * x_k-y_k * y_k + c[0]
                y_k_plus_1 = 2. * x_k * y_k + c[1]
                k += 1
                x_k = x_k_plus_1
                y_k = y_k_plus_1
                r = x_k * x_k + y_k * y_k
                if r > magnitude:
                    int_color = k % num_colors + 1
                    finished = True
                elif k == k_max:
                    int_color = 0
                    finished = True

            color = array_colors[int_color]  # DEBUGGING: color = array_colors[(1 + i + j) % num_colors]

            # paint pixel
            if use_photo_image:
                assert photo_image is not None  # prevents mypy from generating a [union-attr] error for the line below
                photo_image.put(color, (i, j))
            else:
                canvas.create_rectangle(
                    i + 2, j + 2, i + 2, j + 2,  # Experimentally we found out we need + 2 to paint ALL pixels
                    fill=color, outline='')  # faster than canvas.create_oval

            if row_column > informer:
                print(f"{informer_out}", end='', flush=True)
                informer_out += 1
                informer = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
                if not use_photo_image:
                    canvas.update()
            row_column += 1
    print('')

    if use_photo_image:
        # canvas.create_image(0, 0, anchor=tk.NW, image=new_photo, tags="image")
        canvas.create_image((2 + res_xy[0] / 2, 2 + res_xy[1] / 2), image=photo_image, state="normal")
        canvas.image = photo_image  # type: ignore[attr-defined]  # Keep a reference to the image
        canvas.update()

    function_name: Final = go_julia.__name__
    print(f'Call to `{function_name}` took {timer.elapsed()}')


def go_mandelbrot(common_vars: CommonVars, mandelbrot_set_vars: MandelbrotSetVars, canvas: tk.Canvas) -> None:
    timer: Final = Timer()

    magnitude: Final[float] = common_vars.magnitude.get()
    k_max: Final[int] = common_vars.k_max.get()
    num_colors: Final[int] = common_vars.c_max.get()
    step_colors: Final[int] = common_vars.step_colors.get()
    card_s: Final[int] = int(common_vars.card_s.get())
    card_v: Final[int] = int(common_vars.card_v.get())
    res_xy: Final[tuple[int, int]] = common_vars.res_xy[0].get(), common_vars.res_xy[1].get()

    p_min: Final[float] = mandelbrot_set_vars.p_min_max[0].get()
    p_max: Final[float] = mandelbrot_set_vars.p_min_max[1].get()
    q_min: Final[float] = mandelbrot_set_vars.q_min_max[0].get()
    q_max: Final[float] = mandelbrot_set_vars.q_min_max[1].get()

    use_photo_image: Final[bool] = common_vars.use_photo_image.get()

    photo_image: Final = tk.PhotoImage(width=res_xy[0], height=res_xy[1]) if use_photo_image else None

    resolution_i: Final = res_xy[0]
    resolution_j: Final = res_xy[1]

    inc_p = (p_max - p_min)/(resolution_i - 1.)
    inc_q = (q_min - q_max)/(resolution_j - 1.)  # beware!
    int_color: int = 0

    informer_out: int = 1
    informer: int = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
    row_column: int = 0

    array_colors: Final = generate_array_colors(num_colors, step_colors, card_s, card_v)
    # print(f"array_colors is {array_colors}")

    canvas.delete('all')  # delete old objects, reducing memory footprint and running time

    for q in range(0, resolution_j):
        for p in range(0, resolution_i):
            k: int = 0
            p_0 = p_min + p * inc_p
            q_0 = q_max + q * inc_q  # beware!
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
                if r > magnitude:
                    int_color = k % num_colors + 1
                    finished = True
                elif k == k_max:
                    int_color = 0
                    finished = True

            color = array_colors[int_color]  # DEBUGGING: color = array_colors[(1 + i + j) % num_colors]

            # paint pixel
            if use_photo_image:
                assert photo_image is not None  # prevents mypy from generating a [union-attr] error for the line below
                photo_image.put(color, (p, q))
            else:
                canvas.create_rectangle(
                    p + 2, q + 2, p + 2, q + 2,  # Experimentally we found out we need + 2 to paint ALL pixels
                    fill=color, outline='')  # faster than canvas.create_oval

            if row_column > informer:
                print(f"{informer_out}", end='', flush=True)
                informer_out += 1
                informer = int(math.floor(informer_out * resolution_i * resolution_j) / 10.)
                if not use_photo_image:
                    canvas.update()
            row_column += 1
    print('')

    if use_photo_image:
        # canvas.create_image(0, 0, anchor=tk.NW, image=new_photo, tags="image")
        canvas.create_image((2 + res_xy[0] / 2, 2 + res_xy[1] / 2), image=photo_image, state="normal")
        canvas.image = photo_image  # type: ignore[attr-defined]  # Keep a reference to the image
        canvas.update()

    function_name: Final = go_mandelbrot.__name__
    print(f'Call to `{function_name}` took {timer.elapsed()}')


def set_up_fully_operational_gui(size: int) -> None:
    root = tk.Tk()  # Create the main window
    root.title('fractals')

    # Create the frames
    args = tk.Frame(root, relief="raised", borderwidth=0)
    args_common_controls = tk.Frame(args, relief="raised", borderwidth=1)
    args_julia_and_mandelbrot = tk.Frame(args, borderwidth=0)
    args_julia = tk.Frame(args_julia_and_mandelbrot, relief="raised", borderwidth=1)
    args_mandelbrot = tk.Frame(args_julia_and_mandelbrot, relief="raised", borderwidth=1)
    canvas: Final[tk.Canvas] = tk.Canvas(root, width=size, height=size, background='black')

    # Pack the frames
    args.pack(side="left", expand=True, fill="both")
    args_common_controls.pack(side="top", expand=False, fill="both")
    args_julia_and_mandelbrot.pack(side="bottom", expand=True, fill="both")
    args_julia.pack(side="left", expand=True, fill="both")
    args_mandelbrot.pack(side="right", expand=True, fill="both")
    canvas.pack(side="right")

    #
    font_for_titles = Font(size=12, weight="bold")

    # Common controls
    controls_label = tk.Label(args_common_controls, text="Common controls", font=font_for_titles)
    controls_m_frame = tk.Frame(args_common_controls)
    controls_m_label = tk.Label(controls_m_frame, text="M (magnitude)")
    magnitude = tk.DoubleVar(master=root, value=100.)
    controls_m_entry = tk.Entry(controls_m_frame, width=5, textvariable=magnitude)
    controls_m_entry.bind("<Return>", lambda event: None)
    controls_k_max_frame = tk.Frame(args_common_controls)
    controls_k_max_label = tk.Label(controls_k_max_frame, text="k_max (max. #iterations)")
    k_max = tk.IntVar(master=root, value=16)  # Maximum number of iterations
    controls_k_max_entry = tk.Entry(controls_k_max_frame, width=5, textvariable=k_max)
    controls_k_max_entry.bind("<Return>", lambda event: None)
    controls_c_max_frame = tk.Frame(args_common_controls)
    controls_c_max_label = tk.Label(controls_c_max_frame, text="C (max. #colors)")
    c_max = tk.IntVar(master=root, value=16)
    controls_c_max_entry = tk.Entry(controls_c_max_frame, width=5, textvariable=c_max)
    controls_c_max_entry.bind("<Return>", lambda event: None)
    controls_step_colors_frame = tk.Frame(args_common_controls)
    controls_step_colors_label = tk.Label(controls_step_colors_frame, text="SC (step colors)")
    step_colors = tk.IntVar(master=root, value=1)
    controls_step_colors_entry = tk.Entry(controls_step_colors_frame, width=5, textvariable=step_colors)
    controls_step_colors_entry.bind("<Return>", lambda event: None)
    controls_card_sv_frame = tk.Frame(args_common_controls)
    controls_card_sv_s = tk.Scale(controls_card_sv_frame, label="card{S} in HSV", from_=0, to=10, resolution=1,
                                  length="3c", relief="sunken", orient="horizontal")
    controls_card_sv_s.set(1)
    controls_card_sv_v = tk.Scale(controls_card_sv_frame, label="card{V} in HSV", from_=0, to=10, resolution=1,
                                  length="3c", relief="sunken", orient="horizontal")
    controls_card_sv_v.set(1)

    gray = tk.BooleanVar(master=root, value=False)

    class GrayCommand:
        def __init__(self):
            self.old_s: int = 66
            self.old_v: int = 66

        def __call__(self) -> None:
            if gray.get():  # i.e, the checkmark has been activated
                self.old_s = int(controls_card_sv_s.get())
                self.old_v = int(controls_card_sv_v.get())
                controls_card_sv_s.set(0)
                controls_card_sv_v.set(0)
            else:
                controls_card_sv_s.set(self.old_s)
                controls_card_sv_v.set(self.old_v)

    gray_command = GrayCommand()

    controls_g_checkbutton = tk.Checkbutton(args_common_controls, text="g (gray)", variable=gray, relief="flat",
                                            anchor="w", command=gray_command)

    controls_res_x_and_y_frame = tk.Frame(args_common_controls)
    controls_res_x_and_y__x_frame = tk.Frame(controls_res_x_and_y_frame)
    controls_res_x_and_y_y_frame = tk.Frame(controls_res_x_and_y_frame)
    controls_res_x_and_y_x_label = tk.Label(controls_res_x_and_y__x_frame, text="resolution_X")
    res_x = tk.IntVar(master=root, value=128)
    controls_res_x_and_y_x_entry = tk.Entry(controls_res_x_and_y__x_frame, width=5, relief="sunken", textvariable=res_x)
    controls_res_x_and_y_y_label = tk.Label(controls_res_x_and_y_y_frame, text="resolution_Y")
    res_y = tk.IntVar(master=root, value=128)
    controls_res_x_and_y_y_entry = tk.Entry(controls_res_x_and_y_y_frame, width=5, relief="sunken", textvariable=res_y)
    use_photo_image = tk.BooleanVar(master=root, value=False)
    controls_use_photo_image_checkbutton = tk.Checkbutton(args_common_controls, text="Use photo_image",
                                                          variable=use_photo_image, relief="flat", anchor="w",
                                                          command='')
    common_vars = CommonVars(magnitude, k_max, c_max, step_colors, controls_card_sv_s, controls_card_sv_v,
                             (res_x, res_y), use_photo_image)

    # Julia set
    julia_label = tk.Label(args_julia, text="Julia set", font=font_for_titles)
    julia_re_c_frame = tk.Frame(args_julia)
    julia_re_c_label = tk.Label(julia_re_c_frame, text="Re(c)")
    re_c = tk.DoubleVar(master=root, value=-.39054)
    julia_re_c_entry = tk.Entry(julia_re_c_frame, width=12, relief="sunken", textvariable=re_c)
    julia_re_c_entry.bind("<Return>", lambda event: None)
    julia_im_c_frame = tk.Frame(args_julia)
    julia_im_c_label = tk.Label(julia_im_c_frame, text="Im(c)")
    im_c = tk.DoubleVar(master=root, value=-.58679)
    julia_im_c_entry = tk.Entry(julia_im_c_frame, width=12, relief="sunken", textvariable=im_c)
    julia_im_c_entry.bind("<Return>", lambda event: None)
    julia_x_min_frame = tk.Frame(args_julia)
    julia_x_min_label = tk.Label(julia_x_min_frame, text="xMin")
    x_min = tk.DoubleVar(master=root, value=-1.5)
    julia_x_min_entry = tk.Entry(julia_x_min_frame, width=12, relief="sunken", textvariable=x_min)
    julia_x_min_entry.bind("<Return>", lambda event: None)
    julia_x_max_frame = tk.Frame(args_julia)
    julia_x_max_label = tk.Label(julia_x_max_frame, text="xMax")
    x_max = tk.DoubleVar(master=root, value=1.5)
    julia_x_max_entry = tk.Entry(julia_x_max_frame, width=12, relief="sunken", textvariable=x_max)
    julia_x_max_entry.bind("<Return>", lambda event: None)
    julia_y_min_frame = tk.Frame(args_julia)
    julia_y_min_label = tk.Label(julia_y_min_frame, text="yMin")
    y_min = tk.DoubleVar(master=root, value=-1.5)
    julia_y_min_entry = tk.Entry(julia_y_min_frame, width=12, relief="sunken", textvariable=y_min)
    julia_y_min_entry.bind("<Return>", lambda event: None)
    julia_y_max_frame = tk.Frame(args_julia)
    julia_y_max_label = tk.Label(julia_y_max_frame, text="yMax")
    y_max = tk.DoubleVar(master=root, value=1.5)
    julia_y_max_entry = tk.Entry(julia_y_max_frame, width=12, relief="sunken", textvariable=y_max)
    julia_y_max_entry.bind("<Return>", lambda event: None)

    julia_set_vars = JuliaSetVars((re_c, im_c), (x_min, x_max), (y_min, y_max))

    julia_go_button = tk.Button(args_julia, text="Go!", command=lambda: go_julia(common_vars, julia_set_vars, canvas))

    # Mandelbrot set
    mandelbrot_label = tk.Label(args_mandelbrot, text="Mandelbrot set", font=font_for_titles)
    mandelbrot_p_min_frame = tk.Frame(args_mandelbrot)
    mandelbrot_p_min_label = tk.Label(mandelbrot_p_min_frame, text="pMin")
    p_min = tk.DoubleVar(master=root, value=-2.25)
    mandelbrot_p_min_entry = tk.Entry(mandelbrot_p_min_frame, width=12, relief="sunken", textvariable=p_min)
    mandelbrot_p_min_entry.bind("<Return>", lambda event: None)
    mandelbrot_p_max_frame = tk.Frame(args_mandelbrot)
    mandelbrot_p_max_label = tk.Label(mandelbrot_p_max_frame, text="pMax")
    p_max = tk.DoubleVar(master=root, value=.75)
    mandelbrot_p_max_entry = tk.Entry(mandelbrot_p_max_frame, width=12, relief="sunken", textvariable=p_max)
    mandelbrot_p_max_entry.bind("<Return>", lambda event: None)
    mandelbrot_q_min_frame = tk.Frame(args_mandelbrot)
    mandelbrot_q_min_label = tk.Label(mandelbrot_q_min_frame, text="qMin")
    q_min = tk.DoubleVar(master=root, value=-1.5)
    mandelbrot_q_min_entry = tk.Entry(mandelbrot_q_min_frame, width=12, relief="sunken", textvariable=q_min)
    mandelbrot_q_min_entry.bind("<Return>", lambda event: None)
    mandelbrot_q_max_frame = tk.Frame(args_mandelbrot)
    mandelbrot_q_max_label = tk.Label(mandelbrot_q_max_frame, text="qMax")
    q_max = tk.DoubleVar(master=root, value=1.5)
    mandelbrot_q_max_entry = tk.Entry(mandelbrot_q_max_frame, width=12, relief="sunken", textvariable=q_max)
    mandelbrot_q_max_entry.bind("<Return>", lambda event: None)

    mandelbrot_set_vars = MandelbrotSetVars((p_min, p_max), (q_min, q_max))

    mandelbrot_go_button = tk.Button(args_mandelbrot, text="Go!",
                                     command=lambda: go_mandelbrot(common_vars, mandelbrot_set_vars, canvas))

    #
    # Pack the widgets
    #

    controls_label.pack()
    controls_m_frame.pack()
    controls_m_label.pack(side="left")
    controls_m_entry.pack(side="left")
    controls_k_max_frame.pack()
    controls_k_max_label.pack(side="left")
    controls_k_max_entry.pack(side="left")
    controls_c_max_frame.pack()
    controls_c_max_label.pack(side="left")
    controls_c_max_entry.pack(side="left")
    controls_step_colors_frame.pack()
    controls_step_colors_label.pack(side="left")
    controls_step_colors_entry.pack(side="left")
    controls_card_sv_frame.pack()
    controls_card_sv_s.pack(side="left")
    controls_card_sv_v.pack(side="right")
    controls_g_checkbutton.pack()
    controls_res_x_and_y_frame.pack()
    controls_res_x_and_y__x_frame.pack(side="left")
    controls_res_x_and_y_x_label.pack(side="left")
    controls_res_x_and_y_x_entry.pack(side="left")
    controls_res_x_and_y_y_frame.pack(side="right")
    controls_res_x_and_y_y_entry.pack(side="right")
    controls_res_x_and_y_y_label.pack(side="right")
    controls_use_photo_image_checkbutton.pack()

    julia_label.pack()
    julia_re_c_frame.pack(anchor="e")
    julia_re_c_label.pack(side="left", padx="1m")
    julia_re_c_entry.pack(side="left", padx="1m")
    julia_im_c_frame.pack(anchor="e")
    julia_im_c_label.pack(side="left", padx="1m")
    julia_im_c_entry.pack(side="left", padx="1m")
    julia_x_min_frame.pack(anchor="e")
    julia_x_min_label.pack(side="left", padx="1m")
    julia_x_min_entry.pack(side="left", padx="1m")
    julia_x_max_frame.pack(anchor="e")
    julia_x_max_label.pack(side="left", padx="1m")
    julia_x_max_entry.pack(side="left", padx="1m")
    julia_y_min_frame.pack(anchor="e")
    julia_y_min_label.pack(side="left", padx="1m")
    julia_y_min_entry.pack(side="left", padx="1m")
    julia_y_max_frame.pack(anchor="e")
    julia_y_max_label.pack(side="left", padx="1m")
    julia_y_max_entry.pack(side="left", padx="1m")
    julia_go_button.pack(pady="1m")

    mandelbrot_label.pack()
    mandelbrot_p_min_frame.pack(anchor="se")
    mandelbrot_p_min_label.pack(side="left", padx="1m")
    mandelbrot_p_min_entry.pack(side="left", padx="1m")
    mandelbrot_p_max_frame.pack(anchor="se")
    mandelbrot_p_max_label.pack(side="left", padx="1m")
    mandelbrot_p_max_entry.pack(side="left", padx="1m")
    mandelbrot_q_min_frame.pack(anchor="se")
    mandelbrot_q_min_label.pack(side="left", padx="1m")
    mandelbrot_q_min_entry.pack(side="left", padx="1m")
    mandelbrot_q_max_frame.pack(anchor="se")
    mandelbrot_q_max_label.pack(side="left", padx="1m")
    mandelbrot_q_max_entry.pack(side="left", padx="1m")
    mandelbrot_go_button.pack(pady="1m")

    root.config()
    tk.mainloop()


def main():
    hsv: Final[TupleOf3Floats] = 41., .3, .7
    rgb: Final = hsv2rgb(hsv)
    print(f'hsv {to_str(hsv)} converted to RGB resulted in {to_str(rgb)}')

    canvas_size: Final[int] = 512  # Use something ridiculous like 10 to verify ALL expected pixels are painted
    set_up_fully_operational_gui(canvas_size)


if __name__ == '__main__':
    main()
