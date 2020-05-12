import unittest
import os.path as path
import os
import time

import tradebot.adapters.sql_adapter as sql
from tradebot.controllers.stock_vault import StockVault
from tradebot.messaging.message import MessageHandler, Message
from settings import file_location, db_name
from tradebot.objects.stockdescriptor import *


class SQLTestCase(unittest.TestCase):

    def setUp(self) -> None:
        StockVault.setup_instance(db_directory='/tmp/robin_test_db')
        self.client = MessageHandler('client_handler')

    def tearDown(self) -> None:
        StockVault.instance.join()
        self.client.join()
        with os.scandir('/tmp/robin_test_db/') as it:
            for entry in it:
                os.remove(entry.path)
        os.rmdir('/tmp/robin_test_db')

    def test_file_creation(self):
        self.assertTrue(path.exists(path.join('/tmp/robin_test_db', db_name)), 'Can create test files without error')

    def test_add_stock(self):
        self.client.send(Message('vault_request', 'add_monitor', Stock('AAPL')))
        time.sleep(0.1)
        names = StockVault.get_stock_names()
        self.assertTrue('AAPL' in names, 'An inserted stock should appear in the database')


if __name__ == '__main__':
    unittest.main()
