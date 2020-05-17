from tradebot.controllers.stock_vault import StockVault
from tradebot.objects.stockdescriptor import ManagedStock
from tradebot.messaging.message import MessageHandler, Message
from tradebot.objects.commands.command import PolyCommand, Command, is_keyword, parse_variable
from tradebot.objects.commands.add_commands import AddStock, AddMonitor, AddTransaction, AddLimit, AddBalance
from tradebot.objects.commands.remove_commands import RemoveStock, RemoveMonitor
from tradebot.objects.commands.update_commands import UpdateStock, UpdateMonitor
from tradebot.objects.commands.transaction import TransactionCommand


class AddCommand(PolyCommand):
    def __init__(self):
        super().__init__('add')
        self.commands += [AddStock(), AddMonitor(), AddTransaction(), AddLimit(), AddBalance()]


class RemoveCommand(PolyCommand):
    def __init__(self):
        super().__init__('remove')
        self.commands += [RemoveStock(), RemoveMonitor()]


class UpdateCommand(PolyCommand):
    def __init__(self):
        super().__init__('update')
        self.commands += [UpdateStock(), UpdateMonitor(), AddLimit()]

    def parse(self, args: list) -> dict:
        data = super().parse(args)
        if len(data) == 1:
            print('Sending monitor update message')
            data['title'] = 'force'
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        if data['title'] == 'force':
            handler.send(Message('monitor_config', 'update'))
        else:
            super().handle(handler, data)


class ListCommand(Command):
    def __init__(self):
        super().__init__('list')

    def parse(self, args: list) -> dict:
        data = {'type': 'acronym', 'keyword': 'all'}
        for a in range(len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 0:
                data['type'] = args[a]
            else:
                data['keyword'] = args[a]
        return data

    def handle(self, handler: MessageHandler, data: dict) -> None:
        if data['type'] == 'acronym':
            names = StockVault.get_stock_names()
            if names is not None:
                result = '['
                for n in names:
                    result += '{}, '.format(n)
                print((result[:-2] + ']') if len(names) > 0 else '[]')
            else:
                print('No Stocks found')
        elif data['type'] == 'id':
            names = StockVault.get_stock_ids()
            if names is not None:
                result = '['
                for n in names:
                    result += '{}, '.format(n)
                print((result[:-2] + ']') if len(names) > 0 else '[]')
            else:
                print('No Stocks found')


class BuyCommand(Command):
    def __init__(self):
        super().__init__('buy')

    def parse(self, args: list) -> dict:
        return TransactionCommand(True).parse(args)

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('trade_request', 'buy', ManagedStock(data['acronym'],
                                                                  last_price=float(data['price']),
                                                                  shares=int(data['shares']))))


class SellCommand(Command):
    def __init__(self):
        super().__init__('sell')

    def parse(self, args: list) -> dict:
        return TransactionCommand(False).parse(args)

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('trade_request', 'sell', data))


class ExportCommand(Command):
    def __init__(self):
        super().__init__('export')

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('all', 'save'))


class ImportCommand(Command):
    def __init__(self):
        super().__init__('import')

    def handle(self, handler: MessageHandler, data: dict) -> None:
        handler.send(Message('all', 'load'))
