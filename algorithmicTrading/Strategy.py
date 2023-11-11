from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import numpy as np
import time
from MT5 import *


def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0


def moving_average_cross(symbol):
    df = MT5.get_data(symbol, 640, timeframe=mt5.TIMEFRAME_M5).dropna()
    df['MA_16'] = df.close.rolling(window=16).mean()
    df['MA_64'] = df.close.rolling(window=64).mean()
    df['DIFF'] = df.MA_16 - df.MA_64
    df['DIFF_PREV'] = df.DIFF.shift(1)
    df['IS_TRADE'] = df.apply(is_trade, axis=1)
    df_trades = df[df.IS_TRADE != 0].copy()
    today = df_trades['IS_TRADE'].iloc[-1]
    if today == 1:
        long = True
        sell = False
        return long, sell
    elif today == -1:
        long = False
        sell = True
        return long, sell
    else:
        long = False
        sell = False
        return long, sell


def trade_every_5_minute(symbol):
    df = MT5.get_data(symbol, 50, timeframe=mt5.TIMEFRAME_H4).dropna()
    df['ATR'] = ATR(df, 20)['ATR']
    TP = df['close'].iloc[-1] + df['ATR'].iloc[-1] * 0.5
    SL = df['open'].iloc[-1]
    print(type(TP),type(SL))
    sell = True
    long = False
    return long, sell , TP, SL


def ATR(df, n):
    df = df.copy()
    df['High-Low'] = abs(df['high'] - df['low'])
    df['High-PrevClose'] = abs(df['high'] - df['close'].shift(1))
    df['Low-PrevClose'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['High-Low', 'High-PrevClose',
                   'Low-PrevClose']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis=1)
    return df


def Momentum(symbol):

    df = MT5.get_data(symbol, 50, timeframe=mt5.TIMEFRAME_H4).dropna()

    df['ATR'] = ATR(df, 20)['ATR']
    df['direction'] = np.where(df['close'] > df['open'], 'bull', 'bear')
    df['dir_count'] = df.groupby(
        (df['direction'] != df['direction'].shift(1)).cumsum()).cumcount() + 1
    ATR_SL = 0.5
    # Buy
    print(symbol,df.dir_count.iloc[-1])
    if df['dir_count'].iloc[-1] >= 5 and df['direction'].iloc[-1] == 'bull':
        TP = df['close'].iloc[-1] + df['ATR'].iloc[-1] * ATR_SL,
        SL = df['open'].iloc[-1]
        return True, False, TP, SL
    # Sell
    elif df['dir_count'].iloc[-1] >= 5 and df['direction'].iloc[-1] == 'bear':
        TP = df['close'].iloc[-1] - df['ATR'].iloc[-1] * ATR_SL,
        SL = df['open'].iloc[-1]
        return False, True, TP, SL
    # Exit trades---------------------------------------------------------------------------
    # Buy profit

    else:
        long = False
        sell = False
        return long, sell, 0.01, 0.01
