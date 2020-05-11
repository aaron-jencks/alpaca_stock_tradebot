from pyrh import Robinhood
from multiprocessing import Queue, Lock
from queue import Full, Empty
from http.client import RemoteDisconnected
import time

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.objects.stockdescriptor import ManagedStock, Stock
# from login import username, password, verification_method


class PyrhAdapter(QSM):
    def __init__(self, name: str = 'pyrh_adapter'):
        super().__init__(name, ['pyrh_request', 'trade'])
        self.rbn = Robinhood()
        self.logged_in = False
        self.client_req = Queue()
        self.requests = Queue()
        self.request_lock = Lock()

    def setup_states(self):
        super().setup_states()
        self.mappings['login'] = self.login
        self.mappings['quote'] = self.quote
        self.mappings['buy'] = self.buy
        self.mappings['sell'] = self.sell

    def idle_state(self):
        try:
            req = self.client_req.get_nowait()
            self.append_state('pyrh_request', req)
        except Empty as _:
            pass

        super().idle_state()

    def trade_msg(self, msg: Message):
        transaction = msg.payload
        self.handler.send(Message('pyrh_request', 'buy' if transaction.buy else 'sell', transaction))

    def pyrh_request_msg(self, msg: Message):
        if msg.msg == 'logout':
            if self.logged_in:
                self.rbn.logout()
                print("Logged out")
                self.logged_in = False
        if msg.msg == 'quote':
            if not self.logged_in:
                self.append_state('login')
            self.append_state('quote', msg.payload)
        elif msg.msg == 'buy':
            if not self.logged_in:
                self.append_state('login')
            self.append_state('buy', msg.payload)
        elif msg.msg == 'sell':
            if not self.logged_in:
                self.append_state('login')
            self.append_state('sell', msg.payload)

    def login(self):
        while True:
            user = input('Username(email): ')
            pwd = input('Password: ')
            if self.rbn.login(user, pwd):
                print('Logged in successfully')
                self.logged_in = True
                break
            print('Something went wrong, try again?')
            continue

    def quote(self, acronym: str):
        while True:
            try:
                self.requests.put(self.rbn.get_quote(acronym))
                break
            except Full as _:
                print('requests queue is full, skipping...')
                break
            except Exception as _:
                print('Something went wrong, trying again')
                time.sleep(5)

    def buy(self, descriptor: ManagedStock):
        # self.rbn.place_buy_order(self.rbn.get_quote(descriptor.acronym)['instrument'], descriptor.shares)
        print("Buying {}".format(descriptor))

    def sell(self, descriptor: ManagedStock):
        # self.rbn.place_sell_order(self.rbn.get_quote(descriptor.acronym)['instrument'], descriptor.shares)
        print("Selling {}".format(descriptor))

    def get_quote(self, acronym: str) -> dict:
        self.request_lock.acquire()
        self.client_req.put(Message('pyrh_request', 'quote', acronym))
        d = self.requests.get()
        self.request_lock.release()
        return d

    def place_buy(self, s: ManagedStock):
        self.client_req.put(Message('pyrh_request', 'buy', s))

    def place_sell(self, s: ManagedStock):
        self.client_req.put(Message('pyrh_request', 'sell', s))
