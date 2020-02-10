from multiprocessing import Process, Queue, Pool
from queue import Empty, Full
import time

from tqdm import tqdm

from WebsiteParser import WebsiteParser
from WebsiteDescriptor import WebsiteDescriptor


def __parse__(p: WebsiteParser) -> WebsiteDescriptor:
    return p.parse()


class WebsiteController(Process):
    """Controls the website parsing, contains several queues for communication:
    Stop: placing anything in here stops the process
    Tx: Data transmission queue, once the data has been collected, it will be placed in here for collection
    Trigger: Placing anything in here will cause the controller to parse it's websites and collect data
    """

    def __init__(self, parsers: list, stopq: Queue = None, tx: Queue = None, trigger: Queue = None):
        super().__init__()
        self.parsers = parsers

        self.Stop = Queue() if stopq is None else stopq
        self.Tx = Queue() if tx is None else tx
        self.Trigger = Queue() if trigger is None else trigger
        self.pool = Pool()

    def __del__(self):
        self.pool.close()

    def poll_websites(self):
        """Goes around to each website under its control and calls the 'parse()' method on it."""
        # try:
        #     parsings = list(self.pool.map(__parse__, self.parsers))
        #     return parsings
        # except Exception as e:
        #     print(e)
        for p in self.parsers:
            for r in p.parse():
                try:
                    self.Tx.put_nowait(r)
                except Full as _:
                    print("Ran out of space in the parser queue, skipping\n{}".format(str(r)))

    def run(self) -> None:
        while self.Stop.empty():
            while not self.Trigger.empty():
                # Trigger and poll the websites
                try:
                    self.Trigger.get_nowait()
                    print("Website Controller triggered.")
                    self.poll_websites()
                    print("Website Controller finished triggering")
                except Empty as _:
                    print("Trigger queue was empty when trying to read from it, what a shame.")

            time.sleep(5)

        while not self.Trigger.empty():
            # Trigger and poll the websites
            try:
                self.Trigger.get_nowait()
                print("Website Controller triggered.")
                self.poll_websites()
                print("Website Controller finished triggering")
            except Empty as _:
                print("Trigger queue was empty when trying to read from it, what a shame.")


if __name__ == "__main__":
    wc = WebsiteController([WebsiteParser(), WebsiteParser()])
    wc.start()

    print("Testing website controller")
    wc.Trigger.put_nowait("woah")

    wc.Stop.put(True)

    wc.join()
