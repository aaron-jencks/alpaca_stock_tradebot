from typing import List

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class Application(QSM):
    def __init__(self, name: str, modules: List[QSM]):
        super().__init__(name)
        self.modules = modules

    def initial_state(self):
        for m in self.modules:
            m.start()

    def exit_state(self):
        self.handler.send(Message('EXIT'))
        for m in self.modules:
            m.join()
        self.handler.join()
        super().exit_state()
