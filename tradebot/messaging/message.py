import json
from multiprocessing import Process, Queue, Lock
from queue import Empty, Full


class Message:
    def __init__(self, title: str, msg: str = '', payload: object = None):
        self.title = title
        self.msg = msg
        self.payload = payload

    def __eq__(self, other):
        if isinstance(other, Message.__class__):
            return self.title == other.title
        elif isinstance(other, str):
            return self.title == other
        else:
            return False

    def __str__(self) -> str:
        return self.title + " " + self.msg + " " + str(self.payload)

    @staticmethod
    def from_str(data: str) -> object:
        title_end = data.find(' ')
        t = data[:title_end]
        data = data[title_end + 1:]

        msg_end = data.find(' ')
        msg = data[:msg_end]
        payld = data[msg_end + 1:]

        return Message(t, msg, json.loads(payld))


class AddressedMessage(Message):
    def __init__(self, target_id: str, title: str, msg: str = '', payload: object = None):
        super().__init__(title, msg, payload)
        self.target = target_id

    def __str__(self) -> str:
        return "To: {}".format(self.target) + ", " + self.title + " " + self.msg + " " + str(self.payload)

    @staticmethod
    def from_str(data: str) -> object:
        recipient_end = data.find(' ')
        r = data[:recipient_end]
        data = data[recipient_end + 1:]

        title_end = data.find(' ')
        t = data[:title_end]
        data = data[title_end + 1:]

        msg_end = data.find(' ')
        msg = data[:msg_end]
        payld = data[msg_end + 1:]

        return AddressedMessage(r, t, msg, json.loads(payld))


class MessageMailman(Process):
    def __init__(self, incoming: Queue = None):
        super().__init__()
        self.rx = incoming if incoming is not None else Queue()
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
                # print('Mailman received {}'.format(msg))
                if isinstance(msg, AddressedMessage.__class__):
                    if msg.target in self.slots.keys():
                        try:
                            self.slots[msg.target]['queue'].put_nowait(msg)
                        except Full as _:
                            print('{} is full, skipping'.format(msg.target))
                else:
                    for s in self.slots.keys():
                        # print('Checking {}\'s subscriptions list'.format(s))
                        if msg.title == 'all' or msg.title in self.slots[s]['subscriptions']:
                            try:
                                self.slots[s]['queue'].put_nowait(msg)
                                # print('Placed msg into {}\'s mailbox'.format(s))
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
                elif update.title == 'exit':
                    print('Mailman exiting')
                    break
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

    def receive(self, handler_id: str, block: bool = True) -> Message:
        self.receive_lock.acquire()
        self.update_q.put(Message('receive', handler_id, None))
        msg = self.tx.get()
        while block and msg is None:
            self.update_q.put(Message('receive', handler_id, None))
            msg = self.tx.get()
        self.receive_lock.release()
        return msg


class MessageHandler:

    mailman = None

    def __init__(self, handler_id: str, subscriptions: list = None):
        self.subs = subscriptions if subscriptions is not None else []
        self.handler_id = handler_id

        if MessageHandler.mailman is None:
            MessageHandler.mailman = MessageMailman()
            MessageHandler.mailman.start()

        MessageHandler.mailman.connect(self.handler_id, self.subs)

    def __del__(self):
        if MessageHandler.mailman is not None:
            MessageHandler.mailman.disconnect(self.handler_id)

    def send(self, msg: Message):
        MessageHandler.mailman.send(msg)

    def receive(self, block: bool = True) -> Message:
        m = MessageHandler.mailman.receive(self.handler_id, block=block)
        return m

    def join(self):
        self.send(Message('exit'))
        MessageHandler.mailman.update_q.put(Message('exit'))
        MessageHandler.mailman.join(timeout=10)
        MessageHandler.mailman = None


if __name__ == '__main__':
    print('Testing message class')

    msg = Message('something', 'something_else', {'name': 'name'})
    msg2 = Message('something', 'something_else', {'who': 'knows'})
    assert msg == msg2

    msg3 = Message.from_str('something something_else { "name" : "name" }')
    assert msg == msg3
    print("{}".format(msg))
    print('Testing messaging functionality')
    import time

    def test1_output(m: Message):
        print("This is test message 1")

    handler_1 = MessageHandler('handler 1', ['test1'])
    handler_2 = MessageHandler('handler 2')

    time.sleep(1)  # To account for asynchronousness
    handler_2.send(Message('test1'))

    print('waiting for test message')
    while handler_1.receive() is None:
        pass

    test1_output(None)

    handler_2.join()
