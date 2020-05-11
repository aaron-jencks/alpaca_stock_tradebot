import datetime as dt


def get_sql_tables() -> list:
    return [Stock.create_sql_table(),
            ManagedStock.create_sql_table(),
            StockUpdate.create_sql_table(),
            StockTransaction.create_sql_table()]


class Stock:
    def __init__(self, acronym: str = '',
                 ask_price: float = 0, bid_price: float = 0,
                 ask_size: int = 1, bid_size: int = 1):
        self.acronym = acronym
        self.ask_price = ask_price
        self.bid_price = bid_price
        self.ask_size = ask_size
        self.bid_size = bid_size

    def __str__(self):
        return '{}: (${} x{})/(${} x{})'.format(self.acronym,
                                                self.ask_price, self.ask_size,
                                                self.bid_price, self.bid_size)

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'Stocks', 'properties': {'acronym': 'text primary key',
                                                 'ask_price': 'float',
                                                 'bid_price': 'float',
                                                 'ask_size': 'integer',
                                                 'bid_size': 'integer'}}

    @staticmethod
    def get_tuple_names() -> str:
        return '(acronym, ask_price, bid_price, ask_size, bid_size)'

    def to_tuple_str(self) -> str:
        return '("{}", {}, {}, {}, {})'.format(self.acronym,
                                               self.ask_price, self.bid_price,
                                               self.ask_size, self.bid_size)


class ManagedStock:
    def __init__(self, acronym: str, table_id: int = -1, shares: int = 1, last_price: float = 0):
        self.table_id = table_id
        self.acronym = acronym
        self.shares = shares
        self.last_price = last_price

    def __str__(self):
        return '{}: ${} x {}'.format(self.acronym, self.last_price, self.shares)

    def __eq__(self, other):
        if isinstance(other, ManagedStock):
            return other.acronym == self.acronym and \
                   other.shares == self.shares and \
                   other.last_price == self.last_price
        else:
            return False

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'ManagedStocks', 'properties': {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                                                        'stock_acronym': 'TEXT NOT NULL',
                                                        'shares': 'INTEGER NOT NULL',
                                                        'last_price': 'FLOAT',
                                                        'FOREIGN KEY (stock_acronym)': 'REFERENCES Stocks (acronym)'}}

    @staticmethod
    def get_tuple_names() -> str:
        return '(stock_acronym, shares, last_price)'

    def to_tuple_str(self) -> str:
        return '("{}", {}, {})'.format(self.acronym, self.shares, self.last_price)


class StockUpdate(Stock):
    def __init__(self, table_id: int,
                 acronym: str,
                 ask_price: float = 0, ask_size: int = 1,
                 bid_price: float = 0, bid_size: int = 1):
        super().__init__(acronym, ask_price, bid_price, ask_size, bid_size)
        self.table_id = table_id
        self.date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return '{} '.format(self.date) + super().__str__()

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'StockUpdates', 'properties': {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                                                       'stock_acronym': 'TEXT NOT NULL',
                                                       'ask_price': 'FLOAT',
                                                       'bid_price': 'FLOAT',
                                                       'ask_size': 'INTEGER',
                                                       'bid_size': 'INTEGER',
                                                       'date': 'text NOT NULL',
                                                       'FOREIGN KEY (stock_acronym)': 'REFERENCES Stocks (acronym)'}}

    @staticmethod
    def get_tuple_names() -> str:
        return '(stock_acronym, ask_price, bid_price, ask_size, bid_size, date)'

    def to_tuple_str(self) -> str:
        return '("{}", {}, {}, {}, {}, "{}")'.format(self.acronym,
                                                     self.ask_price, self.bid_price,
                                                     self.ask_size, self.bid_size,
                                                     self.date)


class StockTransaction:
    def __init__(self, managed_stock_id: int, acronym: str, buy: bool, price: float = 0, shares: int = 1):
        self.managed_stock_id = managed_stock_id
        self.acronym = acronym
        self.buy = buy
        self.price = price
        self.shares = shares
        self.date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return '{} {} ({} x {}) for ${}'.format(self.date,
                                                'Buy' if self.buy else 'Sell', self.acronym, self.shares,
                                                self.price)

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'StockTransactions', 'properties': {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                                                            'managed_stock_id': 'TEXT NOT NULL',
                                                            'acronym': 'TEXT',
                                                            'buy_sell': 'BOOL NOT NULL',
                                                            'price': 'FLOAT NOT NULL',
                                                            'date': 'text NOT NULL',
                                                            'FOREIGN KEY (managed_stock_id)':
                                                                'REFERENCES ManagedStocks (id)'}}

    @staticmethod
    def get_tuple_names() -> str:
        return '(managed_stock_id, acronym, buy_sell, price, date)'

    def to_tuple_str(self) -> str:
        return '({}, "{}", {}, {}, "{}")'.format(self.managed_stock_id, self.acronym, self.buy, self.price, self.date)
