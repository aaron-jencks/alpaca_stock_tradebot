import unittest, time

from tradebot.messaging.message import MessageHandler
from tradebot.controllers.cli import parse_command
import tradebot.controllers.cli as cli
from tradebot.objects.stockdescriptor import ManagedStock
from tradebot.objects.limitdescriptor import LimitDescriptor


class CLITest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = MessageHandler('test_handler', ['trade_request', 'monitor_config', 'vault_request'])

    def tearDown(self) -> None:
        self.handler.join()
        cli.cli_handler = None

    def test_add(self):
        parse_command('add stock AAPL shares=10; add stock AAPL 1 3.0; add stock AAPL shares=10 price=4.50')
        msg = self.handler.receive()

        self.assertEqual(msg.title, 'vault_request', 'Add command should produce vault_request message')
        self.assertEqual(msg.msg, 'add_stock', 'Add command should produce an add_stock message')
        self.assertTrue(msg.payload == ManagedStock('AAPL', shares=10, last_price=-1))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == ManagedStock('AAPL', shares=1, last_price=3))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == ManagedStock('AAPL', shares=10, last_price=4.5))

    def test_remove(self):
        parse_command('remove stock 123; remove stock 123 10')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'vault_request', 'Remove command should produce vault_request message')
        self.assertEqual(msg.msg, 'remove_stock', 'Remove command should produce a remove_stock message')

        self.assertTrue(msg.payload == ManagedStock('None', table_id=123, shares=-1))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == ManagedStock('None', table_id=123, shares=10))

    def test_list(self):
        parse_command('list; list acronym AAPL')

        # msg = self.handler.receive()
        # self.assertEqual(msg.title, 'vault_request', 'List command should produce vault_request message')
        # self.assertEqual(msg.msg, 'get_stock_names', 'List command should produce a get_stock_names message')

    def test_limit(self):
        parse_command('add limit 123; add limit 123 % 1.05 0.95; add limit 123 0.95 0.85')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'monitor_config', 'List command should produce monitor_config message')
        self.assertEqual(msg.msg, 'limit', 'List command should produce a limit message')

        self.assertTrue(msg.payload == LimitDescriptor(123))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == LimitDescriptor(123))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == LimitDescriptor(123, upper=0.95, lower=0.85))

    def test_buy(self):
        parse_command('buy AAPL; buy AAPL 10; buy AAPL 10 3.75')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'trade_request', 'Buy command should produce a trade_request message')
        self.assertEqual(msg.msg, 'buy', 'Buy command should produce a buy message')

        self.assertTrue(msg.payload == ManagedStock('AAPL', last_price=-1))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == ManagedStock('AAPL', shares=10, last_price=-1))

        msg = self.handler.receive()
        self.assertTrue(msg.payload == ManagedStock('AAPL', shares=10, last_price=3.75))

    def test_sell(self):
        parse_command('sell 123; sell 123 10')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'trade_request', 'Sell command should produce a trade_request message')
        self.assertEqual(msg.msg, 'sell', 'Sell command should produce a sell message')

        self.assertEqual(msg.payload['id'], 123)
        self.assertEqual(msg.payload['shares'], -1)

        msg = self.handler.receive()
        self.assertEqual(msg.payload['id'], 123)
        self.assertEqual(msg.payload['shares'], 10)

    def test_update(self):
        parse_command('update')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'monitor_config', 'Update command should produce a monitor_config message')
        self.assertEqual(msg.msg, 'update', 'Update command should produce an update message')

    def test_export(self):
        parse_command('export')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'all', 'Export command should produce a global message')
        self.assertEqual(msg.msg, 'save', 'Export command should produce an save message')

    def test_import(self):
        parse_command('import')

        msg = self.handler.receive()
        self.assertEqual(msg.title, 'all', 'Import command should produce a global message')
        self.assertEqual(msg.msg, 'load', 'Import command should produce an load message')
