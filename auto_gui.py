"""module docstring should be here"""

import gettext
import os
import pyautogui as pg
import pygetwindow as gw  # type: ignore[import-untyped]
import pyperclip  # type: ignore[import-untyped]
import time

from colorama import Fore, Style
from enum import Enum
from typing import Final

title_FYI: Final[str] = '🤖💬 FYI'


def go_to_the_middle_of_the_window_and_do_click() -> None:
    # noinspection PyUnresolvedReferences
    pg.alert(  # type: ignore[attr-defined]
        '🤖💬 I am going to move the cursor to the middle of the screen, and print its location', title=title_FYI)
    screen_width, screen_height = pg.size()
    pg.moveTo(screen_width / 2, screen_height / 2, duration=.25)
    print(pg.position())


# Function to paste text using PyAutoGUI and Pyperclip
def paste_text(text: str) -> None:
    pyperclip.copy(text)
    pg.hotkey('ctrl', 'v')  # Simulate paste action


def move_window_to_origin(window_title: str) -> None:
    # Try to find the window
    windows: Final = pg.getWindowsWithTitle(window_title)  # type: ignore[attr-defined]
    if len(windows) == 0:
        return
    window: Final = windows[0]

    # Get the current position of the window
    current_x, current_y = window.left, window.top

    # Calculate the new position to move the window to
    new_x, new_y = 0, 0

    # Move the window to the new position
    window.move(new_x - current_x, new_y - current_y)


def move_window_to_bottom_right(window_title: str) -> None:
    # Try to find the window
    windows: Final = pg.getWindowsWithTitle(window_title)  # type: ignore[attr-defined]
    if len(windows) == 0:
        return
    window: Final = windows[0]

    # Get the current position of the window
    current_x, current_y = window.left, window.top

    # Calculate the new position to move the window to
    screen_width, screen_height = pg.size()
    current_width = window.width
    current_height = window.height
    new_x, new_y = screen_width - current_width, screen_height - current_height

    # Move the window to the new position
    window.move(new_x - current_x, new_y - current_y)


def play_a_bit_with_notepad_plus_plus() -> None:
    # noinspection PyUnresolvedReferences
    pg.alert(  # type: ignore[attr-defined]
        '🤖💬 I am going to open notepad++.exe, move the window twice, create a new buffer, type something, '
        'and quit without saving.',
        title=title_FYI)
    pg.PAUSE = 1
    pg.press('win')
    pg.typewrite('notepad', interval=.025)
    paste_text('++')
    pg.typewrite('.exe', interval=.025)
    time.sleep(.5)
    pg.press('enter')

    pg.hotkey('ctrl', 'n')  # 'New'

    # Get the list of all Notepad++ windows
    notepad_windows: Final = gw.getWindowsWithTitle('Notepad++')
    # Get the titles of the open Notepad++ windows
    titles: Final = [window.title for window in notepad_windows]
    # The newest tab will be the last one in the list
    # Assuming the last created tab is the one we just opened
    newest_tab_title: Final = titles[-1] if titles else None

    move_window_to_origin(newest_tab_title)  # do not use 'new 1 - Notepad++' because that can fail
    time.sleep(1)
    move_window_to_bottom_right(newest_tab_title)
    pg.typewrite('Hello, world!\nI will close this tab in 1 second...', interval=.025)
    time.sleep(1)
    pg.hotkey('ctrl', 'w')  # 'Close'
    pg.hotkey('tab')
    pg.press('enter')
    pg.hotkey('alt', 'f4')  # 'Exit'


def translate_hello_world() -> None:
    # Set up the location of the .mo files
    localedir: Final[str] = os.path.join(os.path.dirname(__file__), 'locales')

    # Choose the domain (name of the .mo files)
    domain: Final[str] = 'hello'

    class Languages(Enum):
        de = 'de'
        emoji = 'emoji'  # for the sort of fake emoji language
        en = 'en'
        fr = 'fr'
        ja = 'ja'

    languages_str: Final[tuple[str, ...]] = tuple(member.value for member in Languages)

    # Create translation instances
    map_language_to_translator: dict[str, gettext.GNUTranslations | gettext.NullTranslations] = {}
    for language_str in languages_str:
        map_language_to_translator[language_str] = gettext.translation(domain, localedir, [language_str], fallback=True)

    list_of_languages_plus_quit = list(member.value for member in Languages)
    list_of_languages_plus_quit.append('Quit')
    while True:
        # noinspection PyUnresolvedReferences
        language_str = pg.confirm(  # type: ignore[attr-defined]
            text='🤖💬 Choose the target language to translate Hello, world! to',
            title='Language selection',
            buttons=list_of_languages_plus_quit)
        if language_str in languages_str:
            map_language_to_translator[language_str].install()  # The 'magic' happens here
            print('» ' + Fore.LIGHTYELLOW_EX + f'{language_str}' + Style.RESET_ALL + ': ' +
                  _('Hello, world!'))  # type: ignore[name-defined]
        else:
            break


def main():
    go_to_the_middle_of_the_window_and_do_click() if True else None
    play_a_bit_with_notepad_plus_plus() if True else None
    translate_hello_world() if True else None


if __name__ == '__main__':
    main()
