from tradebot.objects.stockdescriptor import StockDescriptor
from tradebot.objects.limitdescriptor import LimitDescriptor


def parse_stock_descriptor(stock_descriptor: str) -> tuple:
    spaces = stock_descriptor.strip().count(' ')
    info = stock_descriptor.strip().split(' ')
    if spaces == 4:
        d = StockDescriptor(info[0], float(info[4]), float(info[3]), int(info[1]))
        l = LimitDescriptor(info[2], float(info[4]), float(info[3]))
    elif spaces == 3:
        d = StockDescriptor(info[0], float(info[3]), float(info[2]), int(info[1]))
        l = LimitDescriptor('%', float(info[3]), float(info[2]))
    elif spaces == 1:
        d = StockDescriptor(info[0], 0.95, 1.05, int(info[1]))
        l = LimitDescriptor('%', 0.95, 1.05)
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
