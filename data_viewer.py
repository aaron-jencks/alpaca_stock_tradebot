import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import time


matplotlib.use('Tkagg')


fig = plt.figure()
axs = []


def read_data(filename: str = './history.csv'):
    global axs, fig

    df = pd.read_csv(filename)
    acronyms = list(set(df['Name']))
    if len(acronyms) > len(axs):
        diff = len(acronyms) - len(axs)
        for i in range(diff):
            ask = fig.add_subplot(len(acronyms), 2, 2 * len(axs) + 1)
            bid = fig.add_subplot(len(acronyms), 2, 2 * len(axs) + 2)
            axs.append((ask, bid))

    return df


def plot_file(filename: str = './history.csv'):
    global fig, axs

    df = read_data(filename)
    # print(df.head())
    df['Seconds_Epoch'] = df['Second'] + (df['Minute'] * 60) + ((df['Hour'] - 9) * 3600) + (df['Day'] * 25200) + (df['Year'] * 9198000)

    acronyms = list(set(df['Name']))

    for i, row in enumerate(axs):
        acronym = acronyms[i]
        ask, bid = row
        df_row = df[df['Name'] == acronym]
        a_sma = df_row['Ask_Price'].rolling(window=20).mean()
        b_sma = df_row['Ask_Price'].rolling(window=20).mean()

        seconds = df_row['Seconds_Epoch'].array
        seconds = sorted(seconds)
        # print(seconds[-15:])

        ask.cla()
        bid.cla()
        ask.scatter(df_row['Seconds_Epoch'], df_row['Ask_Price'], 1)
        ask.plot(df_row['Seconds_Epoch'], a_sma, color='magenta', linewidth=1)
        ask.axes.get_xaxis().set_ticks([])
        bid.scatter(df_row['Seconds_Epoch'], df_row['Bid_Price'], 1)
        bid.plot(df_row['Seconds_Epoch'], b_sma, color='magenta', linewidth=1)
        bid.axes.get_xaxis().set_ticks([])

    for i, a in enumerate(acronyms):
        fig.text(0.05, 1 - (i/(len(acronyms) + 1)) - 1/(2*(len(acronyms) + 1)) - 0.1, a)

    fig.text(0.3, 0.95, 'Ask Price')
    fig.text(0.67, 0.95, 'Bid Price')
    fig.suptitle('Stock Prices Over Time')

    fig.canvas.draw()
    plt.pause(1)


if __name__ == '__main__':
    while True:
        plot_file()
        time.sleep(60)
