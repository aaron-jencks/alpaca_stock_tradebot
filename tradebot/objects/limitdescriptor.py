
class LimitDescriptor:
    def __init__(self, limit_type: str = '%', buy: float = 0, sell: float = 0):
        self.limit_type = limit_type
        self.buy_price = buy
        self.sell_price = sell

    def check_buy(self, sell_price: float, ask_price: float) -> bool:
        if self.limit_type == '%':
            return ask_price <= sell_price * self.buy_price
        elif self.limit_type == '#':
            return ask_price <= sell_price - self.buy_price
        elif self.limit_type == '$':
            return ask_price <= self.buy_price
        else:
            print('Unrecognized limit type {}'.format(self.limit_type))

    def check_sell(self, buy_price: float, bid_price: float) -> bool:
        if self.limit_type == '%':
            return bid_price >= buy_price * self.sell_price
        elif self.limit_type == '#':
            return bid_price >= buy_price + self.sell_price
        elif self.limit_type == '$':
            return bid_price >= self.sell_price
        else:
            print('Unrecognized limit type {}'.format(self.limit_type))

    def __str__(self):
        return '{}: ({}, {})'.format(self.limit_type, self.buy_price, self.sell_price)
