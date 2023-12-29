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


def PrepareData(data):
    order = 70  # approx. 3 month
    ll = data.Low.copy()
    local_min = argrelextrema(ll.values, np.less_equal, order=order)

    data["hh"] = np.nan
    data["hh_date"] = np.nan
    for bar in range(len(data)):  # iterating over the bars
        date = data.index[bar]  # determine the current bar´s date
        hh = data.iloc[:bar+1].High  # get the high column until current bar

        # determine all local highs until current bar
        local_max = argrelextrema(hh.values, np.greater_equal, order=order)

        # determine the most recent local high (price) and add to "hh" column
        data.loc[date, "hh"] = data.High.values[local_max][-1]

        # determine the most recent local high (date) and add to "hh_date" column
        data.loc[date, "hh_date"] = data.index[local_max][-1]

    data["ll"] = np.nan
    data["ll_date"] = np.nan
    for bar in range(len(data)):  # iterating over the bars
        date = data.index[bar]  # determine the current bar´s date
        ll = data.iloc[:bar+1].Low  # get the high column until current bar

        # determine all local lows until current bar
        local_min = argrelextrema(ll.values, np.less_equal, order=order)

        # determine the most recent local low (price) and add to "ll" column
        data.loc[date, "ll"] = data.Low.values[local_min][-1]

        # determine the most recent local low (date) and add to "ll_date" column
        data.loc[date, "ll_date"] = data.index[local_min][-1]

    data["Trend"] = np.where(data.hh_date > data.ll_date, "Up", "Down")

    data.drop(columns=["hh_date", "ll_date"], inplace=True)

    data["R23.6"] = np.where(data.Trend == "Up", data.hh - (data.hh-data.ll)
                             * 0.236, data.hh - (data.hh-data.ll) * (1-0.236))

    data["R38.2"] = np.where(data.Trend == "Up", data.hh - (data.hh-data.ll)
                             * 0.382, data.hh - (data.hh-data.ll) * (1-0.382))

    data["position"] = np.where((data.hh != data.hh.shift()) | (
        data.ll != data.ll.shift()), 0, np.nan)

    data["position"] = np.where((data.Trend == "Down") & (data.Close.shift(
    ) < data["R23.6"].shift()) & (data.Close > data["R23.6"]), 1, data.position)

    data["position"] = np.where((data.Trend == "Down") & (data.Close.shift(
    ) < data["R38.2"].shift()) & (data.Close >= data["R38.2"]), 0, data.position)

    data["position"] = np.where((data.Trend == "Down") & (
        data.Close.shift() > data.ll.shift()) & (data.Close <= data.ll), 0, data.position)

    data["position"] = np.where((data.Trend == "Up") & (data.Close.shift(
    ) > data["R23.6"].shift()) & (data.Close < data["R23.6"]), -1, data.position)

    data["position"] = np.where((data.Trend == "Up") & (data.Close.shift(
    ) > data["R38.2"].shift()) & (data.Close <= data["R38.2"]), 0, data.position)

    data["position"] = np.where((data.Trend == "Up") & (data.Close.shift(
    ) < data.hh.shift()) & (data.Close >= data.hh), 0, data.position)

    data["position"] = np.where((data.hh != data.hh.shift()) | (
        data.ll != data.ll.shift()), 0, data.position)

    data["position"] = data.position.ffill()

    return data
