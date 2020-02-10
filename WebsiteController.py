from multiprocessing import Process, Queue, Pool
from queue import Empty, Full
import time

from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from WebsiteParser import WebsiteParser
from WebsiteDescriptor import WebsiteDescriptor

from robinhood_api import login


def __parse__(p: WebsiteParser) -> WebsiteDescriptor:
    return p.parse()


class WebsiteController(Process):
    """Controls the website parsing, contains several queues for communication:
    Stop: placing anything in here stops the process
    Tx: Data transmission queue, once the data has been collected, it will be placed in here for collection
    Trigger: Placing anything in here will cause the controller to parse it's websites and collect data
    """

    browser = None
    logged_in = False

    def __init__(self, parsers: list, username: str, password: str, stopq: Queue = None, tx: Queue = None, trigger: Queue = None):
        super().__init__()
        self.parsers = parsers

        self.Stop = Queue() if stopq is None else stopq
        self.Tx = Queue() if tx is None else tx
        self.Trigger = Queue() if trigger is None else trigger
        self.pool = Pool()

        self.username = username
        self.password = password

        if WebsiteController.browser is None:
            foptions = Options()
            foptions.headless = False  # True
            WebsiteController.browser = webdriver.Firefox(options=foptions)

    def __del__(self):
        self.pool.close()

        if self.browser:
            WebsiteController.browser.close()
            WebsiteController.browser = None

    def poll_websites(self):
        """Goes around to each website under its control and calls the 'parse()' method on it."""
        # try:
        #     parsings = list(self.pool.map(__parse__, self.parsers))
        #     return parsings
        # except Exception as e:
        #     print(e)

        if not self.logged_in:
            login(self.browser, self.username, self.password)
            self.logged_in = True

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
