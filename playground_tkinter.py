"""module docstring should be here"""

import tkinter as tk

from enum import Enum
from tkinter import ttk
from typing import Final


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
    labelForFoods: Final = tk.Label(root, text="Select a Monty Python's food:")
    labelForFoods.pack(pady=5)

    # Define the radio buttons
    class MontyPythonFood(Enum):
        bacon = 'Bacon'
        eggs = 'Eggs'
        ham = 'Ham'
        spam = 'Spam'

    optionsForFood: Final = tuple((member.name, member.value) for member in MontyPythonFood)
    radio_value: Final = tk.StringVar(value=MontyPythonFood.spam.name)  # Let us set spam as the default
    for value, text in optionsForFood:
        tk.Radiobutton(root, text=text, variable=radio_value, value=value).pack(anchor=tk.W)

    def confirm():  # Function to be called when the user makes a selection
        user_choice = radio_value.get()
        print(f"Selected Monty Python's food option: {user_choice}")

    # Button to print the selected radio button
    tk.Button(root, text="Confirm", command=confirm).pack()

    # Create a label
    labelForNames: Final = tk.Label(root, text="Select a placeholder name:")
    labelForNames.pack(pady=5)

    # Define the combobox
    class PlaceholderName(Enum):
        foo = 'foo'
        bar = 'bar'
        baz = 'baz'

    optionsForNames: Final = tuple(member.value for member in PlaceholderName)
    selected_option: Final = tk.StringVar()
    combobox: Final = ttk.Combobox(root, textvariable=selected_option, values=optionsForNames)
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
    tk.Button(root, text="Go", command=go).pack()

    # Display Menu
    root.config(menu=menubar)
    tk.mainloop()


def main():
    play_with_tkinter()


if __name__ == '__main__':
    main()
