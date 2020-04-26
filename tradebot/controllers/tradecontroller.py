from tradebot.objects.stockdescriptor import *
from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class TradeController(QSM):
    def __init__(self, name: str):
        super().__init__(name, ['trade_control'])
        self.stocks = []

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

    def buy_stock(self, s: StockDescriptor):
        self.handler.send(Message('trade', self.name, StockTransaction(s.acronym, True,
                                                                       s.bid_price, s.ask_price, s.shares)))
        print("Buying {}".format(s))

    def sell_stock(self, s: StockDescriptor):
        self.handler.send(Message('trade', self.name, StockTransaction(s.acronym, False,
                                                                       s.bid_price, s.ask_price, s.shares)))
        print("Selling {}".format(s))
