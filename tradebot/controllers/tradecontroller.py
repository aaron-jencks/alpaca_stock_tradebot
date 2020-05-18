from tradebot.objects.stockdescriptor import *
from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.objects.balancedescriptor import BalanceUpdate
from tradebot.controllers.stock_vault import StockVault


class TradeController(QSM):
    def __init__(self, name: str, balance: float):
        super().__init__(name, ['trade_control', 'trade_request'])
        self.stocks = {}
        self.balance = balance

    def setup_states(self):
        super().setup_states()
        self.mappings['buy_stock'] = self.buy_stock
        self.mappings['sell_stock'] = self.sell_stock
        self.mappings['load_from_db'] = self.reload_msg

    def reload_msg(self, msg: Message):
        print('Loading trade controller from the database')
        self.stocks = {}
        self.balance = 0
        for tid, acronym in StockVault.get_stock_ids_names():
            self.stocks[tid] = acronym
        self.balance = StockVault.get_balance()

    def trade_control_msg(self, msg: Message):
        if msg.msg == 'add':
            self.handler.send('vault_request', 'add_stock', msg.payload)
            self.append_state('load_from_db')
        elif msg.msg == 'remove':
            self.handler.send('vault_request', 'remove_stock', msg.payload)
            self.append_state('load_from_db')
        elif msg.msg == 'buy':
            self.append_state('buy_stock', msg.payload)
        elif msg.msg == 'sell':
            self.append_state('sell_stock', msg.payload)

    def buy_stock(self, s: ManagedStock):
        info = StockVault.get_info(s.acronym)
        if self.balance >= info.bid_price * s.shares:
            self.handler.send(Message('trade_balance_update', self.name, BalanceUpdate(self.balance)))
            self.handler.send(Message('trade', self.name, StockTransaction(s.table_id, s.acronym, True,
                                                                           info.bid_price, s.shares)))
            s.last_price = info.bid_price
            print("Buying {}".format(s))
        else:
            print('Rejecting transaction, insufficient funds')

    def sell_stock(self, s: ManagedStock):
        info = StockVault.get_info(s.acronym)
        self.balance += info.ask_price * s.shares
        self.handler.send(Message('trade_balance_update', self.name, BalanceUpdate(self.balance)))
        self.handler.send(Message('trade', self.name, StockTransaction(s.table_id, s.acronym, False,
                                                                       info.ask_price, s.shares)))
        s.last_price = info.ask_price
        print("Selling {}".format(s))
