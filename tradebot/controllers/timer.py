import time
import datetime as dt

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
        super().setup_states()
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


class MarketTimer(Timer):
    """A Normal Timer class that automatically pauses during after hours."""
    def idle_state(self):
        dow = dt.datetime.now().isoweekday()
        hour = dt.datetime.now().hour
        minute = dt.datetime.now().minute
        if not self.paused and ((dow == 6 or dow == 7) or
                                ((16 < hour < 9) or (hour == 9 and minute < 30))):
            print('Pausing Timer')
            self.paused = True
        elif self.paused and ((dow != 6 and dow != 7) and ((9 < hour < 16) or (hour == 9 and minute >= 30))):
            print('Unpausing Timer')
            self.paused = False
        super().idle_state()


if __name__ == "__main__":
    from tradebot.messaging.message import MessageHandler

    t = Timer('timer1')
    h = MessageHandler('timer_rx', ['timer'])
    t.start()

    while True:
        if h.receive() is not None:
            print('Timer triggered')
