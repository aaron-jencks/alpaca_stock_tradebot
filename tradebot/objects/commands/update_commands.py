from tradebot.objects.commands.command import Command, parse_variable, is_keyword
from tradebot.messaging.message import MessageHandler, Message
from tradebot.objects.stockdescriptor import ManagedStock, Stock


class UpdateStock(Command):
    def __init__(self):
        super().__init__('stock')

    def parse(self, args: list) -> dict:
        data = {'title': 'stock', 'id': int(args[0]), 'acronym': '', 'shares': -1, 'price': -1.0}
        for a in range(1, len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 1:
                data['acronym'] = args[a]
            elif a == 2:
                data['shares'] = int(args[a])
            elif a == 3:
                data['price'] = float(args[a])
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('vault_request', 'update_stock', ManagedStock(data['acronym'], data['id'],
                                                                           data['shares'], data['price'])))


class UpdateMonitor(Command):
    def __init__(self):
        super().__init__('monitor')

    def parse(self, args: list) -> dict:
        data = {'title': 'monitor', 'acronym': args[0],
                'ask_price': -1.0, 'bid_price': -1.0, 'ask_size': -1, 'bid_size': -1}
        for a in range(1, len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 1:
                data['ask_price'] = float(args[a])
            elif a == 2:
                data['bid_price'] = float(args[a])
            elif a == 3:
                data['ask_size'] = int(args[a])
            else:
                data['bid_size'] = int(args[a])
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('vault_request', 'update_monitor', Stock(data['acronym'],
                                                                      data['ask_price'], data['bid_price'],
                                                                      data['ask_size'], data['bid_size'])))
