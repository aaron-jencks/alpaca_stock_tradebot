import datetime as dt


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


class StockTransaction(StockDescriptor):
    def __init__(self, acronym: str, buy: bool, price: float = 0, shares: int = 1):
        super().__init__(acronym, price, shares)
        self.buy = buy
        self.doy = dt.datetime.now().timetuple().tm_yday
        self.year = dt.date.today().year

    def __str__(self) -> str:
        return '{}/{} {} {} x {} for ${}'.format(self.doy, self.year,
                                                 'Buy' if self.buy else 'Sell', self.acronym, self.shares, self.price)

    @staticmethod
    def get_headers() -> list:
        return ['Day', 'Year', 'Buy_Sell', 'Name', 'Shares', 'Price']

    def to_array(self) -> list:
        return [self.doy, self.year, self.buy, self.acronym, self.shares, self.price]
