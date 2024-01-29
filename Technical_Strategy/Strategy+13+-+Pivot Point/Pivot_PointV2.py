from backtesting import Strategy
import numpy as np
import pandas as pd
from util.ATR import *
from util.SMA import *
from util.Bollinger_bands import *
from util.load_data import *

def PrepareDataV2(data):
    agg_dict = {"Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last"
                }
    daily_data = data.resample("D", offset="16H").agg(agg_dict).dropna()
    daily_data.columns = ["Open_d", "High_d", "Low_d", "Close_d"]
    data = pd.concat([data, daily_data.shift().dropna()],
                     axis=1).ffill().dropna()
    return data


class Pivot_PointV2(Strategy):
    periods = 14
    moving_av = 3

    def init(self):

        self.data.df["PP"] = (
            self.data.df["High_d"] + self.data.df["Low_d"] + self.data.df["Close_d"]) / 3
        self.data.df["S1"] = self.data.df["PP"] * 2 - self.data.df["High_d"]
        self.data.df["S2"] = self.data.df["PP"] - \
            (self.data.df["PP"] - self.data.df["PP"])
        self.data.df["R1"] = self.data.df["PP"] * 2 - self.data.df["Low_d"]
        self.data.df["R2"] = self.data.df["PP"] + \
            (self.data.df["High_d"] - self.data.df["Low_d"])

        self.data.df["position"] = np.where(
            self.data.df["Open"] > self.data.df["PP"], 1, -1)
        self.data.df["position"] = np.where(
            self.data.df["Open"] >= self.data.df["R1"], 0, self.data.df["position"])
        self.data.df["position"] = np.where(
            self.data.df["Open"] <= self.data.df["S1"], 0, self.data.df["position"])

    def next(self):
        position = self.data.df.loc[self.data.df.index[-1], 'position']
        if position == 1 :
            if self.position.is_short:
                self.position.close()
            
            if not self.position :
                self.buy(size=1)

        if position == 0 :
            if self.position.is_long:
                self.position.close()

            if not self.position :
                self.sell(size=1)

      
