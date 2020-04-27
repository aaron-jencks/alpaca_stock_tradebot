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
 
### [Stocks.txt](#Stocks_txt)

The format of [stocks.txt](./stocks.txt) is as follows

```
acronym shares [[type] upper_sell lower_buy]
```

Where:
- *acronym* is the acronym of the stock
- *shares* is the number of shares you'd like to have managed
- *upper_sell lower_buy* are the points, in percentage, that you'd like to auto-trade your stocks. By default this is +/- 5%
    - *type* is the type of auto-trade you'd like to do, by default this is `%`:
        - `$` specifies a hard set limit to sell and buy at, that is the exact price to buy and sell is stated.
        - `%` specifies a percentage limit to sell and buy at, that is when the price goes above a set percentage, it is sold, and when it goes below one, it is bought.
        - `#` specifies a dollar difference, when the price goes a certain dollar amount above, or below, it is bought, or sold
    
    For example:
    ```
    AAPL 10 % 1.10 0.95
    ```
    will manage 10 shares of Apple and auto sell when the current bid price is 10% above the current price, and auto buy when the ask price falls back down to 95% of what it is now.
    
    Or for another example:
    
    ```
    AAPL 10 # 1.10 0.95
    ```
    
    Means that 10 shares of Apple will be sold when the bid price goes up by $1.10, and bought when the ask price goes below by $0.95.
    
    And finally, one last example:
    ```
    AAPL 10 $ 1.10 0.95
    ```
  
    Means that you have 10 shares of Apple and you'd like to sell them once they go over $1.10 and buy when they go below $0.95.
    
    The `lower_buy` needs to be less than `upper_sell`.
    
    You can also specify specific dollar amounts to trade at by placing a `$` before the number.
    
    
 
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
