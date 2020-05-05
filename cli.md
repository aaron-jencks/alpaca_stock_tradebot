# Command Line Interface (CLI)

As of right now, there is no actual cli, but this language marks the framework for future works.

## Commands

### Overview

The commands listed below mark commands that can be piped into the running program, they consist of a series of space separated keywords and arguments.

You can either type in the optional arguments (arguments surrounded by `[]`) positionally, or by using their keyword by name in a `name=value` fashion.

Required values (those without `[]`) don't require their name, and are only accepted positionally.

You can use `;` to string multiple commands together, if using line returns is too much.

Whitespace of any kind, except line returns, obviously, is ignored.

### Commands

- `add acronym [shares=1] [buy_price=market]`: Adds the given stock with the given number of shares, to the stock vault. Returns a `unique_id` to be used in other commands.
- `remove id [shares=all]`: Removes a stock from the vault, removing a certain number of shares if specified, otherwise, removing all.
- `list [acronym]`: Lists all stocks currently managed, lists their current share count, along with the price they were bought at. If the optional argument `acronym` is supplied, then only stocks with that acronym are shown.
- `limit id limit_type`: Changes `id`'s managing limit to the given `limit_type`. See [stocks.txt](./README.md#Stocks_txt) for more info on how to format stock limits.
- `buy acronym [shares=1] [bid_price=market]`: Buys the given stock with the given number of shares, making a certain bid, or using market by default. Returns an `unique_id` just like `add`.
- `sell id [shares=all]`: Sells the number of shares from the given `id`
- `force-update`: Forces the [monitor](./tradebot/controllers/monitor.py) to update all prices for all stocks.
- `export`: Causes the program to save its current state, the default location is `~/.robintrader`, but this can be changed in [settings.py](./settings.py)
- `refresh`: Causes the program to ditch the current state and re-read everything in from the last saved state.
