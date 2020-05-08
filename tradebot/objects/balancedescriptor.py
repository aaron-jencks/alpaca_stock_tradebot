import datetime as dt


class BalanceUpdate:
    def __init__(self, balance: float):
        self.balance = balance
        self.date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create_sql_table() -> dict:
        return {'name': 'BalanceLedger', 'properties': {
            'balance': 'FLOAT NOT NULL',
            'date': 'DATE NOT NULL'
        }}
