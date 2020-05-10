import unittest

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class TestQSM(QSM):
    pass


class QSMTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.uut = TestQSM('uut')
        self.uut.start()

    def test_joinable(self):
        self.uut.join()
        self.assertTrue(True, 'QSMs are joinable')


if __name__ == '__main__':
    unittest.main()
