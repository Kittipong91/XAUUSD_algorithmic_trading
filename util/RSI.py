import numpy as np


def rsi(df, n):
    df['diff'] = df['Close'].diff(1).dropna()
    df['gains'] = np.where(df['diff'] > 0, df['diff'], np.nan)
    df['losses'] = np.where(df['diff'] <= 0, df['diff'], np.nan)
    df['average_gains'] = df['gains'].rolling(n, min_periods=1).mean()
    df['average_losses'] = df['losses'].rolling(n, min_periods=1).mean()
    rs = abs(df['average_gains'] / df['average_losses'])
    df['RSI'] = 100 - (100 / (1 + rs))
    df = df.drop(['diff', 'gains', 'losses','average_gains', 'average_losses'], axis=1)

    return df
