"""module docstring should be here"""

import tkinter as tk

from enum import Enum
from tkinter import ttk
from typing import Final, TypeAlias

TupleOf2Floats: TypeAlias = tuple[float, float]


def play_with_tkinter():
    # Create tkinter window
    root: Final = tk.Tk()
    root.title('Menu Demo')
    # root.geometry("500x250")

    # Create Menubar
    menubar: Final = tk.Menu(root)

    # Add File Menu and commands
    file: Final = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New File', command='')
    file.add_command(label='Open...', command='')
    file.add_command(label='Save', command='')
    file.add_separator()
    file.add_command(label='Exit', command=root.destroy)  # Notice the command here

    # Add Edit Menu and commands
    edit: Final = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=edit)
    edit.add_command(label='Cut', command='')
    edit.add_command(label='Copy', command='')
    edit.add_command(label='Paste', command='')
    edit.add_command(label='Select All', command='')
    edit.add_separator()
    edit.add_command(label='Find...', command='')
    edit.add_command(label='Find again', command='')

    # Add Help Menu
    help_: Final = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=help_)
    help_.add_command(label='Tk Help', command='')
    help_.add_command(label='Demo', command='')
    help_.add_separator()
    help_.add_command(label='About Demo', command='')

    # Create a label
    label_for_foods: Final = tk.Label(root, text="Select a Monty Python's food:")
    label_for_foods.pack(pady=5)

    # Define the radio buttons
    class MontyPythonFood(Enum):
        bacon = 'Bacon'
        eggs = 'Eggs'
        ham = 'Ham'
        spam = 'Spam'

    options_for_food: Final = tuple((member.name, member.value) for member in MontyPythonFood)
    radio_value: Final = tk.StringVar(value=MontyPythonFood.spam.name)  # Let us set spam as the default
    for value, text in options_for_food:
        tk.Radiobutton(root, text=text, variable=radio_value, value=value).pack(anchor=tk.CENTER)

    def confirm():  # Function to be called when the user makes a selection
        user_choice = radio_value.get()
        print(f"Selected Monty Python's food option: {user_choice}")

    # Button to print the selected radio button
    tk.Button(root, text="Confirm", command=confirm).pack()

    # Create a label
    label_for_names: Final = tk.Label(root, text="Select a placeholder name:")
    label_for_names.pack(pady=5)

    # Define the combobox
    class PlaceholderName(Enum):
        foo = 'foo'
        bar = 'bar'
        baz = 'baz'

    options_for_names: Final = tuple(member.value for member in PlaceholderName)
    selected_option: Final = tk.StringVar()
    combobox: Final = ttk.Combobox(root, textvariable=selected_option, values=options_for_names)
    combobox.set(PlaceholderName.bar.value)  # Let us set bar as the default
    combobox.pack(pady=0)

    # Define a function to handle the selection
    def on_select(_):  # We define the argument with an underscore instead of 'event' because it is not used
        selected: Final = combobox.get()
        print(f"Selected placeholder name: {selected}")

    # Bind the selection event to the function
    combobox.bind("<<ComboboxSelected>>", on_select)

    def go():
        print(f"Selected Monty Python's food option {radio_value.get()}, and placeholder name {combobox.get()}")

    # Button to print all the selections
    tk.Button(root, text="Go", command=go).pack(pady=4)

    def g_pline(the_canvas: tk.Canvas, vertices: list[TupleOf2Floats], origin: TupleOf2Floats, scale: float) -> None:
        n: Final = len(vertices)
        if n <= 1:  # bail out ASAP
            return

        vertices_transformed: list[TupleOf2Floats] = []
        height: Final = the_canvas.winfo_height()
        for i in range(0, n):
            vertices_transformed.append(
                (origin[0] + vertices[i][0] * scale, height - (origin[1] + vertices[i][1] * scale)))
        the_canvas.create_line(*vertices_transformed, smooth=False)

    def draw_cobi(the_canvas: tk.Canvas, origin: TupleOf2Floats, scale: float) -> None:
        eye_bottom: Final[list[TupleOf2Floats]] = [(67, 121), (60, 116)]
        eye_top: Final[list[TupleOf2Floats]] = [(50, 149), (42, 142)]
        mouth: Final[list[TupleOf2Floats]] = [(55, 105), (47, 98), (31, 103)]
        head: Final[list[TupleOf2Floats]] = [(90, 130), (77, 132), (75, 134.7), (58, 120), (75, 134.7), (70, 141.3),
                                             (52, 127), (70, 141.3), (68, 144), (50, 132), (68, 144), (70, 160),
                                             (60, 154), (50, 153), (26, 147), (20, 152), (22, 157), (20, 152),
                                             (10, 130), (12, 110), (17, 97), (30, 89), (40, 89), (50, 90), (61, 95),
                                             (90, 130)]
        neck: Final[list[TupleOf2Floats]] = [(17, 97), (20, 82), (30, 89), (42, 80), (61, 95)]
        placket: Final[list[TupleOf2Floats]] = [(25, 85.5), (28, 70), (34, 69), (33, 86.75)]
        button_1: Final[list[TupleOf2Floats]] = [(31, 73), (30, 75)]
        button_2: Final[list[TupleOf2Floats]] = [(30, 80), (30, 83)]
        arm_big: Final[list[TupleOf2Floats]] = [(61, 95), (82, 79), (80, 76), (82, 59), (72, 43), (68, 62), (58, 72),
                                                (68, 62), (80, 76)]
        arm_small: Final[list[TupleOf2Floats]] = [(17, 97), (8, 80), (14, 71), (16, 79), (14, 71), (13, 60), (10, 68),
                                                  (10, 77)]
        belly: Final[list[TupleOf2Floats]] = [(72, 43), (72, 40), (42, 39), (14, 40), (13, 60)]
        leg_1: Final[list[TupleOf2Floats]] = [(68, 39.87), (69, 11), (71, 9), (71, 0), (50, 0), (49, 10), (60, 11),
                                              (69, 11)]
        leg_2: Final[list[TupleOf2Floats]] = [(49, 10), (46, 28), (38, 27), (38, 0), (3, 0), (2, 2), (3, 11), (5, 12),
                                              (18, 12), (18, 39.9)]
        shoe: Final[list[TupleOf2Floats]] = [(38, 8), (30, 9), (30, 4), (20, 4), (21, 0), (20, 4), (15, 12), (18, 12),
                                             (30, 9)]
        button_a: Final[list[TupleOf2Floats]] = [(27, 7), (28, 7)]
        button_b: Final[list[TupleOf2Floats]] = [(24, 8), (25, 8)]
        button_c: Final[list[TupleOf2Floats]] = [(21, 9), (22, 9)]

        for part in (eye_bottom, eye_top, mouth, head, neck, placket, button_1, button_2, arm_big, arm_small, belly,
                     leg_1, leg_2, shoe, button_a, button_b, button_c):
            g_pline(the_canvas, part, origin, scale)

    canvas_size: Final[tuple[int, int]] = 200, 175
    canvas: Final[tk.Canvas] = tk.Canvas(root, bg='white', bd=0, highlightthickness=0, width=canvas_size[0],
                                         height=canvas_size[1])
    canvas.pack(padx=0, pady=0)
    canvas.update()
    draw_cobi(canvas, (55, 10), 1)

    # Display Menu
    root.config(menu=menubar)
    tk.mainloop()


def main():
    play_with_tkinter()


if __name__ == '__main__':
    main()
