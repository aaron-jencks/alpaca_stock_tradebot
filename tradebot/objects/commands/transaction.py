from tradebot.objects.commands.command import Command, is_keyword, parse_variable


class TransactionCommand(Command):
    def __init__(self, buy: bool):
        super().__init__('')
        self.buy = buy

    def parse(self, args: list) -> dict:
        if self.buy:
            data = {'acronym': args[0], 'shares': 1, 'price': -1}
        else:
            data = {'id': int(args[0]), 'shares': -1, 'price': -1}
        for a in range(1, len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 1:
                data['shares'] = int(args[a])
            else:
                data['price'] = float(args[a])
        return data
