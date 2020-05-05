from typing import Callable

from tradebot.gui.menu import Menu


class ExitItem:
    pass


class MenuEntry:
    def __init__(self, name: str, target: object):
        self.name = name
        self.target = target

    def __str__(self) -> str:
        return self.name

    def choose(self):
        if isinstance(self.target, Menu):
            return self.target
        elif isinstance(self.target, Callable):
            return self.target()
