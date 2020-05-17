from tradebot.objects.commands.command import Command, is_keyword, parse_variable


class TransactionCommand(Command):
    def __init__(self):
        super().__init__('')

    def parse(self, args: list) -> dict:
        data = {'id': args[0], 'acronym': args[1], 'shares': 1, 'price': -1}
        for a in range(2, len(args)):
            if is_keyword(args[a]):
                n, v = parse_variable(args[a])
                data[n] = v
            elif a == 2:
                data['shares'] = int(args[a])
            else:
                data['price'] = args[a]
        return data
