# Python Robinhood AutoTrader

## Description
This project contains code for collecting automating the trading of stocks via the [Robinhood](https://robinhood.com/) website

For information on how to get started, install, or configure, see the [wiki](./wiki)
 
### [Development](#Development)

The entire source code is housed in the [tradebot](./tradebot) directory.

If you want to develope your own bot, then you'll probably need to know how the messaging system works. 
See the [messaging](./wiki/messages) page for more information

You can find `timer_relay.py` and `pyrh_adapter.py` in the [adapters](./tradebot/adapters) folder.

You can find all of the QSM modules in the [controllers](./tradebot/controllers) folder

You can find the descriptor objects and classes in the [objects](./tradebot/objects) folder