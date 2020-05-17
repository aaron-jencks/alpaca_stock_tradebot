from tradebot.objects.commands.command import Command
from tradebot.messaging.message import Message, MessageHandler
from tradebot.objects.stockdescriptor import ManagedStock, Stock


class RemoveStock(Command):
    def __init__(self):
        super().__init__('stock')

    def parse(self, args: list) -> dict:
        data = {'title': 'stock', 'id': int(args[0]), 'shares': -1}
        if len(args) == 2:
            data['shares'] = int(args[1])
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('vault_request', 'remove_stock', ManagedStock('', data['id'], data['shares'])))


class RemoveMonitor(Command):
    def __init__(self):
        super().__init__('monitor')

    def parse(self, args: list) -> dict:
        data = {'title': 'monitor', 'acronym': args[0]}
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('monitor_config', 'remove', Stock(data['acronym'])))
