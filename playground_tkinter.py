"""module docstring should be here"""

import tkinter

from typing import Final


def play_with_tkinter():
    # Create tkinter window
    root: Final = tkinter.Tk()
    root.title('Menu Demo')

    # Create Menubar
    menubar: Final = tkinter.Menu(root)

    # Add File Menu and commands
    file: Final = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New File', command='')
    file.add_command(label='Open...', command='')
    file.add_command(label='Save', command='')
    file.add_separator()
    file.add_command(label='Exit', command=root.destroy)  # Notice the command here

    # Add Edit Menu and commands
    edit: Final = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=edit)
    edit.add_command(label='Cut', command='')
    edit.add_command(label='Copy', command='')
    edit.add_command(label='Paste', command='')
    edit.add_command(label='Select All', command='')
    edit.add_separator()
    edit.add_command(label='Find...', command='')
    edit.add_command(label='Find again', command='')

    # Add Help Menu
    help_: Final = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=help_)
    help_.add_command(label='Tk Help', command='')
    help_.add_command(label='Demo', command='')
    help_.add_separator()
    help_.add_command(label='About Demo', command='')

    # Display Menu
    root.config(menu=menubar)
    tkinter.mainloop()


def main():
    play_with_tkinter()


if __name__ == '__main__':
    main()
