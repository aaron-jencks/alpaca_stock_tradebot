from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from tradebot.adapters.sql_adapter import *
from tradebot.objects.stockdescriptor import ManagedStock, Stock, StockTransaction, StockUpdate
from tradebot.objects.balancedescriptor import BalanceUpdate
from tradebot.objects.limitdescriptor import LimitDescriptor

from multiprocessing import Queue, Lock
from queue import Empty


class StockVault(QSM):

    instance = None

    def __init__(self, name: str = 'vault'):
        super().__init__(name, ['vault_request'])
        self.requestq = Queue()
        self.req_lock = Lock()
        self.req_out = Queue()
        self.connection = None

    @staticmethod
    def setup_instance(name: str = 'vault'):
        if StockVault.instance is None:
            StockVault.instance = StockVault(name)
            StockVault.instance.start()

    def setup_states(self):
        super().setup_states()
        self.mappings['add_stock'] = self.add_stock
        self.mappings['add_stocks'] = self.add_stocks
        self.mappings['add_monitor'] = self.add_monitor
        self.mappings['add_monitors'] = self.add_monitors
        self.mappings['remove_stock'] = self.remove_stock
        self.mappings['remove_monitor'] = self.remove_monitor
        self.mappings['get_stock_names'] = self.get_stock_names
        self.mappings['get_info'] = self.get_info
        self.mappings['update_stock'] = self.update_stock
        self.mappings['update_monitor'] = self.update_monitor
        self.mappings['add_transaction'] = self.add_transaction
        self.mappings['add_balance_update'] = self.add_balance_update
        self.mappings['add_limit'] = self.add_limit
        self.mappings['update_limit'] = self.update_limit

    def initial_state(self):
        self.connection = setup_db()

    def idle_state(self):
        try:
            req = self.requestq.get_nowait()

            if req.msg in self.mappings:
                self.append_state(req.msg, req)
        except Empty as _:
            pass

        super().idle_state()

    def vault_request_msg(self, msg: Message):
        self.requestq.put(msg)

    # region add

    def add_stock(self, msg: Message):
        ins_str = setup_record_insertion('ManagedStocks',
                                         ManagedStock.get_tuple_names(), [msg.payload.to_tuple_str()])
        execute_query(self.connection, ins_str)

    def add_stocks(self, msg: Message):
        ins_str = setup_record_insertion('ManagedStocks',
                                         ManagedStock.get_tuple_names(),
                                         [r.to_tuple_str() for r in msg.payload])
        execute_query(self.connection, ins_str)

    def add_monitor(self, msg: Message):
        ins_str = setup_record_insertion('Stocks',
                                         Stock.get_tuple_names(), [msg.payload.to_tuple_str()])
        execute_query(self.connection, ins_str)

    def add_monitors(self, msg: Message):
        ins_str = setup_record_insertion('Stocks',
                                         Stock.get_tuple_names(),
                                         [r.to_tuple_str() for r in msg.payload])
        execute_query(self.connection, ins_str)

    def add_transaction(self, msg: Message):
        ins_str = setup_record_insertion('StockTransactions',
                                         StockTransaction.get_tuple_names(),
                                         [msg.payload.to_tuple_str()])
        execute_query(self.connection, ins_str)

    def add_balance_update(self, msg: Message):
        ins_str = setup_record_insertion('BalanceLedger',
                                         BalanceUpdate.get_tuple_names(),
                                         [msg.payload.to_tuple_str()])
        execute_query(self.connection, ins_str)

    def add_limit(self, msg: Message):
        ins_str = setup_record_insertion('StockLimits',
                                         LimitDescriptor.get_tuple_names(),
                                         [msg.payload.to_tuple_str()])
        execute_query(self.connection, ins_str)

    # endregion
    # region remove

    def remove_stock(self, msg: Message):
        execute_query(self.connection, 'DELETE FROM ManagedStocks WHERE id = {}'.format(msg.payload.table_id))

    def remove_monitor(self, msg: Message):
        execute_query(self.connection, 'DELETE FROM Stocks WHERE acronym = {}'.format(msg.payload.acronym))

    # endregion
    # region query

    def get_stock_names(self, msg: Message):
        results = execute_read_query(self.connection, 'SELECT acronym FROM Stocks')
        self.req_out.put([r[0] for r in results])

    def get_info(self, msg: Message):
        result = execute_read_query(self.connection, 'SELECT * FROM Stocks WHERE acronym=?{}'.format(msg.payload))[0]
        self.req_out.put(Stock(result[0], result[1], result[2], result[3], result[4]))

    # endregion
    # region updates

    def update_stock(self, msg: Message):
        # Update the managed stock
        update_str = setup_record_update('ManagedStocks', {
            'stock_acronym': msg.payload.acronym,
            'shares': msg.payload.shares,
            'last_price': msg.payload.last_price
        }, {
            'id': msg.payload.table_id
        })

        execute_query(self.connection, update_str)

    def update_limit(self, msg: Message):
        # Update the managed stock
        update_str = setup_record_update('StockLimits', {
            'type': msg.payload.limit_type,
            'upper': msg.payload.upper,
            'lower': msg.payload.lower
        }, {
            'managed_stock_id': msg.payload.managed_stock_id
        })

        execute_query(self.connection, update_str)

    def update_monitor(self, msg: Message):
        # Add update to the record table
        ins_str = setup_record_insertion('StockUpdates',
                                         StockUpdate.get_tuple_names(),
                                         [msg.payload.to_tuple_str()])
        execute_query(self.connection, ins_str)

        # Update the managed stock
        update_str = setup_record_update('Stocks', {
            'ask_price': msg.payload.ask_price,
            'bid_price': msg.payload.bid_price,
            'ask_size': msg.payload.ask_size,
            'bid_size': msg.payload.bid_size
        }, {
            'acronym': msg.payload.acronym
        })

        execute_query(self.connection, update_str)

    # endregion
