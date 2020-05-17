from tradebot.controllers import *
from tradebot.adapters.timer_relay import TimerRelay
from tradebot.adapters.pyrh_adapter import PyrhAdapter
from tradebot.file_io import *
from tradebot.messaging.message import Message, MessageHandler
from tradebot.controllers.cli import parse_command
from tradebot.objects.stockdescriptor import Stock
from tradebot.controllers.stock_vault import StockVault


if __name__ == '__main__':
    print('Welcome to iggy\'s Robinhood Trading bot')

    v = StockVault()

    # p = PyrhAdapter()
    # p.login()
    #
    # dm = monitor.StockMonitor('monitor', [Stock(t[0].acronym) for t in stocks], limit_dict, p)
    # # dc = datacontroller.DataController('data_controller')
    # tc = tradecontroller.TradeController('trade_controller', 0)
    #
    print('Starting modules')
    # relay.start()
    # p.start()
    # dm.start()
    # # dc.start()
    # tc.start()
    # t.start()
    v.start()

    print('Type HELP for a list of usable commands, otherwise, please see the wiki.')
    while True:
        st = input('Enter a command $ ')
        if st == 'exit':
            # t.join()
            # # dc.join()
            # tc.join()
            # p.join()
            # relay.join()
            v.sjoin()
            break
        else:
            parse_command(st)
