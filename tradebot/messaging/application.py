from typing import List

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.gui.menu import Menu
from tradebot.gui.menu_entry import ExitItem


class Application(QSM):
    def __init__(self, name: str, main_menu: Menu, modules: List[QSM]):
        super().__init__(name)
        self.modules = modules
        self.menu_stack = [main_menu]

    def setup_states(self):
        super().setup_states()
        self.mappings['event_loop'] = self.event_loop

    def initial_state(self):
        for m in self.modules:
            m.start()
        self.append_state('event_loop')

    def event_loop(self):
        while len(self.menu_stack) > 0:
            e = self.menu_stack[-1]
            e.display()
            t = e.interact()
            if t is None:
                continue
            elif isinstance(t, ExitItem):
                self.menu_stack.pop(-1)
            else:
                self.menu_stack.append(t)

    def exit_state(self):
        self.handler.send(Message('EXIT'))
        for m in self.modules:
            m.join()
        self.handler.join()
        super().exit_state()
