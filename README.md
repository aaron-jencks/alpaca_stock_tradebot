# Python Robinhood AutoTrader

## Description
This project contains code for collecting automating the trading of stocks via the [Robinhood](https://robinhood.com/) website

## Contents
1. [Installation](#Installation)
2. [Module Breakdown](#Module-Breakdown)

# [Installation](#Installation)
To use the software all you have to do is run [main.py](./main.py).

## [Configuration](#Configuration)

To use your account the program needs your login credentials, these credentials can be entered into [login.py](./login.py)

To configure the websites that it uses modify the list inside of [defs.py](./defs.py)
To configure the stocks that you'd like to make available for trade, add them to the list inside of [defs.py](./defs.py)
To configure the algorithms that the bot uses to determine when to buy and sell stock, you can adjust the settings inside of [data_monitor.py](./data_monitor.py)

To define your own parsers, see the [WebsiteParser.py](./WebsiteParser.py) file.

More coming soon

# [Module Breakdown](#Module-Breakdown)
The project architecture is broken down as follows [[source]](./architecture.puml):

![image](./Domain_Model_Diagram.png)
