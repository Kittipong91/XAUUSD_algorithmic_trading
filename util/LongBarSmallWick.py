import numpy as np


def average_bar_size(df):
    df = df.copy()
    df['candle_size'] = df['High'] - df['Low']
    df['average_bar'] = df['candle_size'].rolling(20).mean()
    return df


def small_wick(df, wick_size):
    df = df.copy()
    df['small_wick'] = np.where((df['Close'] > df['Open'])
                                & ((df['High'] - df['Close']) <= ((df['High'] - df['Low']) * wick_size))
                                & ((df['Open'] - df['Low']) <= ((df['High'] - df['Low']) * wick_size))
                                | (df['Close'] < df['Open'])
                                & ((df['High'] - df['Open']) <= ((df['High'] - df['Low']) * wick_size))
                                & ((df['Close'] - df['Low']) <= ((df['High'] - df['Low']) * wick_size)), True, False)
    return df
