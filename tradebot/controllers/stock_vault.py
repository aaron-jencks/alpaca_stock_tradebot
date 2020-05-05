from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message
from multiprocessing import Queue, Lock


class StockVault(QSM):

    instance = None

    def __init__(self, name: str = 'vault'):
        super().__init__(name, ['vault_config', 'vault_request'])
        self.requestq = Queue()
        self.req_lock = Lock()
        self.req_out = Queue()

    @staticmethod
    def setup_instance(name: str = 'vault'):
        if StockVault.instance is None:
            StockVault.instance = StockVault(name)
