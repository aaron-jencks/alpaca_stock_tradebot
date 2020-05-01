from multiprocessing import Process, Pipe, Lock
from multiprocessing.connection import Connection
from typing import Optional


class ConsoleJunction(Process):
    def __init__(self, incoming: Connection):
        super().__init__()
        self.connections = {}
        self.incoming = incoming
        i, o = Pipe(True)
        self.requests = i
        self.__requests = o
        self.req_lock = Lock()
        self.is_stopping = False

    def run(self) -> None:
        while not self.is_stopping:
            while self.incoming.poll():
                msg = self.incoming.recv()
                for c in self.connections.values():
                    c.send(msg)

            while self.__requests.poll():
                cmd = self.__requests.recv()
                if cmd['msg'] == 'connect':
                    i, o = Pipe()
                    self.connections[cmd['payload']] = i
                    self.__requests.send(o)
                elif cmd['msg'] == 'disconnect':
                    if cmd['payload'] in self.connections:
                        self.connections[cmd['payload']].close()
                elif cmd['msg'] == 'exit':
                    self.is_stopping = True
                    print('Console Junction is exitting')

    def connect(self, client_id: str) -> Connection:
        self.req_lock.acquire()
        self.requests.send({'msg': 'connect', 'payload': client_id})
        while not self.requests.poll(5):
            pass
        out = self.requests.recv()
        self.req_lock.release()
        return out

    def disconnect(self, client_id):
        self.requests.send({'msg': 'disconnect', 'payload': client_id})

    def join(self, timeout: Optional[float] = None) -> None:
        self.requests.send({'msg': 'exit'})
        super().join()


class ConsoleServer:

    junction = None
    outgoing = None

    def __init__(self):
        if ConsoleServer.junction is None:
            ConsoleServer.setup_junction()

    @staticmethod
    def setup_junction():
        i, o = Pipe()
        ConsoleServer.outgoing = i
        ConsoleServer.junction = ConsoleJunction(o)
        ConsoleServer.junction.start()

    @staticmethod
    def connect(client_id: str) -> Connection:
        if ConsoleServer.junction is None:
            ConsoleServer.setup_junction()
        return ConsoleServer.junction.connect(client_id)

    @staticmethod
    def disconnect(client_id: str):
        if ConsoleServer.junction is None:
            ConsoleServer.setup_junction()
        ConsoleServer.junction.disconnect(client_id)

    @staticmethod
    def send(msg: str):
        if ConsoleServer.junction is None:
            ConsoleServer.setup_junction()
        ConsoleServer.outgoing.send(msg)

    @staticmethod
    def join():
        if ConsoleServer.junction is not None:
            ConsoleServer.junction.join()
            ConsoleServer.outgoing.close()


class ConsoleClient:
    def __init__(self, client_id: str):
        self.incoming = ConsoleServer.connect(client_id)
        self.client_id = client_id

    def readline(self) -> str:
        self.incoming.poll(None)
        return self.incoming.recv()

    def close(self):
        ConsoleServer.disconnect(self.client_id)
        self.incoming.close()


if __name__ == '__main__':
    import sys


    class TestProcess(Process):
        def __init__(self, name: str):
            super().__init__()
            self.client = ConsoleClient(name)

        def run(self) -> None:
            sys.stdin = self.client
            while True:
                print(input('Please type something'))


    c = TestProcess('test1')
    c.start()

    while True:
        ConsoleServer.send(input())
