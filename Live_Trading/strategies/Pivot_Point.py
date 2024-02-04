import MetaTrader5 as mt5
import numpy as np
import time
from MT5 import *


def PrepareData(data):
    agg_dict = {"open": "first",
                "high": "max",
                "low": "min",
                "close": "last"
                }
    daily_data = data.resample("D", offset="16H").agg(agg_dict).dropna()
    daily_data.columns = ["Open_d", "High_d", "Low_d", "Close_d"]
    data = pd.concat([data, daily_data.shift().dropna()],
                     axis=1).ffill().dropna()
    return data



def Pivot_Point(symbol):

    periods = 14
    moving_av = 3

    # get data from mt5
    df = MT5.get_data(symbol, 50, timeframe=mt5.TIMEFRAME_H4).dropna()
    # print(df)
    # prepare data
    df = PrepareData(df)

    # conditional
    df["PP"] = (
    df["High_d"] + df["Low_d"] + df["Close_d"]) / 3
    df["S1"] = df["PP"] * 2 - df["High_d"]
    df["S2"] = df["PP"] - (df["PP"] - df["PP"])
    df["R1"] = df["PP"] * 2 - df["Low_d"]
    df["R2"] = df["PP"] + (df["High_d"] - df["Low_d"])
    df["position"] = np.where(df["open"] > df["PP"], 1, -1)
    df["position"] = np.where(
    df["open"] >= df["R1"], 0, df["position"])
    df["position"] = np.where(df["open"] <= df["S1"], 0, df["position"])
    # print(df)

    # get signal
    position = df.position.iloc[-2]
    print('signal :' , position )
    # Buy
    if position == 1:
        
        return True, False, None, None
    # Sell
    elif position == 0:
        
        return False, True, None, None
    # Exit trades---------------------------------------------------------------------------
    # Buy profit

    else:
        long = False
        sell = False
        return long, sell, None, None


symbols_list = {
    "Gold - US Dollar": ["XAUUSDm", 0.01],
}
magic = 24002
strategy = 'Pivot Point'


def check_time():
    current_time = time.strftime("%H:%M:%S")
    # print(current_time, 'waiting......')


def run_Pivot_Point():
    while True:
        df = MT5.get_data("XAUUSDm", 2, timeframe=mt5.TIMEFRAME_H4).dropna()
        time_curent = df.index[-1]
        while True:
            df = MT5.get_data(
                "XAUUSDm", 2, timeframe=mt5.TIMEFRAME_H4).dropna()
            if time_curent == df.index[-2]:
                break
            check_time()
            time.sleep(60)
        # Get the current time in HH:MM:SS format
        check_time()
        # Perform trading logic at 5-minute intervals
        for asset in symbols_list.keys():
            symbol = symbols_list[asset][0]
            lot = symbols_list[asset][1]
            buy, sell, dif_tp, dif_sl = Pivot_Point(symbol)
            if buy or sell:
                MT5.run_Pivot_Point(symbol, buy, sell, lot, dif_tp,
                        dif_sl, magic, strategy)

        time.sleep(60)




