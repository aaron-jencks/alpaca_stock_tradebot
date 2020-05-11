import unittest
import os.path as path
import time

from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message, MessageHandler
from tradebot.controllers.json_controller import JSONController
from settings import state_save_file


output_directory = '/tmp/robin_test'


class TestQSM(QSM):
    def __init__(self, name: str):
        super().__init__(name)

    @property
    def dict(self) -> dict:
        return {'name': self.name}

    @staticmethod
    def from_dict(d: dict) -> object:
        sm = TestQSM(d['name'])
        return sm


class StateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.uut = TestQSM('test')
        self.uut.start()

        self.jcontr = JSONController('test_json', output_directory, 1)
        self.jcontr.start()

        self.client = MessageHandler('client')

    def tearDown(self) -> None:
        self.uut.join()
        self.jcontr.join()
        self.client.join()

    def test_save(self):
        self.client.send(Message('json_request', 'save'))
        time.sleep(1)
        self.assertTrue(path.exists(path.join(output_directory, state_save_file)), 'Saving generates a state file')
        self.assertTrue(path.getsize(path.join(output_directory, state_save_file)) > 0, 'Saving should populate file')

    def test_load(self):
        self.client.send(Message('json_request', 'save'))
        time.sleep(1)
        data = JSONController.load(output_directory)
        self.assertTrue(len(data) == 2, "Loading should've created two controllers")

        found = False
        for d in data:
            if d.name == 'test':
                found = True

        self.assertTrue(found, "TestQSM should've been loaded by the controller")

    def test_config_filename(self):
        self.client.send(Message('json_config', 'filename', '/tmp/robin_test_2/'))
        self.client.send(Message('json_request', 'save'))
        time.sleep(1)
        self.assertTrue(path.exists(path.join('/tmp/robin_test_2/', state_save_file)),
                        'Modifying filename, configures to save in new location')

    def test_config_count(self):
        self.client.send(Message('json_config', 'count', 2))
        second_uut = TestQSM('test2')
        second_uut.start()
        self.client.send(Message('json_request', 'save'))
        time.sleep(1)
        data = JSONController.load(output_directory)
        self.assertTrue(len(data) == 3,
                        "Modifying the count value should've generated three controllers, not {}".format(len(data)))


if __name__ == '__main__':
    # unittest.main()
    uut = TestQSM()
    uut.start()

    jcontr = JSONController('test_json', output_directory, 1)
    jcontr.start()

    client = MessageHandler('client')

    client.send(Message('json_request', 'save'))
    time.sleep(1)
    data = JSONController.load(output_directory)
    assert len(data) == 2

    found = False
    for d in data:
        if isinstance(d, TestQSM):
            found = True
    assert found
