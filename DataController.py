from multiprocessing import Process, Queue
from queue import Empty, Full
import os
import time

import pandas as pd
import numpy as np

from WebsiteDescriptor import WebsiteDescriptor


class DataController(Process):
    """Represents the data controller for the project, handles the data model and importing and exporting to file.
    See the README for information on the column names and data layout."""

    def __init__(self, stopq: Queue = None, dataq: Queue = None, filename: str = './data.csv'):
        super().__init__()
        self.Stop = Queue() if stopq is None else stopq
        self.dataq = Queue() if dataq is None else dataq
        self.filename = filename

        self.__data = []
        self.__saveq = Queue()

    def export_data(self):
        """Exports the data for the data collector to the given filename, you can override this method to
        change the file type, currently only csv is supported."""
        initialize = False
        if not os.path.exists(self.filename):
            initialize = True

        with open(self.filename, "a+") as fp:
            rows = []

            # Writes the header row if the file is new
            if initialize:
                row = ''
                for h in WebsiteDescriptor.get_headers():
                    row += h.replace('"', '""') + ','
                rows.append(row[:-1] + '\n')

            # Writes the data to the file line, by line
            for d in self.__data:
                row = ''
                for i in d:
                    if type(i) == str:
                        i = i.replace('"', '""')

                    row += str(i) + ','
                rows.append(row[:-1] + '\n')

            fp.writelines(rows)

        self.__data = []  # Clear the data buffer
        print('Saved the file {}'.format(self.filename))

    def append_data(self, datum: WebsiteDescriptor):
        if datum.name != '':
            print("Appending {}".format(datum))
            self.__data.append(datum.to_array())
        else:
            print("Found erroneous data, skipping")

    def run(self) -> None:
        while self.Stop.empty():
            while not self.dataq.empty():
                # Read in the new data to be appended
                try:
                    self.append_data(self.dataq.get_nowait())
                except Empty as _:
                    print("Data queue was empty when trying to append new data, what a shame.")

            if not self.__saveq.empty():
                # Save the file
                while not self.__saveq.empty():
                    try:
                        self.filename = self.__saveq.get_nowait()
                    except Empty as _:
                        # print("Saving queue was empty when trying to save the data, what a shame.")
                        break

                self.export_data()

            time.sleep(5)

        while not self.dataq.empty():
            # Read in the new data to be appended
            try:
                self.append_data(self.dataq.get_nowait())
            except Empty as _:
                print("Data queue was empty when trying to append new data, what a shame.")
                break

        if not self.__saveq.empty():
            # Save the file
            while not self.__saveq.empty():
                try:
                    self.filename = self.__saveq.get_nowait()
                except Empty as _:
                    # print("Saving queue was empty when trying to save the data, what a shame.")
                    break

            self.export_data()

        print("Stopping the data controller")
        self.Stop.close()
        self.dataq.close()
        self.__saveq.close()

    def save(self, filename: str = ''):
        """Tells the data controller to save it's data"""
        if filename == '':
            filename = self.filename
        else:
            self.filename = filename

        self.__saveq.put(filename)


if __name__ == "__main__":
    from WebsiteDescriptor import *

    dc = DataController()
    dc.start()

    print("Appending data")
    dc.dataq.put(WebsiteDescriptor(Website('BP', 'BP', 'something', 32985734, 9348579348520, 2.30, 5, 500),
                                   OilWebsite(50)))

    print("Saving data")
    dc.save()

    dc.Stop.put(True)
