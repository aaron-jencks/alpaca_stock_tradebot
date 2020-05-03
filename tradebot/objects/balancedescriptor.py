import datetime as dt


class BalanceUpdateDescriptor:
    def __init__(self, balance: float):
        self.balance = balance
        self.doy = dt.datetime.now().timetuple().tm_yday
        self.year = dt.date.today().year
        self.hour = dt.datetime.now().hour
        self.minute = dt.datetime.now().minute
        self.seconds = dt.datetime.now().second

    @staticmethod
    def get_headers() -> list:
        return ['doy', 'Year', 'Hour', 'Minute', 'Second', 'Balance']

    def to_array(self) -> list:
        return [self.doy, self.year, self.hour, self.minute, self.seconds, self.balance]
