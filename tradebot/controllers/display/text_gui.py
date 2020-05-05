from typing import List

from tradebot.messaging.application import Application
from tradebot.messaging.qsm import QSM


class TextApplication(Application):
    def __init__(self, name: str, modules: List[QSM]):
        super().__init__(name, modules)
        self.menus = {}
