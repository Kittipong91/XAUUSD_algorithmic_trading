from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas 

# Import the backtrader platform
import backtrader as bt
import argparse



class St(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)


df =  pandas.read_csv('../Data_Forex/EURUSD/EURUSD_H4 - EURUSD_H4.csv',parse_dates=True,index_col=0)
print(df)
  
data = bt.feeds.PandasData(dataname=df,fromdate=datetime.datetime(2008, 1, 1),todate=datetime.datetime(2023, 12, 31))

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot(iplot=False) 