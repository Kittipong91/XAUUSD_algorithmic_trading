import matplotlib.pyplot as plt


def plot_equity_trades(df,label,account_size) :
    df = df.copy()
    df['cum_res'] = df['PnL'].cumsum() + account_size

    plt.figure(figsize=(26, 10))
    plt.plot(df['ExitTime'],df['cum_res'], label= label)
    plt.legend()
    plt.title('Equity', fontsize=18)

    return