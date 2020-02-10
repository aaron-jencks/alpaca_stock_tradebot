from WebsiteParser import WebsiteParser
from WebsiteDescriptor import WebsiteDescriptor, Website
from robinhood_api import *


class StockParser(WebsiteParser):
    """Represents a parser used to collect product data from the hyvee website"""

    def __init__(self, browser):
        super().__init__()

        self.browser = browser

    def parse(self) -> list:

        return find_recent_purchases(self.browser)
