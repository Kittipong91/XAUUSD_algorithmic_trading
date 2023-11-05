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
    df = MT5.get_data(symbol, 640,timeframe=mt5.TIMEFRAME_M5).dropna()
    df['MA_16'] = df.close.rolling(window=16).mean()
    df['MA_64'] = df.close.rolling(window=64).mean()
    df['DIFF'] = df.MA_16 - df.MA_64
    df['DIFF_PREV'] = df.DIFF.shift(1)
    df['IS_TRADE'] = df.apply(is_trade, axis=1)
    df_trades = df[df.IS_TRADE!=0].copy()
    today = df_trades['IS_TRADE'].iloc[-1]
    if today == 1 :
        long = True
        sell = False
        return long, sell
    elif today == -1 :
        long = False
        sell = True
        return long, sell
    else :
        long = False
        sell = False
        return long,sell
    
def trade_every_5_minute(symbol):
    sell = True
    long = False
    return long, sell

def ATR(df, n):
    df = df.copy()
    df['High-Low'] = abs(df['high'] - df['low'])
    df['High-PrevClose'] = abs(df['high'] - df['close'].shift(1))
    df['Low-PrevClose'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis = 1, skipna = False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
    return df


def Momentum(symbol):

    df = MT5.get_data(symbol, 50,timeframe=mt5.TIMEFRAME_H4).dropna()
   
    df['ATR'] = ATR(df, 20)['ATR']
    df['direction'] = np.where(df['close'] > df['open'], 'bull', 'bear')
    df['dir_count'] = df.groupby((df['direction'] != df['direction'].shift(1)).cumsum()).cumcount() + 1
    ATR_SL = 0.5
    # Buy
    print(df)
    if df['dir_count'].iloc[-1] >= 5 and df['direction'].iloc[-1] == 'bull' :
        TP = df['close'].iloc[-1] + df['ATR'].iloc[-1] * ATR_SL,
        SL = df['open'].iloc[-1]
        return True , False ,TP , SL
    # Sell
    elif df['dir_count'].iloc[-1] >= 5 and df['direction'].iloc[-1] == 'bear' :
        TP = df['close'].iloc[-1] - df['ATR'].iloc[-1] * ATR_SL,
        SL = df['open'].iloc[-1]
        return False , True , TP , SL
    #Exit trades---------------------------------------------------------------------------
    #Buy profit

    else :
        long = False
        sell = False
        return long,sell ,0.01, 0.01






mt5.initialize()




symbols_list = {"Euro vs USdollar": ["EURUSDm", 0.01]}
current_account_info = mt5.account_info()
print("------------------------------------------------------------------")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Balance: {current_account_info.balance} USD,\t"
    f"Equity: {current_account_info.equity} USD, \t"
    f"Profit: {current_account_info.profit} USD")
print("------------------------------------------------------------------")

start = datetime.now().strftime("%H:%M:%S")#"23:59:59"
print('waiting.......')
# while True:
#     if datetime.now().weekday() not in (5,6):  
#         is_time = datetime.now().strftime("%H:%M:%S") == start
#     else:
#         is_time = False
#     if is_time:
#         for asset in symbols_list.keys():           
#             symbol = symbols_list[asset][0]
           
#             lot = symbols_list[asset][1]
#             buy, sell = moving_average_cross(symbol)
            
#             MT5.run(symbol, buy, sell, lot)


# Define the list of desired sleep times
sleep_times = ["23:00:00", "03:00:00", "07:00:00", "11:00:00", "15:00:00", "19:00:00"]
while True:
    current_time = time.strftime("%H:%M:%S")  # Get the current time in HH:MM:SS format
    print(current_time ,'waiting......')
    if current_time in sleep_times:
        # Perform trading logic at 5-minute intervals
        for asset in symbols_list.keys():           
            symbol = symbols_list[asset][0]
           
            lot = symbols_list[asset][1]
            buy, sell, tp, sl = Momentum(symbol)
            MT5.run(symbol, buy, sell, lot , tp , sl)
    time.sleep(60)

        

