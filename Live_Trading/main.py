# import sys
# sys.path.append('../')
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import numpy as np
import time
from MT5 import *
from strategies.Strategy import momentum
   
symbols_list = {
    "Gold - US Dollar": ["XAUUSDm", 0.01],
}

mt5.initialize()
current_account_info = mt5.account_info()
print("------------------------------------------------------------------")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Balance: {current_account_info.balance} USD,\t"
    f"Equity: {current_account_info.equity} USD, \t"
    f"Profit: {current_account_info.profit} USD")
print("------------------------------------------------------------------")

start = datetime.now().strftime("%H:%M:%S")#"23:59:59"
print('waiting.......')

def run() :
    while True:
        current_time = time.strftime("%H:%M:%S")  # Get the current time in HH:MM:SS format
        print(current_time ,'waiting......')
        # Perform trading logic at 5-minute intervals
        for asset in symbols_list.keys():           
            symbol = symbols_list[asset][0]
            lot = symbols_list[asset][1]
            buy, sell, tp, sl = momentum(symbol)
            if buy or sell :
                MT5.run(symbol, buy, sell, lot, tp, sl)
        time.sleep(60)

        
if __name__ == '__main__' :
    run()
