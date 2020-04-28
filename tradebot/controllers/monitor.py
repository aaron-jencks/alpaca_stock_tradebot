import time

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.objects.stockdescriptor import *
from tradebot.objects.limitdescriptor import *
from tradebot.adapters.pyrh_adapter import PyrhAdapter


class StockMonitor(QSM):
    def __init__(self, name: str,
                 managed_stocks: list = None, stock_limits: dict = None,
                 robinhood_adapter: PyrhAdapter = None, stdin_port: int = 1000):
        super().__init__(name, ['monitor_config'], stdin_port)
        self.stocks = managed_stocks if managed_stocks is not None else []
        self.limits = stock_limits if stock_limits is not None else {}
        self.adapter = robinhood_adapter if robinhood_adapter is not None else PyrhAdapter(stdin_port=stdin_port)
        if robinhood_adapter is None:
            self.adapter.start()
            time.sleep(1)

    def setup_states(self):
        super().setup_states()
        self.mappings['update_prices'] = self.update_prices
        self.mappings['check_triggers'] = self.check_triggers

    def monitor_config_msg(self, msg: Message):
        if msg.msg == 'add':
            self.stocks.append(msg.payload)
        elif msg.msg == 'remove':
            self.stocks.remove(msg.payload)
        elif msg.msg == 'update':
            self.append_state('update_prices')
        elif msg.msg == 'check_triggers':
            self.append_state('check_triggers')

    def update_prices(self):
        for s in self.stocks:
            quote = self.adapter.get_quote(s.acronym)
            s.ask_price = quote['ask_price']
            s.bid_price = quote['bid_price']
            print('Updated {}'.format(s))
        self.append_state('check_triggers')

    def check_triggers(self):
        for s in self.stocks:
            if s.ask_price < self.limits[s.acronym].buy_price:
                self.handler.send(Message('trade_control', 'buy', s))
            elif s.bid_price > self.limits[s.acronym].sell_price:
                self.handler.send(Message('trade_control', 'sell', s))
