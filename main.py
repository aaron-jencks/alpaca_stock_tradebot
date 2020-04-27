from tradebot.controllers import *
from tradebot.adapters.timer_relay import TimerRelay
from tradebot.file_io import *
from tradebot.messaging.message import Message


if __name__ == '__main__':
    print('Reading in stock info')
    stocks = read_stocks('./stocks.txt')

    print('Configuring limit info')
    limit_dict = {}
    for s in stocks:
        limit_dict[s[0].acronym] = s[1]

    print('Creating modules')
    t = timer.Timer('update_trigger', interval=3600)
    relay = TimerRelay('timer_relay', Message('monitor_config', 'update'))
    dm = monitor.StockMonitor('monitor', [t[0] for t in stocks], limit_dict)
    dc = datacontroller.DataController('data_controller')
    tc = tradecontroller.TradeController('trade_controller')

    print('Starting modules')
    relay.start()
    dm.start()
    dc.start()
    tc.start()
    t.start()

    print('Waiting for timer to finish')
    t.join()
