
class LimitDescriptor:
    def __init__(self, limit_type: str = '%', buy: float = 0, sell: float = 0):
        self.limit_type = limit_type
        self.buy_price = buy
        self.sell_price = sell

    def __str__(self):
        return '{}: ({}, {})'.format(self.limit_type, self.buy_price, self.sell_price)
