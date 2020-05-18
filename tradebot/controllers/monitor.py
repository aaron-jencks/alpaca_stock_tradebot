import time

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.objects.stockdescriptor import *
from tradebot.objects.limitdescriptor import *
from tradebot.adapters.pyrh_adapter import PyrhAdapter
from tradebot.controllers.stock_vault import StockVault


class StockMonitor(QSM):
    def __init__(self, name: str,
                 managed_stocks: list = None, stock_limits: dict = None,
                 robinhood_adapter: PyrhAdapter = None):
        super().__init__(name, ['monitor_config'])
        self.history = managed_stocks if managed_stocks is not None else []
        self.stocks = managed_stocks if managed_stocks is not None else []
        self.limits = stock_limits if stock_limits is not None else {}
        self.adapter = robinhood_adapter if robinhood_adapter is not None else PyrhAdapter()
        if robinhood_adapter is None:
            self.adapter.start()
            time.sleep(1)

    def setup_states(self):
        super().setup_states()
        self.mappings['update_prices'] = self.update_prices
        self.mappings['check_triggers'] = self.check_triggers
        self.mappings['load_from_db'] = self.reload_msg

    def reload_msg(self, msg: Message):
        print('Loading the monitor from the database')
        self.stocks = []
        self.history = []
        self.limits = {}
        acronyms = StockVault.get_stock_names()
        for a in acronyms:
            self.stocks.append(Stock(a))
            self.history.append(Stock(a))
        for lm in StockVault.get_limits():
            tid, typ, upp, lwr = lm
            self.limits[tid] = LimitDescriptor(tid, typ, upp, lwr)
        self.append_state('update_prices')

    def monitor_config_msg(self, msg: Message):
        if msg.msg == 'add':
            self.handler.send(Message('vault_request', 'add_monitor', msg.payload))
            time.sleep(0.5)
            self.append_state('load_from_db', msg)
        elif msg.msg == 'remove':
            self.handler.send(Message('vault_request', 'remove_monitor', msg.payload))
            time.sleep(0.5)
            self.append_state('load_from_db', msg)
        elif msg.msg == 'update':
            self.append_state('update_prices')
        elif msg.msg == 'check_triggers':
            self.append_state('check_triggers')

    def update_prices(self):
        for s in self.stocks:
            quote = self.adapter.get_quote(s.acronym)
            prev_ask = s.ask_price
            prev_bid = s.bid_price
            s.ask_price = float(quote['ask_price'])
            s.bid_price = float(quote['bid_price'])
            print('Updated {}'.format(s))
            if prev_ask != s.ask_price or prev_bid != s.bid_price:
                self.handler.send(Message('monitor_update', self.name,
                                          StockUpdate(-1, s.acronym, s.ask_price, int(quote['ask_size']),
                                                      s.bid_price, int(quote['bid_size']))))
        self.append_state('check_triggers')

    def check_triggers(self):
        limits = StockVault.get_stock_ids_names()
        for tid, acronym in limits:
            index = self.history.index(Stock(acronym))
            s = self.stocks[index]
            if self.limits[tid].check_buy(self.history[index].bid_price, s.ask_price):
                self.handler.send(Message('trade_control', 'buy', s))
            elif self.limits[s.acronym].check_sell(self.history[index].ask_price, s.bid_price):
                self.handler.send(Message('trade_control', 'sell', s))
