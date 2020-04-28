from multiprocessing import Process, Queue
from queue import Full, Empty
from io import TextIOBase
import socket
import selectors


class SocketConsoleClient(TextIOBase):
    def __init__(self, port: int):
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((socket.gethostbyname('localhost'), self.port))
        self.selector = selectors.DefaultSelector()
        self.conn.setblocking(False)
        self.selector.register(self.conn, selectors.EVENT_WRITE, data='hello')

    def readline(self, size: int = ...) -> str:
        while True:
            for k, _ in self.selector.select(timeout=None):
                if k.data == 'hello':
                    try:
                        return str(self.conn.recv(1024).decode('latin1'))
                    except Exception as e:
                        # print(e)
                        continue


class SocketConsoleWriter(Process):
    def __init__(self):
        super().__init__()
        self.writes = Queue()
        self.connections = []
        self.listener = None
        self.selector = None

        self.port = 10000

    def run(self) -> None:
        while True:
            try:
                self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.listener.bind((socket.gethostbyname('localhost'), self.port))
                self.listener.listen()
                print('listening on', ('localhost', self.port))
                self.listener.setblocking(False)
                break
            except Exception as _:
                self.port += 1  # if errno is 98, then port is not available.

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.listener, selectors.EVENT_READ, data='test')

        while True:
            try:
                w = self.writes.get_nowait()
                if w == '$$$EXIT!!!':
                    break
                else:
                    for c in self.connections:
                        c.send(w.encode('latin1'))
            except Empty:
                pass

            try:
                d = self.selector.select(1)
                for k, _ in d:
                    if k.data == 'test':
                        conn, addr = self.listener.accept()
                        print('{} connected'.format(addr))
                        self.connections.append(conn)
            except Exception as e:
                # print(e)
                pass


class SocketConsoleServer:

    server = None

    def __init__(self):
        if SocketConsoleServer.server is None:
            SocketConsoleServer.server = SocketConsoleWriter()
            SocketConsoleServer.server.start()

    @staticmethod
    def port() -> int:
        if SocketConsoleServer.server is None:
            SocketConsoleServer.server = SocketConsoleWriter()
            SocketConsoleServer.server.start()

        return SocketConsoleServer.server.port

    @staticmethod
    def write(msg: str):
        if SocketConsoleServer.server is None:
            SocketConsoleServer.server = SocketConsoleWriter()
            SocketConsoleServer.server.start()

        SocketConsoleServer.server.writes.put(msg)


if __name__ == '__main__':
    import sys, time

    serv = SocketConsoleServer()
    time.sleep(1)

    class TestProcessSocket(Process):
        def run(self):
            sys.stdin = SocketConsoleClient(serv.port())
            time.sleep(1)
            print(input())

    client = TestProcessSocket()
    client.start()

    serv.write(input('Type something: ') + '\n')
    client.join()
