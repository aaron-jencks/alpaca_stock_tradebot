from typing import Tuple

from tradebot.messaging.message import MessageHandler


def is_keyword(s: str) -> bool:
    return s.find('=') >= 0


def parse_variable(s: str) -> Tuple[str, str]:
    n, v = s.split('=')
    return n, v


class Command:

    def __init__(self, title: str):
        self.title = title

    def parse(self, args: list) -> dict:
        return {'title': self.title}

    def handle(self, handler: MessageHandler, data: dict) -> None:
        pass

    def help(self) -> str:
        return ""


class PolyCommand(Command):
    def __init__(self, title: str):
        super().__init__(title)
        self.commands = []

    def parse(self, args: list) -> dict:
        if len(args) > 0:
            for c in self.commands:
                if c.title == args[0]:
                    return c.parse(args[1:])
        return super().parse(args)

    def handle(self, handler: MessageHandler, data: dict) -> None:
        for c in self.commands:
            if c.title == data['title']:
                c.handle(handler, data)
