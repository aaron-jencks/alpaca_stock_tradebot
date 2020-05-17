import re, json
from typing import Tuple

from tradebot.messaging.message import Message, MessageHandler
from tradebot.objects.commands.cli import AddCommand, RemoveCommand, UpdateCommand, ListCommand, \
    BuyCommand, SellCommand, ExportCommand, ImportCommand


cli_handler = None
commands = [AddCommand(), RemoveCommand(), UpdateCommand(), ListCommand(),
            BuyCommand(), SellCommand(), ExportCommand(), ImportCommand()]


def __setup_handler(name: str = 'cli'):
    global cli_handler

    if cli_handler is None:
        cli_handler = MessageHandler(name)


def parse_command(s: str):
    if cli_handler is None:
        __setup_handler()

    lines = s.strip().split(';')
    for l in lines:
        args = l.strip().split(' ')
        nargs = len(args)

        found = False

        print('Searching for {}'.format(args[0]))
        for c in commands:
            if args[0] == c.title:
                print('Found {}'.format(args[0]))
                data = c.parse(args[1:] if len(args) > 1 else [])
                c.handle(cli_handler, data)
                found = True

        if not found:
            print('{} not found, executing as json message'.format(args[0]))
            if nargs == 1:
                cli_handler.send(Message(args[0]))
            elif nargs == 2:
                cli_handler.send(Message(args[0], args[1]))
            elif nargs == 3:
                cli_handler.send(Message(args[0], args[1], json.loads(args[2])))
