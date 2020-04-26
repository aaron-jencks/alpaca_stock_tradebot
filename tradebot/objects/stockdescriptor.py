import datetime as dt


class Stock:
    def __init__(self, acronym: str = '', buy_price: float = 0, sell_price: float = 0):
        self.acronym = acronym
        self.ask_price = sell_price
        self.bid_price = buy_price

    def __str__(self):
        return '{}: ${}/${}'.format(self.acronym, self.ask_price, self.bid_price)


class StockDescriptor(Stock):
    def __init__(self, acronym: str, buy_price: float = 0, sell_price: float = 0, shares: int = 1):
        super().__init__(acronym, buy_price, sell_price)
        self.shares = shares

    def __str__(self):
        return '{}: ${}/${} x {}'.format(self.acronym, self.ask_price, self.bid_price, self.shares)


class StockTransaction(StockDescriptor):
    def __init__(self, acronym: str, buy: bool, buy_price: float = 0, sell_price: float = 0, shares: int = 1):
        super().__init__(acronym, buy_price, sell_price, shares)
        self.buy = buy
        self.doy = dt.datetime.now().timetuple().tm_yday
        self.year = dt.date.today().year

    def __str__(self) -> str:
        return '{}/{} {} {} x {} for ${}'.format(self.doy, self.year,
                                                 'Buy' if self.buy else 'Sell', self.acronym, self.shares,
                                                 self.ask_price if self.buy else self.bid_price)

    @staticmethod
    def get_headers() -> list:
        return ['Day', 'Year', 'Buy_Sell', 'Name', 'Shares', 'Ask_Price', 'Bid_Price']

    def to_array(self) -> list:
        return [self.doy, self.year, self.buy, self.acronym, self.shares, self.ask_price, self.bid_price]
