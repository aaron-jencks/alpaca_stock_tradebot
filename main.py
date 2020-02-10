from multiprocessing import Queue, Pool
from queue import Empty, Full
from tqdm import tqdm
import time

from Timer import Timer
from DataController import DataController
from WebsiteController import WebsiteController
from stock_info_retriever import GoogleParser


if __name__ == "__main__":
    print("Generating parsers")
    parsers = [GoogleParser(input("Username for hyvee? "), input("Password: "))]

    print("Setting up controllers")
    tm = Timer(interval=180)  # 24*3600)
    dc = DataController(tm.Stop)
    wc = WebsiteController(parsers, tm.Stop)

    tm.start()
    dc.start()
    wc.start()
    print("Waiting for the controllers")
    while True:
        if not tm.Tx.empty():
            try:
                tm.Tx.get_nowait()
                try:
                    wc.Trigger.put_nowait(True)
                except Full as _:
                    print("Website controller is full, skipping...")
            except Empty as _:
                print("Timer magically became empty while retrieving it, skipping")

        new_data = False
        while not wc.Tx.empty():
            try:
                datum = wc.Tx.get_nowait()
                try:
                    dc.dataq.put_nowait(datum)
                except Full as _:
                    print("Data Controller is full, skipping")
                new_data = True
            except Empty as _:
                print("Website controller magically became empty while retrieving it, skipping")

        if new_data:
            dc.save()
            print("Saved data")

        time.sleep(5)
