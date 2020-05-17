import datetime as dt

from tradebot.messaging.message import MessageHandler, Message
from tradebot.objects.stockdescriptor import ManagedStock, Stock, StockTransaction
from tradebot.objects.balancedescriptor import BalanceUpdate
from tradebot.objects.commands.command import Command, is_keyword, parse_variable
from tradebot.objects.limitdescriptor import LimitDescriptor
from settings import date_format


class AddStock(Command):
    def __init__(self):
        super().__init__('stock')

    def parse(self, args: list) -> dict:
        data = {'title': 'stock', 'acronym': args[0], 'shares': 1, 'buy_price': -1}
        for a in range(2, len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 1:
                data['shares'] = int(args[a])
            else:
                data['buy_price'] = args[a]
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('vault_request', 'add_stock', ManagedStock(data['acronym'],
                                                                        last_price=float(data['buy_price']),
                                                                        shares=int(data['shares']))))


class AddMonitor(Command):
    def __init__(self):
        super().__init__('monitor')

    def parse(self, args: list) -> dict:
        data = {'title': 'monitor', 'acronym': args[0]}
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('monitor_config', 'add', Stock(data['acronym'])))


class AddTransaction(Command):
    def __init__(self):
        super().__init__('transaction')

    def parse(self, args: list) -> dict:
        data = {'title': 'transaction', 'id': int(args[0]), 'shares': -1, 'price': -1.0,
                'date': dt.datetime.now().strftime(date_format)}
        for a in range(2, len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 1:
                data['shares'] = int(args[a])
            elif a == 2:
                data['price'] = float(args[a])
            else:
                data['date'] = dt.datetime.strptime(args[a], date_format)
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        trans = StockTransaction(data['id'], '', True, data['price'], data['shares'])
        trans.date = dt.datetime.strptime(data['date'], date_format)
        handler.send(Message('vault_request', 'add_transaction', trans))


class AddLimit(Command):
    def __init__(self):
        super().__init__('limit')

    def parse(self, args: list) -> dict:
        data = super().parse(args)
        if len(args) == 4:
            data['limit'] = LimitDescriptor(int(args[0]), args[1], float(args[2]), float(args[3]))
        elif len(args) == 3:
            data['limit'] = LimitDescriptor(int(args[0]), '%', float(args[1]), float(args[2]))
        else:
            data['limit'] = LimitDescriptor(int(args[0]), '%', 1.05, 0.95)
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('monitor_config', 'limit', data['limit']))


class AddBalance(Command):
    def __init__(self):
        super().__init__('balance')

    def parse(self, args: list) -> dict:
        data = {'title': 'balance', 'amount': float(args[0]), 'date': dt.datetime.now()}
        if len(args) == 2:
            data['date'] = dt.datetime.strptime(args[1], date_format)
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        up = BalanceUpdate(data['amount'])
        up.date = dt.datetime.strptime(data['date'], date_format)
        handler.send(Message('vault_request', 'add_balance_update', up))
