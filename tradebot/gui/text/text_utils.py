import colorama
import re


def clear_screen():
    """Clears the screen of the console"""
    print('\033[2J\033[H')


def create_box_str(contents: str, title: str = '', x: int = 1, y: int = 1) -> str:
    """Creates a box around the given text originating at (x, y),
    do not use ansi-escape sequences in the text entries"""

    entries = contents.splitlines()

    highest_width = len(title)
    for e in entries:
        if len(e) > highest_width:
            highest_width = e

    primary_mid = '\u2500'*(highest_width + len(str(len(entries))) + 2)
    result = '\033[{};{}H\u250c'.format(y, x) + primary_mid + '\u2510'
    last = '\u2514' + primary_mid + '\u2518'

    for i, e in enumerate(entries):
        result += '\u2502 {}. {} '.format(i, e)
        le = len(e)
        if le < highest_width:
            diff = highest_width - le
            result += '\033[{}C'.format(diff)
        result += '\u2502\033[E\033[{}G'.format(y)

    result += last

    return result

