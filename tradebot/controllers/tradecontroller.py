from tradebot.objects.stockdescriptor import *
from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.objects.balancedescriptor import BalanceUpdate


class TradeController(QSM):
    def __init__(self, name: str, balance: float):
        super().__init__(name, ['trade_control'])
        self.stocks = []
        self.balance = balance

    def setup_states(self):
        super().setup_states()
        self.mappings['buy_stock'] = self.buy_stock
        self.mappings['sell_stock'] = self.sell_stock

    def trade_control_msg(self, msg: Message):
        if msg.msg == 'add':
            self.stocks.append(msg.payload)
        elif msg.msg == 'remove':
            self.stocks.remove(msg.payload)
        elif msg.msg == 'buy':
            self.append_state('buy_stock', msg.payload)
        elif msg.msg == 'sell':
            self.append_state('sell_stock', msg.payload)

    def buy_stock(self, s: ManagedStock):
        if self.balance >= s.ask_price * s.shares:
            self.handler.send(Message('trade_balance_update', self.name, BalanceUpdate(self.balance)))
            self.handler.send(Message('trade', self.name, StockTransaction(s.acronym, True,
                                                                           s.bid_price, s.ask_price, s.shares)))
            print("Buying {}".format(s))
        else:
            print('Rejecting transaction, insufficient funds')

    def sell_stock(self, s: ManagedStock):
        self.balance += s.bid_price * s.shares
        self.handler.send(Message('trade_balance_update', self.name, BalanceUpdate(self.balance)))
        self.handler.send(Message('trade', self.name, StockTransaction(s.acronym, False,
                                                                       s.bid_price, s.ask_price, s.shares)))
        print("Selling {}".format(s))
