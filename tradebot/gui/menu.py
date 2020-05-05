from typing import Dict

from tradebot.gui.menu_entry import MenuEntry


class Menu:
    def display(self):
        pass

    def interact(self):
        pass


class RadioMenu(Menu):
    def __init__(self, entries: Dict[str, MenuEntry]):
        self.entries = entries
