from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class TimerRelay(QSM):
    def __init__(self, name: str, target_msg: Message):
        super().__init__(name, ['timer'])
        self.target = target_msg

    def timer_msg(self, msg: Message):
        self.handler.send(self.target)
