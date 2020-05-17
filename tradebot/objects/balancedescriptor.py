import datetime as dt
from settings import date_format


class BalanceUpdate:
    def __init__(self, balance: float):
        self.balance = balance
        self.date = dt.datetime.now().strftime(date_format)

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'BalanceLedger', 'properties': {
            'balance': 'FLOAT NOT NULL',
            'date': 'text NOT NULL'
        }}

    @staticmethod
    def get_tuple_names() -> str:
        return '(balance, date)'

    def to_tuple_str(self) -> str:
        return '({}, "{}")'.format(self.balance, self.date)
