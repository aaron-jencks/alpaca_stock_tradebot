
class LimitDescriptor:
    def __init__(self, buy: float = 0, sell: float = 0):
        self.buy_price = buy
        self.sell_price = sell

    def __str__(self):
        return '({}, {})'.format(self.buy_price, self.sell_price)
