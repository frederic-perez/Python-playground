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
import gettext
import os

from enum import Enum
from typing import Final

# _ = gettext.gettext
#  '- Too bad: when uncommenting this line PyCharm does not complain about undefined reference,
#              but the translations stop working!

dummy_string_to_ensure_utf_8_encoding = "ø"  # Non-ASCII character to ensure (I doubt this, BTW) UTF-8 encoding


def main():
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

    print('`Hello, world!` in different languages:')

    for language_str in languages_str:
        map_language_to_translator[language_str].install()  # The 'magic' happens here
        print(f'- `{language_str}`: ' + _('Hello, world!'))  # type: ignore[name-defined]


if __name__ == '__main__':
    main()
