
class Stock:
    def __init__(self, acronym: str = '', price: float = 0):
        self.acronym = acronym
        self.price = price

    def __str__(self):
        return '{}: ${}'.format(self.acronym, self.price)


class StockDescriptor(Stock):
    def __init__(self, acronym: str, price: float = 0, shares: int = 1):
        super().__init__(acronym, price)
        self.shares = shares

    def __str__(self):
        return '{}: ${} x {}'.format(self.acronym, self.price, self.shares)
