
class LimitDescriptor:
    def __init__(self, managed_stock_id: int, limit_type: str = '%', upper: float = 1.05, lower: float = 0.95):
        self.managed_stock_id = managed_stock_id
        self.limit_type = limit_type
        self.upper = upper
        self.lower = lower

    def __eq__(self, other):
        if isinstance(other, LimitDescriptor):
            return other.limit_type == self.limit_type and \
                   other.upper == self.upper and \
                   other.lower == self.lower
        return False

    def check_buy(self, sell_price: float, ask_price: float) -> bool:
        print('comparing {} to {} with respect to the limit {}({},{})'.format(ask_price, sell_price,
                                                                              self.limit_type,
                                                                              self.upper, self.lower))
        if self.limit_type == '%':
            return ask_price <= sell_price * self.lower
        elif self.limit_type == '#':
            return ask_price <= sell_price - self.lower
        elif self.limit_type == '$':
            return ask_price <= self.lower
        else:
            print('Unrecognized limit type {}'.format(self.limit_type))

    def check_sell(self, buy_price: float, bid_price: float) -> bool:
        print('comparing {} to {} with respect to the limit {}({},{})'.format(bid_price, buy_price,
                                                                              self.limit_type,
                                                                              self.upper, self.lower))
        if self.limit_type == '%':
            return bid_price >= buy_price * self.upper
        elif self.limit_type == '#':
            return bid_price >= buy_price + self.upper
        elif self.limit_type == '$':
            return bid_price >= self.upper
        else:
            print('Unrecognized limit type {}'.format(self.limit_type))

    def __str__(self):
        return '{}: ({}, {})'.format(self.limit_type, self.upper, self.lower)

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'StockLimits', 'properties': {
            'managed_stock_id': 'INTEGER NOT NULL',
            'type': 'TEXT NOT NULL',
            'upper': 'FLOAT',
            'lower': 'FLOAT',
            'FOREIGN KEY (managed_stock_id)': 'REFERENCES ManagedStocks (id)'
        }}

    @staticmethod
    def get_tuple_names() -> str:
        return '(managed_stock_id, type, upper, lower)'

    def to_tuple_str(self) -> str:
        return '({}, {}, {}, {})'.format(self.managed_stock_id, self.limit_type, self.upper, self.lower)
