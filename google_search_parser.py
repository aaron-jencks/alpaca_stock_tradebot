from WebsiteParser import WebsiteParser
from WebsiteDescriptor import WebsiteDescriptor, Website
from hyvee_api import *

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class GoogleParser(WebsiteParser):
    """Represents a parser used to collect product data from the hyvee website"""

    browser = None
    logged_in = False

    def __init__(self, username: str, password: str):
        super().__init__()

        self.username = username
        self.password = password

        if GoogleParser.browser is None:
            foptions = Options()
            foptions.headless = False  # True
            GoogleParser.browser = webdriver.Firefox(options=foptions)

    def __del__(self):
        if self.browser:
            GoogleParser.browser.close()
            GoogleParser.browser = None

    def parse(self) -> list:
        if not self.logged_in:
            login(self.browser, self.username, self.password)
            self.logged_in = True

        return find_recent_purchases(self.browser, self.logged_in)
