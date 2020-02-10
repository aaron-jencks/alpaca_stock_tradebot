from multiprocessing import Process, Queue
import time
from queue import Full, Empty


class Timer(Process):
    """Represents an asynchronous timer, it can be configured by setting the interval, once the interval is set,
    then the timer will proceed to send out a queue item in it's Tx property once every "interval" seconds.
    The default interval is 1 second."""

    def __init__(self, stopq: Queue = None, txq: Queue = None, name: str = '', interval: int = 1):
        super().__init__()
        self.interval = interval
        self.name = name

        self.Tx = Queue() if txq is None else txq
        self.Rx = Queue()
        self.Stop = Queue() if stopq is None else stopq

    def run(self) -> None:
        try:
            self.Tx.put_nowait(self.name)
            print("Timer triggered")
        except Full as _:
            print("Timer output queue is full, skipping.")
            
        start = time.time()
        
        while self.Stop.empty():
            diff = time.time() - start

            if diff >= self.interval:
                try:
                    self.Tx.put_nowait(self.name)
                    print("Timer triggered")
                except Full as _:
                    print("Timer output queue is full, skipping.")

                start = time.time()

            if not self.Rx.empty():
                try:
                    self.interval = self.Rx.get_nowait()
                except Empty as _:
                    print("Swing and a miss at collecting a new timer interval")

            time.sleep(self.interval)

        print("Stopping timer")
        self.Tx.close()
        self.Rx.close()
        self.Stop.close()


if __name__ == "__main__":
    t = Timer()
    t.start()

    while True:
        if not t.Tx.empty():
            print("Timer notification")
            try:
                t.Tx.get_nowait()
            except Empty as _:
                print("Tried to collect timer notification, but the queue was empty, skipping")
