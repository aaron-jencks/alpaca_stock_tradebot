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

## Contents
1. [Descriptors](#Descriptors)
2. [Timers](#Timers)
3. [DataMonitor](#DataMonitor)
4. [TradeController](#TradeController)
5. [DataController](#DataController)
6. [PYRHAdapter](#PYRHAdapter)
7. [Queued State Machines and Messaging](./tradebot/messaging)

### [Descriptors](#Descriptors)

This bot contains several descriptor classes used to represent `Stock` objects as they are represented in different aspects.

These classes are:

- [Stock](./tradebot/objects/stockdescriptor.py)
- [StockDescriptor](./tradebot/objects/stockdescriptor.py)
- [StockUpdateDescriptor](./tradebot/objects/stockdescriptor.py)
- [StockTransaction](./tradebot/objects/stockdescriptor.py)
- [LimitDescriptor](./tradebot/objects/limitdescriptor.py)

#### Stock Descriptors

There are 4 main Stock descriptors, the first is the main class, `Stock`, this class contains the acronym, asking price, and bidding price of the stock.
 Next is the `StockDescriptor` class, which represents a `Stock`, along with the number of shares. Then comes the `StockUpdateDescriptor`
 this is a `StockDescriptor` at a specific time, or day. And lastly there is the `StockTransaction` which is a transaction containing a `StockUpdateDescriptor` and a boolean indicating buying/selling.
 
 #### Limit Descriptors
 
 A `LimitDescriptor` indicates a buy/sell limit for a particular `Stock`, it contains two methods.
 
 `check_buy(sell_price: float, ask_price: float)` returns true if the stock should be bought.
 
 `check_sell(buy_price: float, bid_price: float)` returns true if the stock should be sold.
 
 ### [Timers](#Timers)
 
 There are 3 things you should be aware of when it comes to timers, these classes control how often the `StockMonitor` checks the prices of stocks,
  and can be used for other purposes as well, as you see fit.
  
 #### [Timer](./tradebot/controllers/timer.py)
 
 This is your average, everyday timer, it sends out a `Message` once every `interval` seconds.
 
 #### [MarketTimer](./tradebot/controllers/timer.py)
 
 This is an extension of the `Timer` class, it automatically pauses during aftermarket hours and on weekends.
 
 #### [TimerRelay](./tradebot/adapters/timer_relay.py)
 
 This baby is important, it allows you transform a `Timer` `Message` into a different `Message`. Quite handy.
 
 ### [DataMonitor](#DataMonitor)
 
 The `DataMonitor` is the `Process` that constantly monitors `Stock` prices and updates them, it also triggers the `TradeController` to either buy or sell stock.
 
 It sends out `monitor_update` messages containing `StockUpdateDescriptor` objects whenever it changes the price of a `Stock`.
 
 It sends out `trade_control` messages when it determines it is time to either buy or sell a `Stock`.
 
 ### [TradeController](#TradeController)
 
 The `TradeController` is the `Process` that controls exactly what you think it would. `StockTransactions`, `Message`s are sent to this controller and it determines if it's possible to buy or sell the stock, depending on the contents of the message.
 
 It sends out the `trade` message whenever it makes a trade, containing a `StockTransaction` within.
 
 ### [DataController](#DataController)
 
 The `DataController` is the `Process` that monitors and documents data changes, it intercepts `trade` and `monitor_update` messages, and places their entries into
 either the `transactions` file, or the `price_history` file, by default, these values are `transactions.csv` and `price_history.csv` respectively.
 
 ### [PYRHAdapter](#PYRHAdapter)
 
 The `PyrhAdapter` contains the interface for communicating with Robinhood, the `TradeController` and the `DataMonitor` both interface with this class directly.