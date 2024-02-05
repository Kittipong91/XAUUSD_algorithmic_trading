# import sys
# sys.path.append('../')
from datetime import datetime
import MetaTrader5 as mt5
from MT5 import *
from strategies.Momentum import run_momentum
from strategies.Pivot_Point import run_Pivot_Point
   
mt5.initialize()
current_account_info = mt5.account_info()
print("------------------------------------------------------------------")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Balance: {current_account_info.balance} USD,\t"
    f"Equity: {current_account_info.equity} USD, \t"
    f"Profit: {current_account_info.profit} USD")
print("------------------------------------------------------------------")

start = datetime.now().strftime("%H:%M:%S")#"23:59:59"
print(start)
print('Starting.......')

        
if __name__ == '__main__' :

    # Strategy : Momentum
    # run_momentum()
    
    # Strategy : Pivot_Point
    run_Pivot_Point()

