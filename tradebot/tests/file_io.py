import unittest

import tradebot.adapters.sql_adapter as sql
from tradebot.controllers.stock_vault import StockVault
from tradebot.messaging.message import MessageHandler


class SQLTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.vault = StockVault()
        self.client = MessageHandler('client_handler')

    def tearDown(self) -> None:
        self.vault.instance.join()
        self.client.join()

    def test_file_creation(self):
        sql.setup_files()
        self.assertTrue(True, 'Can create test files without error')


if __name__ == '__main__':
    unittest.main()
