import os.path as path
import os

from tradebot.objects.stockdescriptor import ManagedStock
from tradebot.objects.limitdescriptor import LimitDescriptor
import settings


def is_files_setup(directory: str) -> bool:
    """Returns true if the current files are all setup properly"""
    return path.exists(directory) and \
           path.exists(path.join(directory, settings.db_name)) and \
           path.exists(path.join(directory, settings.bank_balance_file)) and \
           path.exists(path.join(directory, settings.stock_transaction_file)) and \
           path.exists(path.join(directory, settings.stock_history_file)) and \
           path.exists(path.join(directory, settings.state_save_file)) and \
           path.exists(settings.tmp_dir)


def setup_files(directory: str):
    print('Setting up files')
    os.makedirs(directory, exist_ok=True)
    os.makedirs(settings.tmp_dir, exist_ok=True)
    print('Creating file placeholders')
    # db_fp = open(path.join(directory, settings.db_name), mode='w+')
    bal_fp = open(path.join(directory, settings.bank_balance_file), mode='w+')
    trans_fp = open(path.join(directory, settings.stock_transaction_file), mode='w+')
    hist_fp = open(path.join(directory, settings.stock_history_file), mode='w+')
    state_fp = open(path.join(directory, settings.state_save_file), mode='w+')
    fps = [bal_fp, trans_fp, hist_fp, state_fp]
    for fp in fps:
        fp.close()
    print('Files setup')


def parse_stock_descriptor(stock_descriptor: str) -> tuple:
    spaces = stock_descriptor.strip().count(' ')
    info = stock_descriptor.strip().split(' ')
    if spaces == 4:
        d = ManagedStock(info[0], shares=int(info[1]))
        l = LimitDescriptor(d.table_id, info[2], float(info[3]), float(info[4]))
    elif spaces == 3:
        d = ManagedStock(info[0], shares=int(info[1]))
        l = LimitDescriptor(d.table_id, '%', float(info[3]), float(info[2]))
    elif spaces == 1:
        d = ManagedStock(info[0], 0.95, 1.05, int(info[1]))
        l = LimitDescriptor(d.table_id, '%', 0.95, 1.05)
    else:
        print('Incorrect stocks.txt format')
        exit(1)
    return d, l


def read_stocks(filename: str) -> list:
    stocks = []

    with open(filename) as fp:
        lines = fp.readlines()
        for l in lines:
            stocks.append(parse_stock_descriptor(l))

    return stocks
