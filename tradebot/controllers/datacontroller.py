import os

from tradebot.objects.stockdescriptor import StockTransaction
from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class DataController(QSM):
    def __init__(self, name: str, filename: str = './data.csv'):
        super().__init__(name, ['trade'])
        self.filename = filename

    def export_data(self, t: StockTransaction):
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
                for h in StockTransaction.get_headers():
                    row += h.replace('"', '""') + ','
                rows.append(row[:-1] + '\n')

            # Writes the data to the file line, by line
            row = ''
            for i in t.to_array():
                if type(i) == str:
                    i = i.replace('"', '""')

                row += str(i) + ','
            rows.append(row[:-1] + '\n')

            fp.writelines(rows)

        print('Saved the file {}'.format(self.filename))

    def trade_msg(self, msg: Message):
        transaction = msg.payload
        self.export_data(transaction)
