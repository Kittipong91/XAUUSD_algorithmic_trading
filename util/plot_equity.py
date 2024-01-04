import matplotlib.pyplot as plt


def plot_equity_trades(df, label, account_size):
    df = df.copy()
    plt.plot(df.index, df['Equity'], label=label)
    plt.legend()
    plt.title('Equity', fontsize=18)

    return
