import datetime as dt

from numpy import NaN


class Website:
    """Represents one of the websites that the scraper needs to visit, contains most of the datat that would
    hypothetically be collected from the website."""

    def __init__(self, name: str = '', price: float = NaN):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return "{}: ${:03,.2f}".format(self.name, round(self.price, 2))


class WebsiteDescriptor:
    """Represents one of the websites that the scraper needs to visit, contains all of the data that would
    hypothetically be collected from the website. Also adds the day of the year, and the year."""

    def __init__(self, w: Website = None):
        self.name = w.name if w else ''
        self.price = w.price if w else NaN
        self.doy = dt.datetime.now().timetuple().tm_yday
        self.year = dt.date.today().year

    def __str__(self) -> str:
        return "{}/{}: {}: price: ${:03,.2f}".format(
            self.doy, self.year,
            self.name, round(self.price, 2)
        )

    @staticmethod
    def get_headers() -> list:
        return ["day_of_year", "year", "product_name", "price"]

    def to_array(self) -> list:
        return [self.doy, self.year, self.name, self.price]

    def to_dict(self) -> dict:
        result = {}
        arr = self.to_array()
        for i, h in enumerate(self.get_headers()):
            result[h] = arr[i]
        return result
