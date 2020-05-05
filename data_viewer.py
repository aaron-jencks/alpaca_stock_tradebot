import matplotlib.pyplot as plt
import pandas as pd
import time


fig = plt.Figure()
axs = []


def read_data(filename: str = './history.csv'):
    global axs, fig

    df = pd.read_csv(filename)
    acronyms = list(set(df['Name']))
    if len(acronyms) > len(axs):
        diff = len(acronyms) - len(axs)
        for i in range(diff):
            ask = fig.add_subplot(len(axs) + 1, 2, len(axs) + 1)
            bid = fig.add_subplot(len(axs) + 1, 2, len(axs) + 2)
            axs.append((ask, bid))

    return df


def plot_file(filename: str = './history.csv'):
    global fig, axs

    df = read_data(filename)
    # print(df.head())
    df['Seconds_Epoch'] = df['Second'] + (df['Minute'] * 60) + (df['Hour'] * 3600) + \
                          (df['Day'] * 23400) + (df['Year'] * 6100715)

    acronyms = list(set(df['Name']))

    # fig, axs = plt.subplots(len(acronyms), 2, sharey='row')
    for i, row in enumerate(axs):
        acronym = acronyms[i]
        ask, bid = row
        df_row = df[df['Name'] == acronym]
        ask.cla()
        bid.cla()
        ask.scatter(df_row['Seconds_Epoch'], df_row['Ask_Price'])
        bid.scatter(df_row['Seconds_Epoch'], df_row['Bid_Price'])

    for i, a in enumerate(acronyms):
        fig.text(0.05, 1 - (i/(len(acronyms) + 1)) - 1/(2*(len(acronyms) + 1)) - 0.1, a)

    fig.canvas.draw()
    plt.pause(1)


if __name__ == '__main__':
    while True:
        plot_file()
        time.sleep(10)
