import os.path as path
import os, json

from tradebot.messaging.message import Message
from tradebot.messaging.qsm import QSM
from settings import state_save_file


class JSONController(QSM):
    def __init__(self, name: str, output_filename: str, controller_count: int):
        super().__init__(name, ['json_config', 'json_update', 'json_request'])
        self.count = controller_count + 1  # it automatically counts itself
        self.buffer = []
        self.filename = output_filename

    def setup_states(self):
        super().setup_states()
        self.mappings['export'] = self.export
        self.mappings['begin save'] = self.save
        self.mappings['begin load'] = self.load

    def json_config_msg(self, msg: Message):
        if msg.msg == 'filename':
            self.filename = str(msg.payload)
            if not path.isdir(self.filename):
                print('Filename changes for output should take place in settings.py, truncating to directory')
                path.dirname(self.filename)
        elif msg.msg == 'count':
            self.count = msg.payload
            self.buffer.clear()
        elif msg.msg == 'flush':
            self.buffer.clear()

    def json_update_msg(self, msg: Message):
        """A JSON Update should include a dictionary of data to be saved for some controller"""
        self.buffer.append(msg.payload)
        if len(self.buffer) == self.count:
            self.append_state('export')

    def json_request_msg(self, msg: Message):
        if msg.msg == 'save':
            self.append_state('begin save')
        if msg.msg == 'load':
            self.append_state('begin load')

    def export(self):
        print('Saving state data')

        if not path.exists(self.filename):
            os.makedirs(self.filename, exist_ok=True)

        with open(path.join(self.filename, state_save_file), mode='w+') as fp:
            fp.write(json.dumps(self.buffer))

        self.buffer.clear()

    def save(self):
        self.buffer.clear()
        self.handler.send('all', 'save')
        self.buffer.append({
            'dtype': 'JSONController',
            'data': self.__dict__
        })

    @staticmethod
    def load(dirname: str):
        print('Loading state data')

        modules = []

        if not path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        with open(path.join(dirname, state_save_file), mode='w+') as fp:
            data = json.loads(fp.read())

        for d in data:
            dtype = d['dtype']
            method = eval(dtype + ".from_dict")
            modules.append(method(d['data']))
