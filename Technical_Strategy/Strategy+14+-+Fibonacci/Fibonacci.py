from scipy.signal import argrelextrema
from backtesting import Strategy
from util.ATR import *
from util.SMA import *
from util.plot_equity import *
from util.Bollinger_bands import *
from util.load_data import *
import numpy as np

class Fibonacci(Strategy):

    def init(self):
        pass

    def next(self):

        if self.data.position == 1:
            if self.position.is_short:
                self.position.close()
            self.buy(size=1)

        if self.data.position == -1:
            if self.position.is_long:
                self.position.close()
            self.sell(size=1)



            

def PrepareData(data , order = 7):
    
    data["hh"] = np.nan
    data["ll"] = np.nan

    for bar in range(len(data)):
        date = data.index[bar]
        current_low = data.iloc[:bar + 1].Low
        current_high = data.iloc[:bar + 1].High

        local_min = argrelextrema(
            current_low.values, np.less_equal, order=order)
        local_max = argrelextrema(
            current_high.values, np.greater_equal, order=order)

        data.loc[date, "hh"] = data.High.values[local_max][-1] if local_max[0].size > 0 else np.nan
        data.loc[date, "ll"] = data.Low.values[local_min][-1] if local_min[0].size > 0 else np.nan

    data["Trend"] = np.where(data.hh > data.ll, "Up", "Down")

    data["R23.6"] = np.where(data.Trend == "Up", data.hh - (data.hh - data.ll) * 0.236,
                             data.hh - (data.hh - data.ll) * (1 - 0.236))
    data["R38.2"] = np.where(data.Trend == "Up", data.hh - (data.hh - data.ll) * 0.382,
                             data.hh - (data.hh - data.ll) * (1 - 0.382))

    data["position"] = 0

    conditions = [
        (data.Trend == "Down") & (data.Close.shift() <
                                  data["R23.6"].shift()) & (data.Close > data["R23.6"]),
        (data.Trend == "Down") & (data.Close.shift() <
                                  data["R38.2"].shift()) & (data.Close >= data["R38.2"]),
        (data.Trend == "Down") & (data.Close.shift()
                                  > data.ll.shift()) & (data.Close <= data.ll),
        (data.Trend == "Up") & (data.Close.shift() >
                                data["R23.6"].shift()) & (data.Close < data["R23.6"]),
        (data.Trend == "Up") & (data.Close.shift() >
                                data["R38.2"].shift()) & (data.Close <= data["R38.2"]),
        (data.Trend == "Up") & (data.Close.shift() <
                                data.hh.shift()) & (data.Close >= data.hh),
        (data.hh != data.hh.shift()) | (data.ll != data.ll.shift())
    ]

    choices = [1, 0, 0, -1, 0, 0, 0]

    data["position"] = np.select(conditions, choices, default=data["position"])
    data["position"] = data.position.ffill().fillna(0)

    return data
