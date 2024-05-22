"""module docstring should be here"""

# 1. [ONLY ONCE:] Install from https://github.com/vslavik/gettext-tools-windows its latest version
#     » Installed D:\3rd-parties\gettext-tools-windows-0.22.5
#     » Extended the PATH environment variable to include D:\3rd-parties\gettext-tools-windows-0.22.5\bin
# 2. Run the following commands to extract the initial .pot file
#    $ mkdir locales
#    $ xgettext --force-po --from-code=UTF-8 -o locales/hello.pot hello_world_i18n.py
#    $ sed -i 's/; charset=CHARSET/; charset=UTF-8/' locales/hello.pot # Fix CHARSET to UTF-8 for msgfmt
# 3. Create the initial .po files
#    $ mkdir locales/de; mkdir locales/de/LC_MESSAGES; cp locales/hello.pot locales/de/LC_MESSAGES/hello.po
#    $ mkdir locales/emoji; mkdir locales/zz/LC_MESSAGES; cp locales/hello.pot locales/emoji/LC_MESSAGES/hello.po
#    $ mkdir locales/fr; mkdir locales/fr/LC_MESSAGES; cp locales/hello.pot locales/fr/LC_MESSAGES/hello.po
#    $ mkdir locales/ja; mkdir locales/ja/LC_MESSAGES; cp locales/hello.pot locales/ja/LC_MESSAGES/hello.po
# 4. Edit locales/??/LC_MESSAGES/hello.po by adding the required translations
# 5. Create the .mo files
#    $ msgfmt.exe --statistics --verbose locales/de/LC_MESSAGES/hello.po -o locales/de/LC_MESSAGES/hello.mo
#    $ msgfmt.exe --statistics --verbose locales/emoji/LC_MESSAGES/hello.po -o locales/emoji/LC_MESSAGES/hello.mo
#    $ msgfmt.exe --statistics --verbose locales/fr/LC_MESSAGES/hello.po -o locales/fr/LC_MESSAGES/hello.mo
#    $ msgfmt.exe --statistics --verbose locales/ja/LC_MESSAGES/hello.po -o locales/ja/LC_MESSAGES/hello.mo
# Interesting URLs:
# - https://crowdin.com/blog/2022/09/28/python-app-translation-tutorial
#
# `import gettext` below required 'python -m pip install python-gettext'
#
import colorama
import gettext
import msvcrt
import os
import polib

from colorama import Fore, Style
from enum import Enum
from typing import Final

# _ = gettext.gettext
#  `- Too bad: when uncommenting this line PyCharm does not complain about undefined reference,
#              but the translations stop working!

dummy_string_to_ensure_utf_8_encoding = "ø"  # Non-ASCII character to ensure (I doubt this, BTW) UTF-8 encoding


def read_char() -> str:
    return msvcrt.getch().decode()


def colored_input(prompt: str, color: str) -> str:
    print(prompt, end='', flush=True)
    input_value = ''
    while True:
        char = read_char()
        if char == '\r':  # Enter key
            print()
            break
        elif char == '\b':  # Backspace
            if input_value:
                print('\b \b', end='', flush=True)
                input_value = input_value[:-1]
        else:
            print(f'{color}{char}', end='', flush=True)
            input_value += char
    return input_value


def translations_using_locales() -> None:
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

    print(Style.BRIGHT + 'Hello, world!' + Style.RESET_ALL + ' in different languages:')

    for language_str in languages_str:
        map_language_to_translator[language_str].install()  # The 'magic' happens here
        print('- ' + Fore.LIGHTYELLOW_EX + f'{language_str}' + Style.RESET_ALL + ': ' +
              _('Hello, world!'))  # type: ignore[name-defined]

    while True:
        language_str = colored_input('Please, type a target language (or something else, like `q`, to quit): ',
                                     Fore.LIGHTYELLOW_EX)
        if language_str in languages_str:
            map_language_to_translator[language_str].install()  # The 'magic' happens here
            print('» ' + Fore.LIGHTYELLOW_EX + f'{language_str}' + Style.RESET_ALL + ': ' +
                  _('Hello, world!'))  # type: ignore[name-defined]
        else:
            break


def translations_using_polib() -> None:
    def get_entry_if_msgid_exists_in_pofile(msgid: str, po_file: polib.POFile) -> polib.POEntry | None:
        for current_entry in po_file:
            if current_entry.msgid == msgid:
                return current_entry
        return None

    po_fr = polib.POFile()
    for id_str in ('foo', 'toto'), ('bar', 'tata'), ('baz', 'titi'):
        entry = polib.POEntry(msgid=id_str[0],
                              msgstr=id_str[1],
                              comment='A common comment #' + str(ord(id_str[1][1])),
                              tcomment='Translated by ' + id_str[1].capitalize(),
                              occurrences=[('example.py', '12'), ('anothermodule.py', '34')])
        po_fr.append(entry)
    po_fr.append(polib.POEntry(msgid='rare', msgstr=''))
    spy: Final[bool] = False
    if spy:
        print(po_fr)
    print('\nEntries of our POFile object:')
    for entry in po_fr:
        if entry.translated():
            print('- `' + Fore.LIGHTGREEN_EX + entry.msgid + Style.RESET_ALL +
                  '` » `' + entry.msgstr + '` (translated)')
        else:
            print('- `' + Fore.LIGHTRED_EX + entry.msgid + Style.RESET_ALL +
                  '` » `' + entry.msgstr + '` (not translated)')

    while True:
        word = colored_input('Please, enter a word (ahem, msgid) to be translated (or `q` to quit): ',
                             Fore.LIGHTYELLOW_EX)
        if word == 'q':
            break
        possible_entry = get_entry_if_msgid_exists_in_pofile(word, po_fr)
        if possible_entry is not None:
            print(f'The word ' + Fore.LIGHTGREEN_EX + word + Style.RESET_ALL + ' exists in POFile » entry:\n' +
                  Fore.WHITE + f'{possible_entry}' + Style.RESET_ALL)
        else:
            print(f'The word ' + Fore.LIGHTRED_EX + word + Style.RESET_ALL + ' does not exist in POFile')


if __name__ == '__main__':
    colorama.init(autoreset=True)  # initialize the console

    translations_using_locales()
    translations_using_polib()
