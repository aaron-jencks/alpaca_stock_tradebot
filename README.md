# Python Robinhood AutoTrader

## Description
This project contains code for collecting automating the trading of stocks via the [Robinhood](https://robinhood.com/) website

## Contents
1. [Installation](#Installation)
2. [Module Breakdown](#Module-Breakdown)

# [Installation](#Installation)
To use the software all you have to do is run [main.py](./main.py).

## [Configuration](#Configuration)

To use the software, you obviously need to be able to login to Robinhood, which means that you need an account.
 The first time that you try to perform a transaction, the software will prompt you for your username, password.
 You can control which stocks you monitor by editing the configuration file [stocks.txt](./stocks.txt)
 
### [Development](#Development)

The entire source code is housed in the [tradebot](./tradebot) directory.

If you want to develope your own bot, then you'll probably need to know how the messaging system works. 
See the [messaging](./tradebot/messaging/) directory for more information

You can find `timer_relay.py` and `pyrh_adapter.py` in the [adapters](./tradebot/adapters) folder.

You can find all of the QSM modules in the [controllers](./tradebot/controllers) folder

You can find the descriptor objects and classes in the [objects](./tradebot/objects) folder

# [Module Breakdown](#Module-Breakdown)
The project architecture is broken down as follows [[source]](./architecture.puml):

![image](./Domain_Model_Diagram.png)
