
username = 'Your Username/Email Here'
password = 'Your Password here'
challenge_type = 'sms'

# This is the section for file configuration

tmp_dir = '/tmp/.robin_trader'                  # This is where cookies, like authentication tokens will be stored
file_location = '/home/aaron/.robin_trader'               # This is where all of the files for this program will reside.
db_name = 'stocks.db'                           # This is where all of the currently handled stocks will be placed
state_save_file = 'state.json'                  # Whenever the program saves its state, this is where it'll be put
stock_history_file = 'history.csv'              # Whenever a stock changes price, this will be appended to
stock_transaction_file = 'transactions.csv'     # Whenever a stock is bought or sold, this will be appended to
bank_balance_file = 'balance.csv'               # Whenever the bank balance changes, this will be appended to
