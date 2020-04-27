import time

from tradebot.messaging.message import Message
from tradebot.messaging.qsm import QSM


class Timer(QSM):
    """Represents an asynchronous timer, it can be configured by setting the interval, once the interval is set,
    then the timer will proceed to send out a queue item in it's Tx property once every "interval" seconds.
    The default interval is 1 second."""

    def __init__(self, name: str, interval: int = 1):
        super().__init__(name, ['timer_config'])  # Sets up the timer to receive 'timer_config' messages
        self.interval = interval
        self.paused = False
        self.start_time = time.time()

    def setup_states(self):
        self.mappings['trigger'] = self.trigger_state

    def initial_state(self):
        self.append_state('trigger')

    def timer_config_msg(self, msg: Message):
        if msg.msg == 'interval':
            self.interval = msg.payload
            print('Updated timer interval to {}'.format(msg.payload))
        elif msg.msg == 'pause':
            self.paused = msg.payload if msg.payload is not None else True
            print('{} timer'.format('Paused' if self.paused else 'Unpaused'))

    def idle_state(self):
        super().idle_state()
        if not self.paused and time.time() - self.start_time >= self.interval:
            self.append_state('trigger')

    def trigger_state(self):
        self.handler.send(Message('timer', self.name))
        print('Timer {} triggered'.format(self.name))
        self.start_time = time.time()
        time.sleep(self.interval)


if __name__ == "__main__":
    from tradebot.messaging.message import MessageHandler

    t = Timer('timer1')
    h = MessageHandler('timer_rx', ['timer'])
    t.start()

    while True:
        if h.receive() is not None:
            print('Timer triggered')
