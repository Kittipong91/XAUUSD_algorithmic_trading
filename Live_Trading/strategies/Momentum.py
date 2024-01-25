import MetaTrader5 as mt5
import numpy as np
import time
from MT5 import *


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


def momentum(symbol):

    df = MT5.get_data(symbol, 50, timeframe=mt5.TIMEFRAME_H4).dropna()

    df['ATR'] = ATR(df, 20)['ATR']
    df['direction'] = np.where(df['close'] > df['open'], 'bull', 'bear')
    df['dir_count'] = df.groupby(
        (df['direction'] != df['direction'].shift(1)).cumsum()).cumcount() + 1
    ATR_SL = 6
    # Buy
    print(symbol,df.dir_count.iloc[-2])
    if df['dir_count'].iloc[-2] >= 2 and df['direction'].iloc[-2] == 'bull':
        dif_TP = df['ATR'].iloc[-1] * ATR_SL
        dif_SL = abs(df['open'].iloc[-2] - df['close'].iloc[-2])
        return True, False, dif_TP, dif_SL
    # Sell
    elif df['dir_count'].iloc[-2] >= 2 and df['direction'].iloc[-2] == 'bear':
        dif_TP = df['ATR'].iloc[-1] * ATR_SL
        dif_SL = abs(df['open'].iloc[-2] - df['close'].iloc[-2])
        return False, True, dif_TP, dif_SL
    # Exit trades---------------------------------------------------------------------------
    # Buy profit

    else:
        long = False
        sell = False
        return long, sell , None , None


symbols_list = {
    "Gold - US Dollar": ["XAUUSDm", 0.01],
}
magic = 24001
strategy = 'Momentum'

def check_time() :
    current_time = time.strftime("%H:%M:%S")
    # print(current_time, 'waiting......')

def run_momentum():
    while True:
        df = MT5.get_data("XAUUSDm", 2, timeframe=mt5.TIMEFRAME_H4).dropna()
        time_curent = df.index[-1]
        while True :
            df = MT5.get_data("XAUUSDm", 2, timeframe=mt5.TIMEFRAME_H4).dropna()
            if time_curent == df.index[-2] :
                break
            check_time()
            time.sleep(60)
        # Get the current time in HH:MM:SS format
        check_time()
        # Perform trading logic at 5-minute intervals
        for asset in symbols_list.keys():
            symbol = symbols_list[asset][0]
            lot = symbols_list[asset][1]
            buy, sell, dif_tp, dif_sl = momentum(symbol)
            if buy or sell:
                MT5.run(symbol, buy, sell, lot, dif_tp, dif_sl,magic,strategy)

        time.sleep(60)
