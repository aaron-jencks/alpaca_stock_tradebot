from WebsiteDescriptor import *


class WebsiteParser:
    """Represents an interface for creating web parsing modules, contains a property for the url of the site to parse,
    and a method 'parse()' that parses said url."""

    def __init__(self, url: str = ''):
        self.url = url

    def parse(self) -> WebsiteDescriptor:
        print("Parser Triggered")
        return WebsiteDescriptor()
