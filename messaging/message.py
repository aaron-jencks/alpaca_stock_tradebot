import json
from multiprocessing import Process, Queue, Lock
from queue import Empty, Full


class Message:
    def __init__(self, title: str, msg: str, payload: object):
        self.title = title
        self.msg = msg
        self.payload = payload

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.title == other.title

    def __str__(self) -> str:
        return self.title + " " + self.msg + " " + json.dumps(self.payload)

    @staticmethod
    def from_str(data: str) -> object:
        title_end = data.find(' ')
        t = data[:title_end]
        data = data[title_end + 1:]

        msg_end = data.find(' ')
        msg = data[:msg_end]
        payld = data[msg_end + 1:]

        return Message(t, msg, json.loads(payld))


class MessageMailman(Process):
    def __init__(self, incoming: Queue):
        super().__init__()
        self.rx = incoming
        self.tx = Queue()
        self.receive_lock = Lock()
        self.update_q = Queue()
        self.slots = {}

    def __del__(self):
        self.update_q.close()
        self.rx.close()
        self.tx.close()

    def run(self) -> None:
        while True:
            try:
                msg = self.rx.get_nowait()
                for s in self.slots.keys():
                    if msg in self.slots[s]['subscriptions']:
                        try:
                            self.slots[s]['queue'].put_nowait(msg)
                        except Full as _:
                            print('{} is full, skipping'.format(s))
            except Empty as _:
                pass

            try:
                update = self.update_q.get_nowait()
                if update.title == 'connect':
                    self.slots[update.msg] = {'subscriptions': update.payload, 'queue': Queue()}
                elif update.title == 'diconnect':
                    self.slots[update.msg]['queue'].close()
                    self.slots[update.msg] = {'subscriptions': [], 'queue': None}
                elif update.title == 'subscribe':
                    if update.msg not in self.slots.keys():
                        self.slots[update.msg] = {'subscriptions': [update.payload], 'queue': Queue()}
                    else:
                        self.slots[update.msg]['subscriptions'].append(update.payload)
                elif update.title == 'unsubscribe':
                    if update.msg in self.slots.keys():
                        if update.payload in self.slots[update.msg]['subscriptions']:
                            self.slots[update.msg]['subscriptions'].remove(update.payload)
                elif update.title == 'receive':
                    if update.msg in self.slots.keys():
                        try:
                            self.tx.put(self.slots[update.msg]['queue'].get_nowait())
                        except Empty as _:
                            self.tx.put(None)
            except Empty as _:
                pass

    def connect(self, handler_id: str, subscription_list: list):
        self.update_q.put(Message('connect', handler_id, subscription_list))

    def disconnect(self, handler_id: str):
        self.update_q.put(Message('disconnect', handler_id, None))

    def subscribe(self, handler_id: str, msg_id: str):
        self.update_q.put(Message('subscribe', handler_id, msg_id))

    def unsubscribe(self, handler_id, msg_id):
        self.update_q.put(Message('unsubscribe', handler_id, msg_id))

    def send(self, msg: Message):
        self.rx.put(msg)

    def receive(self, handler_id: str) -> Message:
        self.receive_lock.acquire()
        self.update_q.put(Message('receive', handler_id, None))
        msg = self.tx.get()
        self.receive_lock.release()
        return msg


class MessageHandler:
    def __init__(self, msg_mappings: dict):
        self.mappings = msg_mappings

    def handle_msg(self, msg: Message):
        if msg in self.mappings:
            self.mappings[msg](msg)


if __name__ == '__main__':
    print('Testing message class')
    msg = Message('something', 'something_else', {'name': 'name'})
    msg2 = Message('something', 'something_else', {'who': 'knows'})
    assert msg == msg2
    msg3 = Message.from_str('something something_else { "name" : "name" }')
    assert msg == msg3
    print("{}".format(msg))
