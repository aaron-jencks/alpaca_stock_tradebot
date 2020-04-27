from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class TimerRelay(QSM):
    def __init__(self, name: str, target_msg: Message):
        super().__init__(name, ['timer'])
        self.target = target_msg

    def timer_msg(self, msg: Message):
        print('Relay {} triggered'.format(self.name))
        self.handler.send(self.target)


if __name__ == '__main__':
    from tradebot.controllers.timer import Timer
    from tradebot.messaging.message import MessageHandler

    t = Timer('timer1', 1)
    tr = TimerRelay('relay', Message('something'))
    rx = MessageHandler('receiver', ['something'])

    tr.start()
    t.start()

    while True:
        if rx.receive() is not None:
            print('Relay fired')
