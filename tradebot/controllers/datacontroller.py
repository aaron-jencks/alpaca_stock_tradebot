import os

from tradebot.objects.stockdescriptor import StockTransaction, StockUpdateDescriptor
from tradebot.messaging.qsm import QSM
from tradebot.messaging.message import Message


class DataController(QSM):
    def __init__(self, name: str, transaction_filename: str = './transactions.csv',
                 price_history_filename: str = './history.csv'):
        super().__init__(name, ['trade', 'monitor_update'])
        self.tfilename = transaction_filename
        self.pfilename = price_history_filename

    def export_transaction_data(self, t: StockTransaction):
        """Exports the data for the data collector to the given filename, you can override this method to
        change the file type, currently only csv is supported."""
        initialize = False
        if not os.path.exists(self.tfilename):
            initialize = True

        with open(self.tfilename, "a+") as fp:
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

        print('Saved the file {}'.format(self.tfilename))

    def export_price_data(self, t: StockUpdateDescriptor):
        """Exports the data for the data collector to the given filename, you can override this method to
        change the file type, currently only csv is supported."""
        initialize = False
        if not os.path.exists(self.tfilename):
            initialize = True

        with open(self.tfilename, "a+") as fp:
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

        print('Saved the file {}'.format(self.tfilename))

    def trade_msg(self, msg: Message):
        transaction = msg.payload
        self.export_transaction_data(transaction)

    def monitor_update_msg(self, msg: Message):
        stock = msg.payload
        self.export_price_data(stock)
