"""module docstring should be here"""

import tkinter as tk

from enum import Enum
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

    # Define the radio buttons
    class MontyPythonFood(Enum):
        bacon = 'Bacon'
        eggs = 'Eggs'
        ham = 'Ham'
        spam = 'Spam'

    options: Final = tuple((member.name, member.value) for member in MontyPythonFood)
    radio_value: Final = tk.StringVar(value=MontyPythonFood.spam.name)  # Let us set spam as the default
    for value, text in options:
        tk.Radiobutton(root, text=text, variable=radio_value, value=value).pack(anchor=tk.W)

    def confirm():  # Function to be called when the user makes a selection
        user_choice = radio_value.get()
        print(f"Selected option {user_choice}")

    # Button to confirm the selection
    tk.Button(root, text="Confirm", command=confirm).pack()

    # Display Menu
    root.config(menu=menubar)
    tk.mainloop()


def main():
    play_with_tkinter()


if __name__ == '__main__':
    main()
